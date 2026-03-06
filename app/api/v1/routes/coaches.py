"""
Coach routes for API v1.
Thin layer: validates HTTP input, calls controller, returns response.

Diseño RESTful plano — los IDs siempre van al final del path.
"""
from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.controllers.coaches.coach_controller import coach_controller
from app.schemas.coaches import (
    CoachCreate,
    CoachUpdate,
    CoachResponse,
    CoachNearbyResponse,
    BookingCreate,
    BookingStatusUpdate,
    BookingResponse,
    ReviewCreate,
)

router = APIRouter()


# ━━━━━━━━━━━━━━━━━━━━━━━━━  Profile  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post(
    "/",
    response_model=CoachResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrarse como coach",
)
def register_coach(
    coach_in: CoachCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Registra al usuario autenticado como coach.
    Requiere ubicación (lat/lng) para aparecer en el mapa.
    """
    return coach_controller.register_coach(
        db, coach_in=coach_in, current_user=current_user
    )


@router.get(
    "/",
    response_model=list[CoachResponse],
    summary="Listar coaches",
)
def list_coaches(
    specialty: Optional[str] = Query(None, description="Filtrar por especialidad"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Lista todos los coaches activos, opcionalmente filtrados por especialidad."""
    return coach_controller.list_coaches(
        db, specialty=specialty, skip=skip, limit=limit
    )


@router.get(
    "/nearby",
    response_model=list[CoachNearbyResponse],
    summary="Buscar coaches cercanos",
)
def get_nearby_coaches(
    lat: float = Query(..., ge=-90, le=90, description="Latitud del atleta"),
    lng: float = Query(..., ge=-180, le=180, description="Longitud del atleta"),
    radius_km: float = Query(10.0, gt=0, description="Radio de búsqueda en km"),
    specialty: Optional[str] = Query(None, description="Filtrar por especialidad"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Busca coaches disponibles dentro de un radio en kilómetros
    desde las coordenadas del atleta. Usa fórmula de Haversine.
    Ideal para mostrar en un mapa.
    """
    return coach_controller.get_nearby_coaches(
        db,
        lat=lat,
        lng=lng,
        radius_km=radius_km,
        specialty=specialty,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{coach_id}",
    response_model=CoachResponse,
    summary="Ver perfil de coach",
)
def get_coach(
    coach_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna el perfil completo de un coach."""
    return coach_controller.get_coach(db, coach_id=coach_id)


@router.put(
    "/{coach_id}",
    response_model=CoachResponse,
    summary="Actualizar perfil de coach",
)
def update_coach(
    coach_id: int,
    coach_in: CoachUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Actualiza el perfil del coach. Solo el dueño puede editarlo."""
    return coach_controller.update_coach(
        db, coach_id=coach_id, coach_in=coach_in, current_user=current_user
    )


@router.delete(
    "/{coach_id}",
    response_model=CoachResponse,
    summary="Desactivar perfil de coach",
)
def deactivate_coach(
    coach_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Desactiva el perfil del coach (soft delete). Solo el dueño puede hacerlo."""
    return coach_controller.deactivate_coach(
        db, coach_id=coach_id, current_user=current_user
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━  Bookings  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post(
    "/bookings",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Solicitar sesión con coach",
)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    El atleta solicita una sesión con un coach.
    El coach_id va en el body. El precio se calcula automáticamente.
    """
    return coach_controller.create_booking(
        db, booking_in=booking_in, current_user=current_user
    )


@router.get(
    "/bookings/my-sessions",
    response_model=list[BookingResponse],
    summary="Mis sesiones como atleta",
)
def list_my_bookings(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna las sesiones donde el usuario actúa como atleta."""
    return coach_controller.list_my_bookings(
        db, current_user=current_user, skip=skip, limit=limit
    )


@router.get(
    "/bookings/my-clients",
    response_model=list[BookingResponse],
    summary="Mis clientes como coach",
)
def list_coach_bookings(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna las sesiones donde el usuario actúa como coach."""
    return coach_controller.list_coach_bookings(
        db, current_user=current_user, skip=skip, limit=limit
    )


@router.put(
    "/bookings/{booking_id}",
    response_model=BookingResponse,
    summary="Aceptar/rechazar sesión",
)
def update_booking_status(
    booking_id: int,
    status_in: BookingStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    El coach acepta, rechaza o marca como completada una sesión.
    Solo el coach dueño puede cambiar el estado.
    """
    return coach_controller.update_booking_status(
        db,
        booking_id=booking_id,
        status_in=status_in,
        current_user=current_user,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━  Reviews  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post(
    "/reviews",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Calificar sesión",
)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    El atleta califica una sesión completada (1.0 - 5.0).
    El booking_id va en el body. Solo sesiones con status 'completed'.
    El rating promedio del coach se recalcula automáticamente.
    """
    return coach_controller.create_review(
        db, review_in=review_in, current_user=current_user
    )
