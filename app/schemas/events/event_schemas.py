from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .event_enums import EventType, EventStatus


class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    event_type: EventType
    location_name: str = Field(..., min_length=1, max_length=300)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    start_date: datetime
    end_date: Optional[datetime] = None
    max_participants: Optional[int] = Field(None, gt=0)
    is_public: bool = True
    cover_image_url: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    event_type: Optional[EventType] = None
    status: Optional[EventStatus] = None
    location_name: Optional[str] = Field(None, min_length=1, max_length=300)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_participants: Optional[int] = Field(None, gt=0)
    is_public: Optional[bool] = None
    cover_image_url: Optional[str] = None


class EventResponse(EventBase):
    id: int
    creator_id: int
    status: str
    participant_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class JoinEventRequest(BaseModel):
    event_id: int = Field(..., description="ID del evento")


class LeaveEventRequest(BaseModel):
    event_id: int = Field(..., description="ID del evento")


class EventParticipantResponse(BaseModel):
    id: int
    event_id: int
    user_id: int
    joined_at: datetime

    model_config = {"from_attributes": True}
