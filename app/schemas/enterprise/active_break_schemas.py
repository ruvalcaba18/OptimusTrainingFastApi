from datetime import datetime

from pydantic import BaseModel, Field

from .enterprise_enums import BreakCategory, BreakDuration


class ActiveBreakBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    category: BreakCategory
    duration_minutes: BreakDuration
    instructions: str | None = None
    video_url: str | None = None
    image_url: str | None = None


class ActiveBreakCreate(ActiveBreakBase):
    pass


class ActiveBreakUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    category: BreakCategory | None = None
    duration_minutes: BreakDuration | None = None
    instructions: str | None = None
    video_url: str | None = None
    image_url: str | None = None


class ActiveBreakResponse(ActiveBreakBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class ActiveBreakLogCreate(BaseModel):
    session_id: int = Field(..., description="ID de la pausa activa a iniciar")


class ActiveBreakLogResponse(BaseModel):
    id: int
    session_id: int
    user_id: int
    enterprise_id: int | None = None
    started_at: datetime
    completed: bool
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class ActiveBreakStatsResponse(BaseModel):
    total_sessions_started: int
    total_sessions_completed: int
    total_minutes: int
    sessions_by_category: dict[str, int]
