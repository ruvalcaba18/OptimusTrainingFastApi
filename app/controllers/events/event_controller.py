from typing import Optional

from sqlalchemy.orm import Session

from app.controllers.events.exceptions import (
    AlreadyJoinedEventError,
    EventCancelledError,
    EventFullError,
    EventNotFoundError,
    NotJoinedEventError,
)
from app.core.error_handlers import handle_controller_errors
from app.core.exceptions import ForbiddenError
from app.models import User
from app.schemas.events import (
    EventCreate,
    EventParticipantResponse,
    EventResponse,
    EventUpdate,
    JoinEventRequest,
    LeaveEventRequest,
)
from app.services import event_service


class EventController:

    @staticmethod
    @handle_controller_errors
    def create_event(
        db: Session, event_in: EventCreate, current_user: User
    ) -> EventResponse:
        event = event_service.create(
            db, creator_id=current_user.id, event_in=event_in
        )
        db.commit()
        count = event_service.count_participants(db, event.id)
        response = EventResponse.model_validate(event)
        response.participant_count = count
        return response

    @staticmethod
    @handle_controller_errors
    def list_events(
        db: Session,
        event_type: Optional[str] = None,
        event_status: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[EventResponse]:
        events = event_service.get_multi(
            db, event_type=event_type, status=event_status, skip=skip, limit=limit
        )
        results = []
        for ev in events:
            count = event_service.count_participants(db, ev.id)
            resp = EventResponse.model_validate(ev)
            resp.participant_count = count
            results.append(resp)
        return results

    @staticmethod
    @handle_controller_errors
    def get_event(db: Session, event_id: int) -> EventResponse:
        event = event_service.get_by_id(db, event_id)
        if not event:
            raise EventNotFoundError()
        count = event_service.count_participants(db, event.id)
        resp = EventResponse.model_validate(event)
        resp.participant_count = count
        return resp

    @staticmethod
    @handle_controller_errors
    def update_event(
        db: Session, event_id: int, event_in: EventUpdate, current_user: User
    ) -> EventResponse:
        event = event_service.get_by_id(db, event_id)
        if not event:
            raise EventNotFoundError()
        if event.creator_id != current_user.id:
            raise ForbiddenError("Solo el creador puede editar este evento")

        updated = event_service.update(db, db_obj=event, event_in=event_in)
        db.commit()
        count = event_service.count_participants(db, updated.id)
        resp = EventResponse.model_validate(updated)
        resp.participant_count = count
        return resp

    @staticmethod
    @handle_controller_errors
    def cancel_event(
        db: Session, event_id: int, current_user: User
    ) -> EventResponse:
        event = event_service.get_by_id(db, event_id)
        if not event:
            raise EventNotFoundError()
        if event.creator_id != current_user.id:
            raise ForbiddenError("Solo el creador puede cancelar este evento")
        if event.status == "cancelled":
            raise EventCancelledError("Este evento ya está cancelado")

        cancelled = event_service.cancel(db, db_obj=event)
        db.commit()
        count = event_service.count_participants(db, cancelled.id)
        resp = EventResponse.model_validate(cancelled)
        resp.participant_count = count
        return resp

    @staticmethod
    @handle_controller_errors
    def join_event(
        db: Session, join_in: JoinEventRequest, current_user: User
    ) -> EventParticipantResponse:
        event = event_service.get_by_id_for_update(db, join_in.event_id)
        if not event:
            raise EventNotFoundError()
        if event.status == "cancelled":
            raise EventCancelledError()

        existing = event_service.get_participant(
            db, event_id=join_in.event_id, user_id=current_user.id
        )
        if existing:
            raise AlreadyJoinedEventError()

        if event.max_participants is not None:
            current_count = event_service.count_participants(db, event.id)
            if current_count >= event.max_participants:
                raise EventFullError()

        participant = event_service.add_participant(
            db, event_id=join_in.event_id, user_id=current_user.id
        )
        db.commit()
        return participant

    @staticmethod
    @handle_controller_errors
    def leave_event(
        db: Session, leave_in: LeaveEventRequest, current_user: User
    ) -> dict:
        event = event_service.get_by_id(db, leave_in.event_id)
        if not event:
            raise EventNotFoundError()

        existing = event_service.get_participant(
            db, event_id=leave_in.event_id, user_id=current_user.id
        )
        if not existing:
            raise NotJoinedEventError()

        event_service.remove_participant(
            db, event_id=leave_in.event_id, user_id=current_user.id
        )
        db.commit()
        return {"message": "Has salido del evento exitosamente", "success": True}

    @staticmethod
    @handle_controller_errors
    def list_participants(
        db: Session, event_id: int, skip: int = 0, limit: int = 100
    ) -> list[EventParticipantResponse]:
        event = event_service.get_by_id(db, event_id)
        if not event:
            raise EventNotFoundError()
        return event_service.get_participants(
            db, event_id=event_id, skip=skip, limit=limit
        )


event_controller = EventController()
