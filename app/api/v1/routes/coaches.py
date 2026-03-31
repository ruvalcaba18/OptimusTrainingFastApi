from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.cache import cache_get, cache_set, cache_delete_pattern, make_key
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
    return coach_controller.list_coaches(
        db, specialty=specialty, skip=skip, limit=limit
    )


@router.get(
    "/nearby",
    response_model=list[CoachNearbyResponse],
    summary="Buscar coaches cercanos",
)
async def get_nearby_coaches(
    lat: float = Query(..., ge=-90, le=90, description="Latitud del atleta"),
    lng: float = Query(..., ge=-180, le=180, description="Longitud del atleta"),
    radius_km: float = Query(10.0, gt=0, description="Radio de búsqueda en km"),
    specialty: Optional[str] = Query(None, description="Filtrar por especialidad"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    cache_key = make_key(
        "coaches", "nearby",
        round(lat, 2), round(lng, 2),
        radius_km, specialty, skip, limit,
    )
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached
    result = coach_controller.get_nearby_coaches(
        db, lat=lat, lng=lng, radius_km=radius_km,
        specialty=specialty, skip=skip, limit=limit,
    )
    serialized = [r.model_dump() for r in result]
    await cache_set(cache_key, serialized, ttl=180)
    return result


@router.get(
    "/{coach_id}",
    response_model=CoachResponse,
    summary="Ver perfil de coach",
)
async def get_coach(
    coach_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    cache_key = make_key("coach", "profile", coach_id)
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached
    result = coach_controller.get_coach(db, coach_id=coach_id)
    await cache_set(cache_key, result.model_dump(), ttl=300)
    return result


@router.put(
    "/{coach_id}",
    response_model=CoachResponse,
    summary="Actualizar perfil de coach",
)
async def update_coach(
    coach_id: int,
    coach_in: CoachUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    result = coach_controller.update_coach(
        db, coach_id=coach_id, coach_in=coach_in, current_user=current_user
    )
    await cache_delete_pattern(f"coach:profile:{coach_id}")
    await cache_delete_pattern("coaches:nearby:*")
    return result


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
    return coach_controller.deactivate_coach(
        db, coach_id=coach_id, current_user=current_user
    )


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
    return coach_controller.update_booking_status(
        db,
        booking_id=booking_id,
        status_in=status_in,
        current_user=current_user,
    )


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
    return coach_controller.create_review(
        db, review_in=review_in, current_user=current_user
    )
