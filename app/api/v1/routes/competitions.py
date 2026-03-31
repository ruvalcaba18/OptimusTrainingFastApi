from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.cache import cache_get, cache_set, cache_delete, make_key
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.controllers.competitions.competition_controller import competition_controller
from app.schemas.competitions import (
    CompetitionCreate,
    CompetitionUpdate,
    CompetitionResponse,
    JoinCompetitionRequest,
    ScoreUpdateRequest,
    CompetitionParticipantResponse,
    RankingResponse,
)

router = APIRouter()

@router.post(
    "/",
    response_model=CompetitionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear competencia",
)
def create_competition(
    comp_in: CompetitionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return competition_controller.create_competition(
        db, comp_in=comp_in, current_user=current_user
    )

@router.get(
    "/",
    response_model=list[CompetitionResponse],
    summary="Listar competencias",
)
def list_competitions(
    sport_type: Optional[str] = Query(None, description="Filtrar por tipo de deporte"),
    comp_status: Optional[str] = Query(None, alias="status", description="Filtrar por estado"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return competition_controller.list_competitions(
        db, sport_type=sport_type, comp_status=comp_status, skip=skip, limit=limit
    )

@router.get(
    "/{competition_id}",
    response_model=CompetitionResponse,
    summary="Detalle de competencia",
)
def get_competition(
    competition_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return competition_controller.get_competition(db, comp_id=competition_id)

@router.put(
    "/{competition_id}",
    response_model=CompetitionResponse,
    summary="Actualizar competencia",
)
def update_competition(
    competition_id: int,
    comp_in: CompetitionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return competition_controller.update_competition(
        db, comp_id=competition_id, comp_in=comp_in, current_user=current_user
    )

@router.post(
    "/participants",
    response_model=CompetitionParticipantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Inscribirse en competencia",
)
def join_competition(
    join_in: JoinCompetitionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return competition_controller.join_competition(
        db, join_in=join_in, current_user=current_user
    )

@router.put(
    "/scores",
    response_model=CompetitionParticipantResponse,
    summary="Actualizar score",
)
async def update_score(
    score_in: ScoreUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    result = competition_controller.update_score(
        db, score_in=score_in, current_user=current_user
    )
    await cache_delete(make_key("ranking", score_in.competition_id))
    return result

@router.get(
    "/ranking",
    response_model=RankingResponse,
    summary="Ver ranking",
)
async def get_ranking(
    competition_id: int = Query(..., description="ID de la competencia"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    cache_key = make_key("ranking", competition_id)
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached
    result = competition_controller.get_ranking(db, competition_id=competition_id)
    await cache_set(cache_key, result.model_dump(), ttl=60)
    return result
