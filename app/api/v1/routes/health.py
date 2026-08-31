from fastapi import APIRouter

from app.core.cache import cache_service
from app.core.config import settings

router = APIRouter()

@router.get("/", tags=["Health"], summary="Health check")
async def root():
    redis_ok = await cache_service.health_check()
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT,
        "docs": f"{settings.API_V1_STR}/docs",
        "services": {
            "redis": "up" if redis_ok else "down",
        },
    }
