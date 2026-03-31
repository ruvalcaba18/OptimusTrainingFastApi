from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .enterprise_enums import BreakCategory, BreakDuration


class ActiveBreakBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: BreakCategory
    duration_minutes: BreakDuration
    instructions: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None


class ActiveBreakCreate(ActiveBreakBase):
    pass


class ActiveBreakUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[BreakCategory] = None
    duration_minutes: Optional[BreakDuration] = None
    instructions: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None


class ActiveBreakResponse(ActiveBreakBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ActiveBreakLogCreate(BaseModel):
    session_id: int = Field(..., description="ID de la pausa activa a iniciar")


class ActiveBreakLogResponse(BaseModel):
    id: int
    session_id: int
    user_id: int
    enterprise_id: Optional[int] = None
    started_at: datetime
    completed: bool
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ActiveBreakStatsResponse(BaseModel):
    total_sessions_started: int
    total_sessions_completed: int
    total_minutes: int
    sessions_by_category: dict[str, int]
