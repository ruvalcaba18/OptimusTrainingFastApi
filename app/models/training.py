from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class PlanStatus(enum.Enum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"


class WorkoutStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class CoachAthlete(Base):
    __tablename__ = "coach_athletes"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("coach_profiles.id", ondelete="CASCADE"), nullable=False)
    athlete_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    coach = relationship("CoachProfile", backref="athletes_relation")
    athlete = relationship("User", backref="coach_relation")


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
