"""
Event service — data-access layer con ACID.

ACID guarantees:
  - Atomicity: flush() sin commit (commit en controller).
  - Consistency: UniqueConstraint + validación de capacidad pre-insert.
  - Isolation: with_for_update() en join/leave para evitar race conditions.
  - Idempotency: verificación de estado antes de cada mutación.
"""
from typing import List, Optional

from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from app.models.event import Event, EventParticipant
from app.schemas.events import EventCreate, EventUpdate


class EventService:

    # ━━━━━━━━━━━━━━━━━━━━━━━━━  Event CRUD  ━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def create(db: Session, creator_id: int, event_in: EventCreate) -> Event:
        db_event = Event(
            creator_id=creator_id,
            title=event_in.title,
            description=event_in.description,
            event_type=event_in.event_type.value,
            status="published",
            location_name=event_in.location_name,
            latitude=event_in.latitude,
            longitude=event_in.longitude,
            start_date=event_in.start_date,
            end_date=event_in.end_date,
            max_participants=event_in.max_participants,
            is_public=event_in.is_public,
            cover_image_url=event_in.cover_image_url,
        )
        db.add(db_event)
        db.flush()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def get_by_id(db: Session, event_id: int) -> Optional[Event]:
        return db.query(Event).filter(Event.id == event_id).first()

    @staticmethod
    def get_by_id_for_update(db: Session, event_id: int) -> Optional[Event]:
        """Row-level lock — bloquea el evento durante la transacción."""
        return (
            db.query(Event)
            .filter(Event.id == event_id)
            .with_for_update()
            .first()
        )

    @staticmethod
    def get_multi(
        db: Session,
        event_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Event]:
        query = db.query(Event).filter(Event.is_public == True)
        if event_type:
            query = query.filter(Event.event_type == event_type)
        if status:
            query = query.filter(Event.status == status)
        return (
            query.order_by(Event.start_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(db: Session, db_obj: Event, event_in: EventUpdate) -> Event:
        update_data = event_in.model_dump(exclude_unset=True)

        if "event_type" in update_data and update_data["event_type"] is not None:
            update_data["event_type"] = update_data["event_type"].value
        if "status" in update_data and update_data["status"] is not None:
            update_data["status"] = update_data["status"].value

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def cancel(db: Session, db_obj: Event) -> Event:
        db_obj.status = "cancelled"
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    # ━━━━━━━━━━━━━━━━━━━━━  Participants (ACID)  ━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def get_participant(
        db: Session, event_id: int, user_id: int
    ) -> Optional[EventParticipant]:
        return (
            db.query(EventParticipant)
            .filter(
                EventParticipant.event_id == event_id,
                EventParticipant.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def count_participants(db: Session, event_id: int) -> int:
        return (
            db.query(sa_func.count(EventParticipant.id))
            .filter(EventParticipant.event_id == event_id)
            .scalar()
        )

    @staticmethod
    def add_participant(
        db: Session, event_id: int, user_id: int
    ) -> EventParticipant:
        participant = EventParticipant(
            event_id=event_id,
            user_id=user_id,
        )
        db.add(participant)
        db.flush()
        db.refresh(participant)
        return participant

    @staticmethod
    def remove_participant(
        db: Session, event_id: int, user_id: int
    ) -> Optional[EventParticipant]:
        participant = (
            db.query(EventParticipant)
            .filter(
                EventParticipant.event_id == event_id,
                EventParticipant.user_id == user_id,
            )
            .first()
        )
        if participant:
            db.delete(participant)
            db.flush()
        return participant

    @staticmethod
    def get_participants(
        db: Session, event_id: int, skip: int = 0, limit: int = 100
    ) -> List[EventParticipant]:
        return (
            db.query(EventParticipant)
            .filter(EventParticipant.event_id == event_id)
            .order_by(EventParticipant.joined_at)
            .offset(skip)
            .limit(limit)
            .all()
        )


event_service = EventService()
