from typing import Dict, List
from .utils.env import get_config, get_ttl_by_type
from .logProvider import logger
import redis
from redis.commands.json.path import Path
from .baseObj import BaseObj
from singleton import Singleton
from .enums import TTL_Type
from .validators import validate_base_obj_cls, validate_base_obj_instance

class RedisClient(metaclass=Singleton):
    def __init__(self,  host: str = None, port: int = None):
        self.redisInstance = None
        self.channelLastMessage = {}

    def getDatabase(self):
        if (self.redisInstance is None):
            host = get_config().redis_host
            port = get_config().redis_port

            self.redisInstance = redis.Redis(host=host, port=port, db=0, decode_responses=True)

        return self.redisInstance

    @validate_base_obj_instance
    def saveToDB (self, objId: str, dataObj : BaseObj):
        db = self.getDatabase()

        db.json().set(f"{dataObj.dbCollectionName}:{objId}", '.', dataObj.toJSON())

    @validate_base_obj_instance
    def saveTempToDB (self, objId: str, dataObj : BaseObj, ttlType: TTL_Type = TTL_Type.LONG):
        if (dataObj.dbCollectionName == ""):
            logger.error(f'RedisClient.saveTempToDB called for Class {dataObj.__name__} but does not have dbCollectionName defined.')
            raise Exception(f'RedisClient.saveTempToDB called for Class {dataObj.__name__} but does not have dbCollectionName defined.')

        self.saveToDB(objId=objId,dataObj=dataObj)

        objTTL = get_ttl_by_type(ttlType=ttlType)

        self.getDatabase().expire(f"{dataObj.dbCollectionName}:{objId}", objTTL)

    # get all ids for this cls
    @validate_base_obj_cls
    def loadIdsFromDB(self, cls, filter= '*'):
        foundAllObjsIds = self.getDatabase().scan_iter(f"{cls.dbCollectionName}:{filter}")

        allObjsIds : list[str]= []
        for currFoundObjId in foundAllObjsIds:
            currObjId : str = currFoundObjId.replace(f'{cls.dbCollectionName}:',"")
            allObjsIds.append(currObjId)

        # all objsIds is Iterator - convert to list
        return list(allObjsIds)

    @validate_base_obj_cls
    def loadFromDB(self, cls, objId):
        db = self.getDatabase()
        result = db.json().get(f"{cls.dbCollectionName}:{objId}")

        if result:
            return cls.fromJSON(result)
        else:
            return None

    @validate_base_obj_cls
    def loadManyFromDB (self, cls, filter) -> List[BaseObj]:
        db = self.getDatabase()
        objectsList : List[BaseObj] = []
        for objId in db.scan_iter(f"{cls.dbCollectionName}:{filter}"):
            # Get the JSON data for each matched key
            
            jsonData = db.json().get(f'{objId}', Path.root_path())
            currUserObjRef = cls.fromJSON(jsonData)

            if (currUserObjRef is not None):
                objectsList.append(currUserObjRef)

        return objectsList

    @validate_base_obj_cls
    def removeFromDB(self, objId : str, cls):
        db = self.getDatabase()        
        db.delete(f"{cls.dbCollectionName}:{objId}")

    def pubObjToChannel(self, channelId, dataObj: BaseObj):
        self.getDatabase().xadd(channelId, {'data': dataObj.toJSON()})

    @validate_base_obj_cls
    def subGetObjFromChannel(self, channelId, cls, timeout=5000) -> Dict[str,BaseObj]:
        if (channelId not in self.channelLastMessage):
            self.channelLastMessage [channelId] = '0-0'

        lastMessageId = self.channelLastMessage[channelId]
        rawMessages = self.getDatabase().xread({channelId: lastMessageId}, block=timeout)

        if rawMessages is None:
            return {}
        
        objsDict = {}
        # Process and delete the messages
        for stream, message_list in rawMessages:
            for messageId, message_data in message_list:
                # jsonData = message_data[b'data'].decode('utf-8')  # Convert bytes to string
                jsonData = message_data['data']
                # jsonData = json.loads(json_string)  # Parse JSON

                currObj = cls.fromJSON(jsonData)
                objsDict[messageId]= currObj

                self.channelLastMessage[channelId] = messageId

        return objsDict

    def removeFromChannel(self, channelId: str, messageId: str):
        # Delete the processed message from the stream
        self.getDatabase().xdel(channelId, messageId)
