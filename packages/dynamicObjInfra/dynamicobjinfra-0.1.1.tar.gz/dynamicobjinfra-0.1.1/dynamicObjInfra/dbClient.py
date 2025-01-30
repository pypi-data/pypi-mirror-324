from redisClient import RedisClient
from logProvider import logger
from baseObj import BaseObj
from singleton import Singleton
from pymongo import MongoClient
from validators import validate_base_obj_cls, validate_base_obj_instance

#TBD: add support for redis configutation

class DBClient(metaclass=Singleton):
    host : str
    port : int
    dbName : str
    redisCache : RedisClient

    def __init__(self):
        pass

    def setConnectionDetails(self, host: str, port: int, dbName: str,useRedisCache: bool = False, redisHost: str = None, redisPort: int = None):
        self.host = host
        self.port = port
        self.dbName = dbName
        
        if (self.host is None or self.port is None or self.dbName is None):
            logger.critical(f'DBClient was created without host or port, or dbName')
            return

        self.useRedisCache = useRedisCache
        if (self.useRedisCache):
            if (redisHost is None or redisPort is None):
                logger.critical(f'DBClient was created with useRedisCache, but without redisHost or redisPort')
                self.useRedisCache = False
            else:
                self.redisCache.setConnectionDetails(host=self.redisHost, port=self.redisPort)

    def getDatabase(self):
        if (self.host is None or self.port is None or self.dbName is None):
            logger.critical(f'DBClient was created without host or port, or dbName')
            return None
                
        if self.dbInstance is None:
            connectionString = f"mongodb://{self.host}:{self.port}/"
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