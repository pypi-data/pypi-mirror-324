from .redisClient import RedisClient
from .logProvider import logger
from .baseObj import BaseObj
from singleton import Singleton
from pymongo import MongoClient
from .validators import validate_base_obj_cls, validate_base_obj_instance
from .utils.env import get_config 

#TBD: add support for redis configutation

class DBClient(metaclass=Singleton):
    useRedisCache : bool
    redisCache : RedisClient

    def __init__(self):
        #empty __init__ to allow external configuration
        pass

    def getDatabase(self):                
        if self.dbInstance is None:
            host = get_config().db_host
            port = get_config().db_port
            dbName = get_config().db_name   
            self.useRedisCache = get_config().db_useRedisCache
            
            if (dbName is None or dbName == ""):
                logger.critical(f'DBClient was created without dbName')
                return None
            
            connectionString = f"mongodb://{host}:{port}/"
            client = MongoClient(connectionString, tz_aware=True)

            self.dbInstance = client[self.dbName]

        return self.dbInstance
    
    @validate_base_obj_instance
    def saveToDB (self, dataObj : BaseObj, filter = {}):
        db = self.getDatabase()
        collection = db[dataObj.dbCollectionName]

        if (filter == {}):
            filter = {'id': dataObj.id}
            
        collection.replace_one(filter, dataObj.serialize(), upsert=True)

        if (self.useRedisCache and dataObj.isCached):
            #update cache
            self.redisCache.saveTempToDB(dataObj.id, dataObj=dataObj)

    @validate_base_obj_cls
    def loadFromDB(self, cls, field_value, field_name: str = 'id'):
        if (self.useRedisCache and cls.isCached):
            # see if the data is in the cache
            obj = self.redisCache.loadFromDB(cls=cls, objId=field_value)
            if (obj is not None):
                return obj

        db = self.getDatabase()
        collection = db[cls.dbCollectionName]

        query = {field_name: field_value}
        result = collection.find_one(query)

        if result:
            # Remove '_id' 
            result.pop('_id', None)
            obj : BaseObj = cls.deserialize(result)
           
            if (obj is None):
                logger.error(f'loadFromDB failed to desiralize objId {field_value}, result is {result}')
                return None

            if (self.useRedisCache and cls.isCached):
                # update cache
                self.redisCache.saveTempToDB(objId=obj.id, dataObj=obj)

            return obj
        else:
            return None
        
    @validate_base_obj_cls
    def loadManyFromDB(self, cls, field_name: str, field_value):
        db = self.getDatabase()
        collection = db[cls.dbCollectionName]

        query = {field_name: field_value}
        results = collection.find(query)

        objects = []
        for result in results:
            result.pop('_id', None)  # Remove '_id'
            obj = cls.deserialize(result)
            objects.append(obj)

            if (self.useRedisCache and cls.isCached):
                # update cache
                self.redisCache.saveTempToDB(objId=obj.id, dataObj=obj)

        return objects

    @validate_base_obj_cls
    def loadManyFromDBByFilter(self, cls, filter = {}):
        db = self.getDatabase()
        collection = db[cls.dbCollectionName]

        results = collection.find(filter)

        objects = []
        for result in results:
            result.pop('_id', None)  # Remove '_id'
            obj = cls.deserialize(result)
            objects.append(obj)

            if (self.useRedisCache and cls.isCached):
                # update cache
                self.redisCache.saveTempToDB(objId=obj.id, dataObj=obj)            

        return objects