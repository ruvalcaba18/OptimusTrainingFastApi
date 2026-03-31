from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

_is_sqlite = settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite")

engine_kwargs = {
    "pool_pre_ping": True,
    "pool_recycle": 1800,
}

if not _is_sqlite:
    engine_kwargs.update({
        "pool_size": 20,
        "max_overflow": 40,
        "pool_timeout": 30,
    })
else:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
