from datetime import datetime

from pydantic import BaseModel, Field

from .event_enums import EventStatus, EventType


class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    event_type: EventType
    location_name: str = Field(..., min_length=1, max_length=300)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    start_date: datetime
    end_date: datetime | None = None
    max_participants: int | None = Field(None, gt=0)
    is_public: bool = True
    cover_image_url: str | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    event_type: EventType | None = None
    status: EventStatus | None = None
    location_name: str | None = Field(None, min_length=1, max_length=300)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    start_date: datetime | None = None
    end_date: datetime | None = None
    max_participants: int | None = Field(None, gt=0)
    is_public: bool | None = None
    cover_image_url: str | None = None


class EventResponse(EventBase):
    id: int
    creator_id: int
    status: str
    participant_count: int = 0
    created_at: datetime
    updated_at: datetime | None = None

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
