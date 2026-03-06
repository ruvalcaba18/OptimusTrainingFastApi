"""
Schemas para CoachBooking y reviews.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .coach_enums import BookingStatus, SessionType


# ━━━━━━━━━━━━━━━━━━━━━━━━━  Coach Booking  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class BookingCreate(BaseModel):
    """Payload para solicitar una sesión con un coach."""
    coach_id: int = Field(..., description="ID del perfil de coach")
    scheduled_date: datetime
    duration_minutes: int = Field(..., gt=0, description="Duración en minutos")
    session_type: Optional[SessionType] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    athlete_notes: Optional[str] = None


class BookingStatusUpdate(BaseModel):
    """Payload para que el coach acepte/rechace una solicitud."""
    status: BookingStatus
    coach_notes: Optional[str] = None


class BookingResponse(BaseModel):
    id: int
    coach_id: int
    athlete_id: int
    scheduled_date: datetime
    duration_minutes: int
    session_type: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: str
    total_price: float
    currency: str
    athlete_notes: Optional[str] = None
    coach_notes: Optional[str] = None
    athlete_rating: Optional[float] = None
    athlete_review: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━  Review  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class ReviewCreate(BaseModel):
    """Payload para que el atleta califique una sesión completada."""
    booking_id: int = Field(..., description="ID de la reservación a calificar")
    rating: float = Field(..., ge=1.0, le=5.0, description="Calificación 1.0 - 5.0")
    review: Optional[str] = None
