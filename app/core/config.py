from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Optimus Training API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-super-secret-key-change-me"  # In production, use env var
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:password@localhost/optimus_db"

    # Validation constraints
    MIN_PASSWORD_LENGTH: int = 8

    class Config:
        case_sensitive = True

settings = Settings()
