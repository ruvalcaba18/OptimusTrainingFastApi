from typing import List, Optional, Tuple

from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from app.models.coach import CoachProfile
from app.models.coach_booking import CoachBooking
from app.schemas.coaches import CoachCreate, CoachUpdate, BookingCreate


class CoachService:

                                                                        
    @staticmethod
    def get_by_user_id(db: Session, user_id: int) -> Optional[CoachProfile]:
        return (
            db.query(CoachProfile)
            .filter(CoachProfile.user_id == user_id)
            .first()
        )

    @staticmethod
    def get_by_id(db: Session, coach_id: int) -> Optional[CoachProfile]:
        return (
            db.query(CoachProfile)
            .filter(CoachProfile.id == coach_id)
            .first()
        )

    @staticmethod
    def get_multi(
        db: Session,
        specialty: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[CoachProfile]:
        query = db.query(CoachProfile).filter(CoachProfile.is_active == True)
        if specialty:
            query = query.filter(CoachProfile.specialty == specialty)
        return (
            query.order_by(CoachProfile.avg_rating.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, user_id: int, coach_in: CoachCreate) -> CoachProfile:
        db_coach = CoachProfile(
            user_id=user_id,
            bio=coach_in.bio,
            specialty=coach_in.specialty.value,
            experience_years=coach_in.experience_years,
            certifications=coach_in.certifications,
            hourly_rate=coach_in.hourly_rate,
            currency=coach_in.currency,
            latitude=coach_in.latitude,
            longitude=coach_in.longitude,
            city=coach_in.city,
            state=coach_in.state,
            service_radius_km=coach_in.service_radius_km,
            available_hours=coach_in.available_hours,
        )
        db.add(db_coach)
        db.flush()
        db.refresh(db_coach)
        return db_coach

    @staticmethod
    def update(
        db: Session, db_obj: CoachProfile, coach_in: CoachUpdate
    ) -> CoachProfile:
        update_data = coach_in.model_dump(exclude_unset=True)

        if "specialty" in update_data and update_data["specialty"] is not None:
            update_data["specialty"] = update_data["specialty"].value

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def deactivate(db: Session, db_obj: CoachProfile) -> CoachProfile:
        db_obj.is_active = False
        db_obj.is_available = False
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

                                                                        
    @staticmethod
    def get_nearby(
        db: Session,
        lat: float,
        lng: float,
        radius_km: float = 10.0,
        specialty: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Tuple[CoachProfile, float]]:
        earth_radius_km = 6371.0

        dlat = sa_func.radians(CoachProfile.latitude - lat)
        dlng = sa_func.radians(CoachProfile.longitude - lng)

        a = (
            sa_func.sin(dlat / 2) * sa_func.sin(dlat / 2)
            + sa_func.cos(sa_func.radians(lat))
            * sa_func.cos(sa_func.radians(CoachProfile.latitude))
            * sa_func.sin(dlng / 2)
            * sa_func.sin(dlng / 2)
        )

        distance = earth_radius_km * 2 * sa_func.atan2(
            sa_func.sqrt(a), sa_func.sqrt(1 - a)
        )

        distance_label = distance.label("distance_km")

        query = (
            db.query(CoachProfile, distance_label)
            .filter(CoachProfile.is_active == True)
            .filter(CoachProfile.is_available == True)
            .filter(distance <= radius_km)
        )

        if specialty:
            query = query.filter(CoachProfile.specialty == specialty)

        return (
            query.order_by(distance_label)
            .offset(skip)
            .limit(limit)
            .all()
        )

                                                                       
    @staticmethod
    def get_by_id_for_update(db: Session, coach_id: int) -> Optional[CoachProfile]:
        return (
            db.query(CoachProfile)
            .filter(CoachProfile.id == coach_id)
            .with_for_update()
            .first()
        )

    @staticmethod
    def get_booking_by_id_for_update(
        db: Session, booking_id: int
    ) -> Optional[CoachBooking]:
        return (
            db.query(CoachBooking)
            .filter(CoachBooking.id == booking_id)
            .with_for_update()
            .first()
        )

    @staticmethod
    def create_booking(
        db: Session,
        coach: CoachProfile,
        athlete_id: int,
        booking_in: BookingCreate,
    ) -> CoachBooking:
                                                               
        hours = booking_in.duration_minutes / 60.0
        total_price = round(coach.hourly_rate * hours, 2)

        db_booking = CoachBooking(
            coach_id=booking_in.coach_id,
            athlete_id=athlete_id,
            scheduled_date=booking_in.scheduled_date,
            duration_minutes=booking_in.duration_minutes,
            session_type=booking_in.session_type.value if booking_in.session_type else None,
            location_name=booking_in.location_name,
            latitude=booking_in.latitude,
            longitude=booking_in.longitude,
            total_price=total_price,
            currency=coach.currency,
            athlete_notes=booking_in.athlete_notes,
            status="pending",
        )
        db.add(db_booking)
        db.flush()
        db.refresh(db_booking)
        return db_booking

    @staticmethod
    def get_booking_by_id(db: Session, booking_id: int) -> Optional[CoachBooking]:
        return (
            db.query(CoachBooking)
            .filter(CoachBooking.id == booking_id)
            .first()
        )

    @staticmethod
    def get_bookings_by_athlete(
        db: Session, athlete_id: int, skip: int = 0, limit: int = 50
    ) -> List[CoachBooking]:
        return (
            db.query(CoachBooking)
            .filter(CoachBooking.athlete_id == athlete_id)
            .order_by(CoachBooking.scheduled_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_bookings_by_coach(
        db: Session, coach_id: int, skip: int = 0, limit: int = 50
    ) -> List[CoachBooking]:
        return (
            db.query(CoachBooking)
            .filter(CoachBooking.coach_id == coach_id)
            .order_by(CoachBooking.scheduled_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_booking_status(
        db: Session,
        booking: CoachBooking,
        new_status: str,
        coach_notes: Optional[str] = None,
    ) -> CoachBooking:
        booking.status = new_status
        if coach_notes is not None:
            booking.coach_notes = coach_notes
        db.add(booking)
        db.flush()
        db.refresh(booking)
        return booking

                                                                       
    @staticmethod
    def add_review(
        db: Session,
        booking: CoachBooking,
        rating: float,
        review: Optional[str],
    ) -> CoachBooking:
        booking.athlete_rating = rating
        booking.athlete_review = review
        db.add(booking)
        db.flush()
        db.refresh(booking)
        return booking

    @staticmethod
    def recalculate_coach_rating(db: Session, coach_id: int) -> None:
        result = (
            db.query(
                sa_func.avg(CoachBooking.athlete_rating),
                sa_func.count(CoachBooking.athlete_rating),
            )
            .filter(
                CoachBooking.coach_id == coach_id,
                CoachBooking.athlete_rating.isnot(None),
            )
            .first()
        )

        avg_rating = round(float(result[0]), 2) if result[0] else 0.0
        total_reviews = result[1] or 0

        coach = db.query(CoachProfile).filter(CoachProfile.id == coach_id).first()
        if coach:
            coach.avg_rating = avg_rating
            coach.total_reviews = total_reviews
            db.add(coach)
            db.flush()


coach_service = CoachService()
