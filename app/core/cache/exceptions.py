class CacheError(Exception):
    
    pass

class RedisConnectionError(CacheError):
    
    pass

class CacheSerializationError(CacheError):
    
    pass
