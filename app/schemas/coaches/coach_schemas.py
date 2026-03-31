from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .coach_enums import CoachSpecialty

class CoachBase(BaseModel):
    bio: Optional[str] = None
    specialty: CoachSpecialty
    experience_years: int = Field(..., ge=0)
    certifications: Optional[str] = None
    hourly_rate: float = Field(..., gt=0)
    currency: str = Field(default="MXN", max_length=10)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    city: Optional[str] = None
    state: Optional[str] = None
    service_radius_km: float = Field(default=10.0, gt=0)
    available_hours: Optional[str] = None               
    is_searchable: bool = True

class CoachCreate(CoachBase):
    pass


class CoachUpdate(BaseModel):
    bio: Optional[str] = None
    specialty: Optional[CoachSpecialty] = None
    experience_years: Optional[int] = Field(None, ge=0)
    certifications: Optional[str] = None
    hourly_rate: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, max_length=10)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    city: Optional[str] = None
    state: Optional[str] = None
    service_radius_km: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None
    available_hours: Optional[str] = None
    is_searchable: Optional[bool] = None


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
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CoachNearbyResponse(BaseModel):
    coach: CoachResponse
    distance_km: float
