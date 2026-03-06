"""
Competition routes for API v1.
Thin layer: validates HTTP input, calls controller, returns response.

Diseño RESTful plano — IDs solo al final del path.
"""
from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

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


# ━━━━━━━━━━━━━━━━━━━━━━━  Competitions  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


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
    """Crea una nueva competencia deportiva. Requiere autenticación."""
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
    """Lista competencias con filtros opcionales."""
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
    """Retorna el detalle de una competencia."""
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
    """Actualiza una competencia. Solo el creador puede editarla."""
    return competition_controller.update_competition(
        db, comp_id=competition_id, comp_in=comp_in, current_user=current_user
    )


# ━━━━━━━━━━━━━━━━━━━━━  Participants  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


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
    """
    Inscribirse en una competencia. El competition_id va en el body.
    ACID: usa row-level lock para validar capacidad.
    Idempotente: retorna 409 si ya estás inscrito.
    """
    return competition_controller.join_competition(
        db, join_in=join_in, current_user=current_user
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━  Scores  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.put(
    "/scores",
    response_model=CompetitionParticipantResponse,
    summary="Actualizar score",
)
def update_score(
    score_in: ScoreUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Actualiza el score de un participante. Solo el creador de la competencia.
    ACID: row-level lock en el participante. Idempotente (PUT semántico).
    Las posiciones se recalculan automáticamente.
    """
    return competition_controller.update_score(
        db, score_in=score_in, current_user=current_user
    )


# ━━━━━━━━━━━━━━━━━━━━━━━  Ranking  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.get(
    "/ranking",
    response_model=RankingResponse,
    summary="Ver ranking",
)
def get_ranking(
    competition_id: int = Query(..., description="ID de la competencia"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna el ranking de una competencia ordenado por posición."""
    return competition_controller.get_ranking(db, competition_id=competition_id)
