from datetime import datetime

from pydantic import BaseModel, Field

from .coach_enums import BookingStatus, SessionType


class BookingCreate(BaseModel):
    coach_id: int = Field(..., description="ID del perfil de coach")
    scheduled_date: datetime
    duration_minutes: int = Field(..., gt=0, description="Duración en minutos")
    session_type: SessionType | None = None
    location_name: str | None = None
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    athlete_notes: str | None = None

class BookingStatusUpdate(BaseModel):
    status: BookingStatus
    coach_notes: str | None = None

class BookingResponse(BaseModel):
    id: int
    coach_id: int
    athlete_id: int
    scheduled_date: datetime
    duration_minutes: int
    session_type: str | None = None
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    status: str
    total_price: float
    currency: str
    athlete_notes: str | None = None
    coach_notes: str | None = None
    athlete_rating: float | None = None
    athlete_review: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}

class ReviewCreate(BaseModel):
    booking_id: int = Field(..., description="ID de la reservación a calificar")
    rating: float = Field(..., ge=1.0, le=5.0, description="Calificación 1.0 - 5.0")
    review: str | None = None