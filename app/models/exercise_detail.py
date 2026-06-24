from sqlalchemy import Column, Integer, ForeignKey, String, Float, Text
from sqlalchemy.orm import relationship
from typing import final
from app.database import Base

@final
class ExerciseDetail(Base):
    __tablename__ = "exercise_details"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("daily_workouts.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    sets = Column(Integer, default=0)
    reps = Column(Integer, default=0)
    weight = Column(Float, default=0.0)
    order = Column(Integer, default=0)                                

    workout = relationship("DailyWorkout", back_populates="exercises")
