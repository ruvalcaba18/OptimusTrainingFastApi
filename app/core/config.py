"""
App settings — all values can be overridden via environment variables or .env file.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # ─── Meta ─────────────────────────────────────────────────────────────
    PROJECT_NAME: str = "Optimus Training API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"   # development | staging | production

    # ─── Security ─────────────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-in-production-use-a-256-bit-random-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120           # 2 hours
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 60    # 1 hour

    # ─── Email (Mocked for now) ───────────────────────────────────────────
    EMAILS_FROM_NAME: str = "Optimus Training"
    EMAILS_FROM_EMAIL: str = "info@optimus.com"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # ─── Database ─────────────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:password@localhost/optimus_db"

    # ─── Uploads ──────────────────────────────────────────────────────────
    MAX_UPLOAD_SIZE_MB: int = 5
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".webp"]

    # ─── Validation ───────────────────────────────────────────────────────
    MIN_PASSWORD_LENGTH: int = 8

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
