from typing import Optional

from sqlalchemy.orm import Session

from app.controllers.coaches.exceptions import (
    BookingNotFoundError,
    CoachAlreadyExistsError,
    CoachNotFoundError,
    CoachUnavailableError,
    SelfBookingError,
    SessionAlreadyReviewedError,
)
from app.core.error_handlers import handle_controller_errors
from app.core.exceptions import ForbiddenError
from app.models import User
from app.schemas.coaches import (
    BookingCreate,
    BookingResponse,
    BookingStatusUpdate,
    CoachCreate,
    CoachNearbyResponse,
    CoachResponse,
    CoachUpdate,
    ReviewCreate,
)
from app.services import coach_service


class CoachController:

    @staticmethod
    @handle_controller_errors
    def register_coach(
        db: Session, coach_in: CoachCreate, current_user: User
    ) -> CoachResponse:
        existing = coach_service.get_by_user_id(db, user_id=current_user.id)
        if existing:
            raise CoachAlreadyExistsError()

        coach = coach_service.create(db, user_id=current_user.id, coach_in=coach_in)
        db.commit()
        return coach

    @staticmethod
    @handle_controller_errors
    def list_coaches(
        db: Session,
        specialty: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[CoachResponse]:
        return coach_service.get_multi(
            db, specialty=specialty, skip=skip, limit=limit
        )

    @staticmethod
    @handle_controller_errors
    def get_coach(db: Session, coach_id: int) -> CoachResponse:
        coach = coach_service.get_by_id(db, coach_id)
        if not coach:
            raise CoachNotFoundError()
        return coach

    @staticmethod
    @handle_controller_errors
    def update_coach(
        db: Session, coach_id: int, coach_in: CoachUpdate, current_user: User
    ) -> CoachResponse:
        coach = coach_service.get_by_id(db, coach_id)
        if not coach:
            raise CoachNotFoundError()
        if coach.user_id != current_user.id:
            raise ForbiddenError("No autorizado para editar este perfil")

        updated = coach_service.update(db, db_obj=coach, coach_in=coach_in)
        db.commit()
        return updated

    @staticmethod
    @handle_controller_errors
    def deactivate_coach(
        db: Session, coach_id: int, current_user: User
    ) -> CoachResponse:
        coach = coach_service.get_by_id(db, coach_id)
        if not coach:
            raise CoachNotFoundError()
        if coach.user_id != current_user.id:
            raise ForbiddenError("No autorizado para desactivar este perfil")

        deactivated = coach_service.deactivate(db, db_obj=coach)
        db.commit()
        return deactivated

    @staticmethod
    @handle_controller_errors
    def get_nearby_coaches(
        db: Session,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        specialty: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[CoachNearbyResponse]:
        results = coach_service.get_nearby(
            db,
            lat=lat,
            lng=lng,
            radius_km=radius_km,
            specialty=specialty,
            skip=skip,
            limit=limit,
        )
        return [
            CoachNearbyResponse(
                coach=CoachResponse.model_validate(coach),
                distance_km=round(distance, 2),
            )
            for coach, distance in results
        ]

    @staticmethod
    @handle_controller_errors
    def create_booking(
        db: Session, booking_in: BookingCreate, current_user: User
    ) -> BookingResponse:
        coach = coach_service.get_by_id_for_update(db, booking_in.coach_id)
        if not coach:
            raise CoachNotFoundError()
        if not coach.is_active or not coach.is_available:
            raise CoachUnavailableError()
        if coach.user_id == current_user.id:
            raise SelfBookingError()

        booking = coach_service.create_booking(
            db, coach=coach, athlete_id=current_user.id, booking_in=booking_in
        )
        db.commit()
        return booking

    @staticmethod
    @handle_controller_errors
    def list_my_bookings(
        db: Session, current_user: User, skip: int = 0, limit: int = 50
    ) -> list[BookingResponse]:
        return coach_service.get_bookings_by_athlete(
            db, athlete_id=current_user.id, skip=skip, limit=limit
        )

    @staticmethod
    @handle_controller_errors
    def list_coach_bookings(
        db: Session, current_user: User, skip: int = 0, limit: int = 50
    ) -> list[BookingResponse]:
        coach = coach_service.get_by_user_id(db, user_id=current_user.id)
        if not coach:
            raise CoachNotFoundError("No tienes un perfil de coach registrado")
        return coach_service.get_bookings_by_coach(
            db, coach_id=coach.id, skip=skip, limit=limit
        )

    @staticmethod
    @handle_controller_errors
    def update_booking_status(
        db: Session,
        booking_id: int,
        status_in: BookingStatusUpdate,
        current_user: User,
    ) -> BookingResponse:
        booking = coach_service.get_booking_by_id_for_update(db, booking_id)
        if not booking:
            raise BookingNotFoundError()

        coach = coach_service.get_by_id(db, booking.coach_id)
        if not coach or coach.user_id != current_user.id:
            raise ForbiddenError("Solo el coach puede cambiar el estado de la reservación")

        updated = coach_service.update_booking_status(
            db,
            booking=booking,
            new_status=status_in.status.value,
            coach_notes=status_in.coach_notes,
        )
        db.commit()
        return updated

    @staticmethod
    @handle_controller_errors
    def create_review(
        db: Session, review_in: ReviewCreate, current_user: User
    ) -> BookingResponse:
        booking = coach_service.get_booking_by_id(db, review_in.booking_id)
        if not booking:
            raise BookingNotFoundError()
        if booking.athlete_id != current_user.id:
            raise ForbiddenError("Solo el atleta puede calificar la sesión")
        if booking.status != "completed":
            raise CoachUnavailableError("Solo puedes calificar sesiones completadas")
        if booking.athlete_rating is not None:
            raise SessionAlreadyReviewedError()

        reviewed = coach_service.add_review(
            db,
            booking=booking,
            rating=review_in.rating,
            review=review_in.review,
        )
        coach_service.recalculate_coach_rating(db, coach_id=booking.coach_id)
        db.commit()
        return reviewed


coach_controller = CoachController()
