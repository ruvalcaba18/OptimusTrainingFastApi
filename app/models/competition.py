"""
SQLAlchemy Competition models.
Competencias deportivas con rankings y scores.

ACID:
  - UniqueConstraint en (competition_id, user_id) previene inscripciones duplicadas.
  - Score updates son idempotentes — se usa with_for_update() en el service.
"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime,
    Text, ForeignKey, Boolean, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Competition(Base):
    __tablename__ = "competitions"

    # ─── Primary key ──────────────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)

    # ─── Creator ──────────────────────────────────────────────────────────
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ─── Info ─────────────────────────────────────────────────────────────
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    sport_type = Column(String(50), nullable=False)
    status = Column(String(20), default="upcoming", nullable=False)

    # ─── Schedule ─────────────────────────────────────────────────────────
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)

    # ─── Location ─────────────────────────────────────────────────────────
    location_name = Column(String(300), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # ─── Rules ────────────────────────────────────────────────────────────
    max_participants = Column(Integer, nullable=True)
    rules = Column(Text, nullable=True)
    prize_description = Column(Text, nullable=True)

    # ─── Image ────────────────────────────────────────────────────────────
    cover_image_url = Column(String, nullable=True)

    # ─── Timestamps ───────────────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # ─── Relationships ────────────────────────────────────────────────────
    creator = relationship("User", backref="created_competitions")
    participants = relationship(
        "CompetitionParticipant", back_populates="competition", cascade="all, delete-orphan"
    )


class CompetitionParticipant(Base):
    __tablename__ = "competition_participants"

    # ─── Primary key ──────────────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)
    competition_id = Column(
        Integer, ForeignKey("competitions.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ─── Ranking / Score ──────────────────────────────────────────────────
    score = Column(Float, nullable=True)
    position = Column(Integer, nullable=True)

    # ─── Timestamps ───────────────────────────────────────────────────────
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # ─── Relationships ────────────────────────────────────────────────────
    competition = relationship("Competition", back_populates="participants")
    user = relationship("User", backref="competition_participations")

    # ─── ACID: evita inscripción duplicada a nivel de DB ──────────────────
    __table_args__ = (
        UniqueConstraint("competition_id", "user_id", name="uq_competition_participant"),
    )
