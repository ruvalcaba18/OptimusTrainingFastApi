from typing import final

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


@final
class UserRoutine(Base):
    __tablename__ = "user_routines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    week = Column(Integer, nullable=False, default=1) # Week 1, 2, 3, 4
    day = Column(Integer, nullable=False)
    goal = Column(String, nullable=False)
    level = Column(String, nullable=False)
    volume = Column(String, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(String, nullable=False)
    rest = Column(String, nullable=False)
    method_name = Column(String, nullable=False)
    exercises = Column(JSON, nullable=False) # Snapshot list of exercises
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="user_routines")
