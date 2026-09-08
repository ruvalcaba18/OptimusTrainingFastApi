from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


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
    description: str | None = None
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
    exercises: list[ExerciseDetailCreate] = Field(..., max_length=8)


class DailyWorkoutUpdate(BaseModel):
    status: WorkoutStatus | None = None
    coach_validated: bool | None = None
    exercises: list[ExerciseDetailCreate] | None = Field(None, max_length=8)


class DailyWorkoutResponse(DailyWorkoutBase):
    id: int
    plan_id: int
    validation_date: datetime | None = None
    exercises: list[ExerciseDetailResponse]

    model_config = {"from_attributes": True}


class TrainingPlanBase(BaseModel):
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2024)
    status: PlanStatus = PlanStatus.DRAFT


class TrainingPlanCreate(TrainingPlanBase):
    athlete_id: int


class TrainingPlanUpdate(BaseModel):
    status: PlanStatus | None = None


class TrainingPlanResponse(TrainingPlanBase):
    id: int
    coach_id: int
    athlete_id: int
    created_at: datetime
    updated_at: datetime | None = None
    workouts: list[DailyWorkoutResponse]

    model_config = {"from_attributes": True}


class CoachAthleteResponse(BaseModel):
    id: int
    coach_id: int
    athlete_id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
