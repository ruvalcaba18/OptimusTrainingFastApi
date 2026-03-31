from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class PlanStatus(str, Enum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"


class WorkoutStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class ExerciseDetailBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    sets: int = Field(0, ge=0)
    reps: int = Field(0, ge=0)
    weight: float = Field(0.0, ge=0)
    order: int = Field(0, ge=0)


class ExerciseDetailCreate(ExerciseDetailBase):
    pass


class ExerciseDetailResponse(ExerciseDetailBase):
    id: int
    workout_id: int

    model_config = {"from_attributes": True}


class DailyWorkoutBase(BaseModel):
    date: date
    status: WorkoutStatus = WorkoutStatus.PENDING
    coach_validated: bool = False


class DailyWorkoutCreate(DailyWorkoutBase):
    exercises: List[ExerciseDetailCreate] = Field(..., max_items=8)


class DailyWorkoutUpdate(BaseModel):
    status: Optional[WorkoutStatus] = None
    coach_validated: Optional[bool] = None
    exercises: Optional[List[ExerciseDetailCreate]] = Field(None, max_items=8)


class DailyWorkoutResponse(DailyWorkoutBase):
    id: int
    plan_id: int
    validation_date: Optional[datetime] = None
    exercises: List[ExerciseDetailResponse]

    model_config = {"from_attributes": True}


class TrainingPlanBase(BaseModel):
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2024)
    status: PlanStatus = PlanStatus.DRAFT


class TrainingPlanCreate(TrainingPlanBase):
    athlete_id: int


class TrainingPlanUpdate(BaseModel):
    status: Optional[PlanStatus] = None


class TrainingPlanResponse(TrainingPlanBase):
    id: int
    coach_id: int
    athlete_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    workouts: List[DailyWorkoutResponse]

    model_config = {"from_attributes": True}


class CoachAthleteResponse(BaseModel):
    id: int
    coach_id: int
    athlete_id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
