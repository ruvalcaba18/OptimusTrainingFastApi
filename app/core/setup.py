import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.error_handlers import register_exception_handlers
from app.core.logging_config import setup_logging
from app.core.middleware import MiddlewareConfigurator
from app.core.cache import cache_service
from app.database.session.session import engine, Base, SessionLocal
from app.models import Goal
from app.database.seed_all import DatabaseSeeder
from app.core.rate_limiter import limiter
from app.api.v1.routes.health import router as health_router

logger = logging.getLogger("optimus")


class ApplicationBuilder:
    """
    Builder responsible for configuring and initializing the FastAPI application.
    """

    @staticmethod
    def setup_database_schema() -> None:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables verified/created successfully.")
        except Exception as e:
            logger.error("Error creating database tables: %s", e)

    @staticmethod
    def seed_initial_data() -> None:
        db = SessionLocal()
        try:
            if db.query(Goal).count() == 0:
                logger.info("Database is empty. Running database seeder...")
                data_dir = Path(__file__).parent.parent / "database" / "data"
                seeder = DatabaseSeeder(db, data_dir)
                seeder.seed_all()
                logger.info("Database seeded successfully during startup!")
        except Exception as e:
            logger.error("Error seeding database on startup: %s", e)
        finally:
            db.close()

    @staticmethod
    async def verify_redis_connection() -> None:
        try:
            if await cache_service.health_check():
                logger.info("Redis connected: %s", settings.REDIS_URL)
        except Exception as exc:
            logger.warning("Redis not available — caching/blacklisting disabled: %s", exc)

    @classmethod
    @asynccontextmanager
    async def lifespan(cls, app: FastAPI):
        cls.setup_database_schema()
        cls.seed_initial_data()
        await cls.verify_redis_connection()
        yield
        await cache_service.close()
        logger.info("App shutdown complete.")

    @classmethod
    def build(cls) -> FastAPI:
        setup_logging()
        
        app = FastAPI(
            title=settings.PROJECT_NAME,
            description="API de deportes y entrenamiento — escalable a 1 millón de usuarios.",
            version="2.0.0",
            openapi_url=f"{settings.API_V1_STR}/openapi.json",
            docs_url=f"{settings.API_V1_STR}/docs",
            redoc_url=f"{settings.API_V1_STR}/redoc",
            lifespan=cls.lifespan,
        )
        
        # Configure Rate Limiter
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        
        # Register Exception Handlers
        register_exception_handlers(app)
        
        # Register Middlewares
        MiddlewareConfigurator.register(app)
        
        # Mount Uploads Static Files
        uploads_dir = Path(__file__).parent.parent / "uploads"
        uploads_dir.mkdir(exist_ok=True)
        app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")
        
        # Include API Routers
        app.include_router(api_router, prefix=settings.API_V1_STR)
        
        # Include Health/Root Router
        app.include_router(health_router)
        
        return app
