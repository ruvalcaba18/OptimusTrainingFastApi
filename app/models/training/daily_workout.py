from typing import final

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.Enums.WorkoutStatus import WorkoutStatus


@final
class DailyWorkout(Base):
    __tablename__ = "daily_workouts"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("training_plans.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(WorkoutStatus), default=WorkoutStatus.PENDING, nullable=False)
    coach_validated = Column(Boolean, default=False, nullable=False)
    validation_date = Column(DateTime(timezone=True), nullable=True)
    
    plan = relationship("TrainingPlan", back_populates="workouts")
    exercises = relationship("ExerciseDetail", back_populates="workout", cascade="all, delete-orphan")
