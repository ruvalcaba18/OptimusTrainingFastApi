from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.coach_service import coach_service
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


class CoachController:

                                                                       
    @staticmethod
    def register_coach(
        db: Session, coach_in: CoachCreate, current_user: User
    ) -> CoachResponse:
        existing = coach_service.get_by_user_id(db, user_id=current_user.id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya tienes un perfil de coach registrado.",
            )

        try:
            coach = coach_service.create(db, user_id=current_user.id, coach_in=coach_in)
            db.commit()
            return coach
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al registrar coach: {str(e)}",
            )

    @staticmethod
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
    def get_coach(db: Session, coach_id: int) -> CoachResponse:
        coach = coach_service.get_by_id(db, coach_id)
        if not coach:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coach no encontrado",
            )
        return coach

    @staticmethod
    def update_coach(
        db: Session, coach_id: int, coach_in: CoachUpdate, current_user: User
    ) -> CoachResponse:
        coach = coach_service.get_by_id(db, coach_id)
        if not coach:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coach no encontrado",
            )
        if coach.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No autorizado para editar este perfil",
            )

        try:
            updated = coach_service.update(db, db_obj=coach, coach_in=coach_in)
            db.commit()
            return updated
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar coach: {str(e)}",
            )

    @staticmethod
    def deactivate_coach(
        db: Session, coach_id: int, current_user: User
    ) -> CoachResponse:
        coach = coach_service.get_by_id(db, coach_id)
        if not coach:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coach no encontrado",
            )
        if coach.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No autorizado para desactivar este perfil",
            )

        try:
            deactivated = coach_service.deactivate(db, db_obj=coach)
            db.commit()
            return deactivated
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al desactivar coach: {str(e)}",
            )

                                                                       
    @staticmethod
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
    def create_booking(
        db: Session, booking_in: BookingCreate, current_user: User
    ) -> BookingResponse:
                                                                               
        coach = coach_service.get_by_id_for_update(db, booking_in.coach_id)
        if not coach:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coach no encontrado",
            )
        if not coach.is_active or not coach.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este coach no está disponible actualmente",
            )
        if coach.user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes contratarte a ti mismo",
            )

        try:
            booking = coach_service.create_booking(
                db, coach=coach, athlete_id=current_user.id, booking_in=booking_in
            )
            db.commit()
            return booking
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear reservación: {str(e)}",
            )

    @staticmethod
    def list_my_bookings(
        db: Session, current_user: User, skip: int = 0, limit: int = 50
    ) -> list[BookingResponse]:
        return coach_service.get_bookings_by_athlete(
            db, athlete_id=current_user.id, skip=skip, limit=limit
        )

    @staticmethod
    def list_coach_bookings(
        db: Session, current_user: User, skip: int = 0, limit: int = 50
    ) -> list[BookingResponse]:
        coach = coach_service.get_by_user_id(db, user_id=current_user.id)
        if not coach:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No tienes un perfil de coach registrado",
            )
        return coach_service.get_bookings_by_coach(
            db, coach_id=coach.id, skip=skip, limit=limit
        )

    @staticmethod
    def update_booking_status(
        db: Session,
        booking_id: int,
        status_in: BookingStatusUpdate,
        current_user: User,
    ) -> BookingResponse:
                                                                         
        booking = coach_service.get_booking_by_id_for_update(db, booking_id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservación no encontrada",
            )

                                                     
        coach = coach_service.get_by_id(db, booking.coach_id)
        if not coach or coach.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el coach puede cambiar el estado de la reservación",
            )

        try:
            updated = coach_service.update_booking_status(
                db,
                booking=booking,
                new_status=status_in.status.value,
                coach_notes=status_in.coach_notes,
            )
            db.commit()
            return updated
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar reservación: {str(e)}",
            )

                                                                       
    @staticmethod
    def create_review(
        db: Session, review_in: ReviewCreate, current_user: User
    ) -> BookingResponse:
        booking = coach_service.get_booking_by_id(db, review_in.booking_id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservación no encontrada",
            )
        if booking.athlete_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el atleta puede calificar la sesión",
            )
        if booking.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo puedes calificar sesiones completadas",
            )
        if booking.athlete_rating is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya calificaste esta sesión",
            )

        try:
            reviewed = coach_service.add_review(
                db,
                booking=booking,
                rating=review_in.rating,
                review=review_in.review,
            )
                                                  
            coach_service.recalculate_coach_rating(db, coach_id=booking.coach_id)
            db.commit()
            return reviewed
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al calificar sesión: {str(e)}",
            )


coach_controller = CoachController()
