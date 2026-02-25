"""
Database package.

Subdirectories:
  session/  → Configuración del engine, SessionLocal, Base y get_db

Si en el futuro necesitas un segundo motor (por ejemplo Redis o lectura replicas),
agrégalo como un nuevo subfolder aquí: database/cache/, database/read_replica/, etc.
"""
from app.database.session.session import Base, engine, SessionLocal, get_db

__all__ = ["Base", "engine", "SessionLocal", "get_db"]
