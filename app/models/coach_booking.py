"""
SQLAlchemy Coach Booking model.
Un atleta contrata a un coach para una sesión de entrenamiento.
"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime,
    Text, ForeignKey, Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class CoachBooking(Base):
    __tablename__ = "coach_bookings"

    # ─── Primary key ──────────────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)

    # ─── Participants ─────────────────────────────────────────────────────
    coach_id = Column(
        Integer, ForeignKey("coach_profiles.id", ondelete="CASCADE"), nullable=False
    )
    athlete_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ─── Session details ──────────────────────────────────────────────────
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    session_type = Column(String(50), nullable=True)  # "presencial" | "virtual"

    # ─── Location ─────────────────────────────────────────────────────────
    location_name = Column(String(300), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # ─── Status ───────────────────────────────────────────────────────────
    status = Column(String(20), default="pending", nullable=False)

    # ─── Price ────────────────────────────────────────────────────────────
    total_price = Column(Float, nullable=False)
    currency = Column(String(10), default="MXN", nullable=False)

    # ─── Notes ────────────────────────────────────────────────────────────
    athlete_notes = Column(Text, nullable=True)
    coach_notes = Column(Text, nullable=True)

    # ─── Rating (post-sesión) ─────────────────────────────────────────────
    athlete_rating = Column(Float, nullable=True)
    athlete_review = Column(Text, nullable=True)

    # ─── Timestamps ───────────────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # ─── Relationships ────────────────────────────────────────────────────
    coach = relationship("CoachProfile", back_populates="bookings")
    athlete = relationship("User", backref="coach_bookings")
