import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.error_handlers import register_exception_handlers
from app.core.logging_config import setup_logging
from app.core.middleware import SecurityMiddleware
from app.core.cache import cache_service
from app.database.session.session import engine, Base
import app.models 

setup_logging()
logger = logging.getLogger("optimus")

from app.core.rate_limiter import limiter


async def startup_db_init():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created successfully.")
    except Exception as e:
        logger.error("Error creating database tables: %s", e)

async def startup_redis_check():
    try:
        if await cache_service.health_check():
            logger.info("Redis connected: %s", settings.REDIS_URL)
    except Exception as exc:
        logger.warning("Redis not available — caching/blacklisting disabled: %s", exc)

# MARK: - Lifespan

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_init()
    await startup_redis_check()

    yield

    await cache_service.close()
    logger.info("App shutdown complete.")


# MARK: - App Initialization

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API de deportes y entrenamiento — escalable a 1 millón de usuarios.",
    version="2.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Request-ID"],
    expose_headers=["X-Process-Time-Ms"],
)

app.add_middleware(SecurityMiddleware)

UPLOADS_DIR = Path(__file__).parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health"], summary="Health check")
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
