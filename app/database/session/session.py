"""
Database session configuration.
Supports connection pooling for high-concurrency (100k users).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


# ─── Connection pool tuning for production scale ───────────────────────────
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,        # Detect stale connections automatically
    pool_size=10,              # Persistent connections kept alive
    max_overflow=20,           # Extra connections under heavy load
    pool_timeout=30,           # Seconds to wait for a connection
    pool_recycle=1800,         # Recycle connections every 30 min
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy models."""
    pass


# ─── Dependency ─────────────────────────────────────────────────────────────
def get_db():
    """Provide a transactional database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
