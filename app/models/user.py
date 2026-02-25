"""
SQLAlchemy User model.
Includes profile_picture_url for photo uploads.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    # ─── Primary key ──────────────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)

    # ─── Auth ─────────────────────────────────────────────────────────────
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # ─── Personal info ────────────────────────────────────────────────────
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)

    # ─── Sports profile ───────────────────────────────────────────────────
    exercise_frequency = Column(String, nullable=False)
    training_type = Column(String, nullable=False)

    # ─── Profile picture ──────────────────────────────────────────────────
    profile_picture_url = Column(String, nullable=True)

    # ─── Timestamps ───────────────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
