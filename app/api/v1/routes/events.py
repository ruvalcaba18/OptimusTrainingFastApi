"""
Event routes for API v1.
Thin layer: validates HTTP input, calls controller, returns response.

Diseño RESTful plano — IDs solo al final del path.
"""
from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.controllers.events.event_controller import event_controller
from app.schemas.events import (
    EventCreate,
    EventUpdate,
    EventResponse,
    JoinEventRequest,
    LeaveEventRequest,
    EventParticipantResponse,
)
from app.schemas.common.response import MessageResponse

router = APIRouter()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━  Events  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear evento",
)
def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Crea un nuevo evento deportivo. Requiere autenticación."""
    return event_controller.create_event(
        db, event_in=event_in, current_user=current_user
    )


@router.get(
    "/",
    response_model=list[EventResponse],
    summary="Listar eventos",
)
def list_events(
    event_type: Optional[str] = Query(None, description="Filtrar por tipo de evento"),
    event_status: Optional[str] = Query(None, alias="status", description="Filtrar por estado"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Lista eventos públicos con filtros opcionales."""
    return event_controller.list_events(
        db, event_type=event_type, event_status=event_status, skip=skip, limit=limit
    )


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Detalle de evento",
)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna el detalle de un evento con el conteo de participantes."""
    return event_controller.get_event(db, event_id=event_id)


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    summary="Actualizar evento",
)
def update_event(
    event_id: int,
    event_in: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Actualiza un evento. Solo el creador puede editarlo."""
    return event_controller.update_event(
        db, event_id=event_id, event_in=event_in, current_user=current_user
    )


@router.delete(
    "/{event_id}",
    response_model=EventResponse,
    summary="Cancelar evento",
)
def cancel_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Cancela un evento (soft cancel). Solo el creador puede hacerlo."""
    return event_controller.cancel_event(
        db, event_id=event_id, current_user=current_user
    )


# ━━━━━━━━━━━━━━━━━━━━━━  Participants  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post(
    "/participants",
    response_model=EventParticipantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Unirse a evento",
)
def join_event(
    join_in: JoinEventRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Unirse a un evento. El event_id va en el body.
    ACID: usa row-level lock para validar capacidad.
    Idempotente: retorna 409 si ya estás inscrito.
    """
    return event_controller.join_event(
        db, join_in=join_in, current_user=current_user
    )


@router.delete(
    "/participants",
    response_model=MessageResponse,
    summary="Salir de evento",
)
def leave_event(
    leave_in: LeaveEventRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Salir de un evento. El event_id va en el body."""
    return event_controller.leave_event(
        db, leave_in=leave_in, current_user=current_user
    )


@router.get(
    "/participants/list",
    response_model=list[EventParticipantResponse],
    summary="Listar participantes",
)
def list_participants(
    event_id: int = Query(..., description="ID del evento"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna los participantes de un evento. El event_id va como query param."""
    return event_controller.list_participants(
        db, event_id=event_id, skip=skip, limit=limit
    )
