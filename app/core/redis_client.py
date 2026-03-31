import redis.asyncio as aioredis
from app.core.config import settings

_redis_client: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
    return _redis_client


async def close_redis() -> None:
    global _redis_client
    if _redis_client:
        await _redis_client.aclose()
        _redis_client = None


async def is_token_blacklisted(jti: str) -> bool:
    try:
        client = await get_redis()
        return await client.exists(f"blacklist:{jti}") == 1
    except Exception:
        return False


async def blacklist_token(jti: str, ttl_seconds: int) -> None:
    try:
        client = await get_redis()
        await client.setex(f"blacklist:{jti}", ttl_seconds, "1")
    except Exception:
        pass


async def redis_health() -> bool:
    try:
        client = await get_redis()
        return await client.ping()
    except Exception:
        return False
