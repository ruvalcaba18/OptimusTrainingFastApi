from typing import final

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


@final
class CoachAthlete(Base):
    __tablename__ = "coach_athletes"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("coach_profiles.id", ondelete="CASCADE"), nullable=False)
    athlete_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    coach = relationship("CoachProfile", backref="athletes_relation")
    athlete = relationship("User", backref="coach_relation")
