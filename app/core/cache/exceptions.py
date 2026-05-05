class CacheError(Exception):
    """Base exception for cache operations."""
    pass

class RedisConnectionError(CacheError):
    """Raised when there's an error connecting to Redis."""
    pass

class CacheSerializationError(CacheError):
    """Raised when there's an error serializing or deserializing cache data."""
    pass
