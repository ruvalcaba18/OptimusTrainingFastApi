import json
import logging
import redis.asyncio as aioredis
from typing import Any, Optional, List
from app.core.config import settings
from app.core.cache.exceptions import RedisConnectionError, CacheSerializationError

logger = logging.getLogger("optimus")

from enum import IntEnum

class CacheTTL(IntEnum):
    """TTL values in seconds."""
    MINUTE = 60
    SHORT = 300      # 5 minutes
    MEDIUM = 1800    # 30 minutes
    LONG = 3600      # 1 hour
    HOUR = 3600
    DAY = 86400      # 24 hours
    WEEK = 604800    # 7 days

class RedisCacheService:
    def __init__(self):
        self._redis_client: Optional[aioredis.Redis] = None

    async def get_client(self) -> aioredis.Redis:
        if self._redis_client is None:
            try:
                self._redis_client = aioredis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2,
                )
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise RedisConnectionError(f"Could not connect to Redis at {settings.REDIS_URL}")
        return self._redis_client

    async def close(self):
        if self._redis_client:
            await self._redis_client.aclose()
            self._redis_client = None

    async def get(self, key: str) -> Optional[Any]:
        try:
            client = await self.get_client()
            raw = await client.get(key)
            if raw is not None:
                return json.loads(raw)
        except json.JSONDecodeError:
            raise CacheSerializationError(f"Error deserializing data for key: {key}")
        except Exception as e:
            logger.debug(f"Cache GET error for {key}: {e}")
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        try:
            client = await self.get_client()
            await client.setex(key, ttl, json.dumps(value, default=str))
        except Exception as e:
            logger.error(f"Cache SET error for {key}: {e}")
            raise CacheSerializationError(f"Error serializing data for key: {key}")

    async def delete(self, key: str) -> None:
        try:
            client = await self.get_client()
            await client.delete(key)
        except Exception as e:
            logger.debug(f"Cache DELETE error for {key}: {e}")

    async def delete_pattern(self, pattern: str) -> None:
        try:
            client = await self.get_client()
            keys = await client.keys(pattern)
            if keys:
                await client.delete(*keys)
        except Exception as e:
            logger.debug(f"Cache DELETE pattern error for {pattern}: {e}")

    async def is_blacklisted(self, jti: str) -> bool:
        try:
            client = await self.get_client()
            return await client.exists(f"blacklist:{jti}") == 1
        except Exception:
            return False

    async def blacklist_token(self, jti: str, ttl_seconds: int) -> None:
        try:
            client = await self.get_client()
            await client.setex(f"blacklist:{jti}", ttl_seconds, "1")
        except Exception as e:
            logger.error(f"Error blacklisting token {jti}: {e}")

    async def health_check(self) -> bool:
        try:
            client = await self.get_client()
            return await client.ping()
        except Exception:
            return False

    @staticmethod
    def make_key(*parts) -> str:
        return ":".join(str(p) for p in parts if p is not None)

cache_service = RedisCacheService()
