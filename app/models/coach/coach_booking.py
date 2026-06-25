from sqlalchemy import (
    Column, Integer, String, Float, DateTime,
    Text, ForeignKey, Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class CoachBooking(Base):
    __tablename__ = "coach_bookings"

                                                                            
    id = Column(Integer, primary_key=True, index=True)

                                                                            
    coach_id = Column(
        Integer, ForeignKey("coach_profiles.id", ondelete="CASCADE"), nullable=False
    )
    athlete_id = Column(Integer, ForeignKey("users.id"), nullable=False)

                                                                            
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    session_type = Column(String(50), nullable=True)                            

                                                                            
    location_name = Column(String(300), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

                                                                            
    status = Column(String(20), default="pending", nullable=False)

                                                                            
    total_price = Column(Float, nullable=False)
    currency = Column(String(10), default="MXN", nullable=False)

                                                                            
    athlete_notes = Column(Text, nullable=True)
    coach_notes = Column(Text, nullable=True)

                                                                            
    athlete_rating = Column(Float, nullable=True)
    athlete_review = Column(Text, nullable=True)

                                                                            
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

                                                                            
    coach = relationship("CoachProfile", back_populates="bookings")
    athlete = relationship("User", backref="coach_bookings")
