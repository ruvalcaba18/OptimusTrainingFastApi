from typing import Any
from app.core.cache.service import cache_service, CacheTTL
from app.core.cache.exceptions import CacheError, RedisConnectionError, CacheSerializationError

async def cache_get(key: str):
    return await cache_service.get(key)

async def cache_set(key: str, value: Any, ttl: int):
    return await cache_service.set(key, value, ttl)

async def cache_delete(key: str):
    return await cache_service.delete(key)

async def cache_delete_pattern(pattern: str):
    return await cache_service.delete_pattern(pattern)

def make_key(*parts):
    return cache_service.make_key(*parts)

__all__ = [
    "cache_service", 
    "cache_get", 
    "cache_set", 
    "cache_delete", 
    "cache_delete_pattern", 
    "make_key",
    "CacheTTL",
    "CacheError", 
    "RedisConnectionError", 
    "CacheSerializationError"
]
