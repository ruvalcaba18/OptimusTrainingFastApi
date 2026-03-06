"""
SQLAlchemy Active Break models.
Plantillas de pausas activas y log de uso por empleado.
"""
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    Text, ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ActiveBreakSession(Base):
    """
    Plantilla reutilizable de pausa activa.
    Ejemplo: "Estiramiento de espalda — 10 min".
    """
    __tablename__ = "active_break_sessions"

    # ─── Primary key ──────────────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)

    # ─── Content ──────────────────────────────────────────────────────────
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)         # BreakCategory enum value
    duration_minutes = Column(Integer, nullable=False)     # 10 | 20 | 30
    instructions = Column(Text, nullable=True)             # Pasos a seguir
    video_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    # ─── Status ───────────────────────────────────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)

    # ─── Timestamps ───────────────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # ─── Relationships ────────────────────────────────────────────────────
    logs = relationship(
        "ActiveBreakLog", back_populates="session", cascade="all, delete-orphan"
    )


class ActiveBreakLog(Base):
    """
    Registro cada vez que un empleado comienza / completa una pausa activa.
    Sirve para reportes y gamificación futura.
    """
    __tablename__ = "active_break_logs"

    # ─── Primary key ──────────────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)

    # ─── Foreign keys ─────────────────────────────────────────────────────
    session_id = Column(
        Integer, ForeignKey("active_break_sessions.id"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    enterprise_id = Column(
        Integer, ForeignKey("enterprises.id"), nullable=True
    )

    # ─── Tracking ─────────────────────────────────────────────────────────
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # ─── Relationships ────────────────────────────────────────────────────
    session = relationship("ActiveBreakSession", back_populates="logs")
    user = relationship("User", backref="active_break_logs")
