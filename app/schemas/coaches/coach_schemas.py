from datetime import datetime

from pydantic import BaseModel, Field

from .coach_enums import CoachSpecialty


class CoachBase(BaseModel):
    bio: str | None = None
    specialty: CoachSpecialty
    experience_years: int = Field(..., ge=0)
    certifications: str | None = None
    hourly_rate: float = Field(..., gt=0)
    currency: str = Field(default="MXN", max_length=10)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    city: str | None = None
    state: str | None = None
    service_radius_km: float = Field(default=10.0, gt=0)
    available_hours: str | None = None               
    is_searchable: bool = True

class CoachCreate(CoachBase):
    pass


class CoachUpdate(BaseModel):
    bio: str | None = None
    specialty: CoachSpecialty | None = None
    experience_years: int | None = Field(None, ge=0)
    certifications: str | None = None
    hourly_rate: float | None = Field(None, gt=0)
    currency: str | None = Field(None, max_length=10)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    city: str | None = None
    state: str | None = None
    service_radius_km: float | None = Field(None, gt=0)
    is_available: bool | None = None
    available_hours: str | None = None
    is_searchable: bool | None = None


class CoachResponse(CoachBase):
    id: int
    user_id: int
    is_available: bool
    avg_rating: float
    total_reviews: int
    is_verified: bool
    is_active: bool
    is_searchable: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class CoachNearbyResponse(BaseModel):
    coach: CoachResponse
    distance_km: float
