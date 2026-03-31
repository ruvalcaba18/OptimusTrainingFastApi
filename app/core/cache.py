import json
import logging
from functools import wraps
from typing import Any, Callable, Optional

from app.core.redis_client import get_redis

logger = logging.getLogger("optimus")

_CACHE_ENABLED = True

async def cache_get(key: str) -> Optional[Any]:
    try:
        client = await get_redis()
        raw = await client.get(key)
        if raw is not None:
            return json.loads(raw)
    except Exception as exc:
        logger.debug("Cache GET miss/error for %s: %s", key, exc)
    return None


async def cache_set(key: str, value: Any, ttl: int) -> None:
    try:
        client = await get_redis()
        await client.setex(key, ttl, json.dumps(value, default=str))
    except Exception as exc:
        logger.debug("Cache SET error for %s: %s", key, exc)


async def cache_delete(key: str) -> None:
    try:
        client = await get_redis()
        await client.delete(key)
    except Exception as exc:
        logger.debug("Cache DELETE error for %s: %s", key, exc)


async def cache_delete_pattern(pattern: str) -> None:
    try:
        client = await get_redis()
        keys = await client.keys(pattern)
        if keys:
            await client.delete(*keys)
    except Exception as exc:
        logger.debug("Cache DELETE pattern error for %s: %s", pattern, exc)


def make_key(*parts) -> str:
    return ":".join(str(p) for p in parts if p is not None)
