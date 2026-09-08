from datetime import datetime

from pydantic import BaseModel, Field

from .competition_enums import CompetitionStatus


class CompetitionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    sport_type: str = Field(..., min_length=1, max_length=50)
    location_name: str = Field(..., min_length=1, max_length=300)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    start_date: datetime
    end_date: datetime | None = None
    max_participants: int | None = Field(None, gt=0)
    rules: str | None = None
    prize_description: str | None = None
    cover_image_url: str | None = None


class CompetitionCreate(CompetitionBase):
    pass


class CompetitionUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    sport_type: str | None = Field(None, min_length=1, max_length=50)
    status: CompetitionStatus | None = None
    location_name: str | None = Field(None, min_length=1, max_length=300)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    start_date: datetime | None = None
    end_date: datetime | None = None
    max_participants: int | None = Field(None, gt=0)
    rules: str | None = None
    prize_description: str | None = None
    cover_image_url: str | None = None


class CompetitionResponse(CompetitionBase):
    id: int
    creator_id: int
    status: str
    participant_count: int = 0
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class JoinCompetitionRequest(BaseModel):
    competition_id: int = Field(..., description="ID de la competencia")


class ScoreUpdateRequest(BaseModel):
    competition_id: int = Field(..., description="ID de la competencia")
    user_id: int = Field(..., description="ID del participante")
    score: float = Field(..., description="Score del participante")


class CompetitionParticipantResponse(BaseModel):
    id: int
    competition_id: int
    user_id: int
    score: float | None = None
    position: int | None = None
    joined_at: datetime

    model_config = {"from_attributes": True}


class RankingResponse(BaseModel):
    competition_id: int
    participants: list[CompetitionParticipantResponse]
