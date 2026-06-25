from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime,
    Text, ForeignKey, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Event(Base):
    __tablename__ = "events"

                                                                            
    id = Column(Integer, primary_key=True, index=True)

                                                                            
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

                                                                            
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    event_type = Column(String(50), nullable=False)
    status = Column(String(20), default="draft", nullable=False)

                                                                            
    location_name = Column(String(300), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

                                                                            
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)

                                                                            
    max_participants = Column(Integer, nullable=True)                     
    is_public = Column(Boolean, default=True, nullable=False)

                                                                            
    cover_image_url = Column(String, nullable=True)

                                                                            
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

                                                                            
    creator = relationship("User", backref="created_events")
    participants = relationship(
        "EventParticipant", back_populates="event", cascade="all, delete-orphan"
    )


class EventParticipant(Base):
    __tablename__ = "event_participants"

                                                                            
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(
        Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

                                                                            
    event = relationship("Event", back_populates="participants")
    user = relationship("User", backref="event_participations")

                                                                            
    __table_args__ = (
        UniqueConstraint("event_id", "user_id", name="uq_event_participant"),
    )
