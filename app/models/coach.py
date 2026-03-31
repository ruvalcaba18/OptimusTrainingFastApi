from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, Text, ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class CoachProfile(Base):
    __tablename__ = "coach_profiles"

                                                                            
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

                                                                            
    bio = Column(Text, nullable=True)
    specialty = Column(String(50), nullable=False)
    experience_years = Column(Integer, nullable=False)
    certifications = Column(Text, nullable=True)

                                                                            
    hourly_rate = Column(Float, nullable=False)
    currency = Column(String(10), default="MXN", nullable=False)

                                                                            
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    service_radius_km = Column(Float, default=10.0, nullable=False)

                                                                            
    is_available = Column(Boolean, default=True, nullable=False)
    available_hours = Column(Text, nullable=True)               

                                                                            
    avg_rating = Column(Float, default=0.0, nullable=False)
    total_reviews = Column(Integer, default=0, nullable=False)

                                                                            
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_searchable = Column(Boolean, default=True, nullable=False)

                                                                            
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

                                                                            
    user = relationship("User", backref="coach_profile")
    bookings = relationship(
        "CoachBooking", back_populates="coach", cascade="all, delete-orphan"
    )
