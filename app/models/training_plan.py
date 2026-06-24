from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import final
from app.database import Base
from app.models.Enums.PlanStatus import PlanStatus

@final
class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("coach_profiles.id"), nullable=False)
    athlete_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(Enum(PlanStatus), default=PlanStatus.DRAFT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    coach = relationship("CoachProfile", backref="training_plans")
    athlete = relationship("User", backref="training_plans")
    workouts = relationship("DailyWorkout", back_populates="plan", cascade="all, delete-orphan")
