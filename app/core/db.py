"""
Backward compatibility shim.
The canonical DB session is now in app/database/session.py.
This file re-exports it so any code that still imports from app.core.db continues to work.
"""
from app.database import Base, engine, SessionLocal, get_db  # noqa: F401
