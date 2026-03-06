"""
Schemas para Competition y CompetitionParticipant.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .competition_enums import CompetitionStatus


# ━━━━━━━━━━━━━━━━━━━━━━━━  Competition  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class CompetitionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    sport_type: str = Field(..., min_length=1, max_length=50)
    location_name: str = Field(..., min_length=1, max_length=300)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    start_date: datetime
    end_date: Optional[datetime] = None
    max_participants: Optional[int] = Field(None, gt=0)
    rules: Optional[str] = None
    prize_description: Optional[str] = None
    cover_image_url: Optional[str] = None


class CompetitionCreate(CompetitionBase):
    pass


class CompetitionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    sport_type: Optional[str] = Field(None, min_length=1, max_length=50)
    status: Optional[CompetitionStatus] = None
    location_name: Optional[str] = Field(None, min_length=1, max_length=300)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_participants: Optional[int] = Field(None, gt=0)
    rules: Optional[str] = None
    prize_description: Optional[str] = None
    cover_image_url: Optional[str] = None


class CompetitionResponse(CompetitionBase):
    id: int
    creator_id: int
    status: str
    participant_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ━━━━━━━━━━━━━━━━━━━━━━━━  Participant  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class JoinCompetitionRequest(BaseModel):
    """Payload para inscribirse — idempotente."""
    competition_id: int = Field(..., description="ID de la competencia")


class ScoreUpdateRequest(BaseModel):
    """Payload para actualizar score — idempotente (PUT semántico)."""
    competition_id: int = Field(..., description="ID de la competencia")
    user_id: int = Field(..., description="ID del participante")
    score: float = Field(..., description="Score del participante")


class CompetitionParticipantResponse(BaseModel):
    id: int
    competition_id: int
    user_id: int
    score: Optional[float] = None
    position: Optional[int] = None
    joined_at: datetime

    model_config = {"from_attributes": True}


class RankingResponse(BaseModel):
    """Respuesta del ranking de una competencia."""
    competition_id: int
    participants: list[CompetitionParticipantResponse]
