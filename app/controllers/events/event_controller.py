from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.event_service import event_service
from app.schemas.events import (
    EventCreate,
    EventUpdate,
    EventResponse,
    JoinEventRequest,
    LeaveEventRequest,
    EventParticipantResponse,
)


class EventController:

                                                                       
    @staticmethod
    def create_event(
        db: Session, event_in: EventCreate, current_user: User
    ) -> EventResponse:
        try:
            event = event_service.create(
                db, creator_id=current_user.id, event_in=event_in
            )
            db.commit()
            count = event_service.count_participants(db, event.id)
            response = EventResponse.model_validate(event)
            response.participant_count = count
            return response
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear evento: {str(e)}",
            )

    @staticmethod
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
    def get_event(db: Session, event_id: int) -> EventResponse:
        event = event_service.get_by_id(db, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado",
            )
        count = event_service.count_participants(db, event.id)
        resp = EventResponse.model_validate(event)
        resp.participant_count = count
        return resp

    @staticmethod
    def update_event(
        db: Session, event_id: int, event_in: EventUpdate, current_user: User
    ) -> EventResponse:
        event = event_service.get_by_id(db, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado",
            )
        if event.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el creador puede editar este evento",
            )

        try:
            updated = event_service.update(db, db_obj=event, event_in=event_in)
            db.commit()
            count = event_service.count_participants(db, updated.id)
            resp = EventResponse.model_validate(updated)
            resp.participant_count = count
            return resp
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar evento: {str(e)}",
            )

    @staticmethod
    def cancel_event(
        db: Session, event_id: int, current_user: User
    ) -> EventResponse:
        event = event_service.get_by_id(db, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado",
            )
        if event.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el creador puede cancelar este evento",
            )
        if event.status == "cancelled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este evento ya está cancelado",
            )

        try:
            cancelled = event_service.cancel(db, db_obj=event)
            db.commit()
            count = event_service.count_participants(db, cancelled.id)
            resp = EventResponse.model_validate(cancelled)
            resp.participant_count = count
            return resp
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al cancelar evento: {str(e)}",
            )

                                                                       
    @staticmethod
    def join_event(
        db: Session, join_in: JoinEventRequest, current_user: User
    ) -> EventParticipantResponse:
                           
        event = event_service.get_by_id_for_update(db, join_in.event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado",
            )
        if event.status == "cancelled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes unirte a un evento cancelado",
            )

                              
        existing = event_service.get_participant(
            db, event_id=join_in.event_id, user_id=current_user.id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya estás inscrito en este evento",
            )

                                
        if event.max_participants is not None:
            current_count = event_service.count_participants(db, event.id)
            if current_count >= event.max_participants:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El evento ha alcanzado el máximo de participantes",
                )

                
        try:
            participant = event_service.add_participant(
                db, event_id=join_in.event_id, user_id=current_user.id
            )
            db.commit()
            return participant
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al unirse al evento: {str(e)}",
            )

    @staticmethod
    def leave_event(
        db: Session, leave_in: LeaveEventRequest, current_user: User
    ) -> dict:
        event = event_service.get_by_id(db, leave_in.event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado",
            )

                                             
        existing = event_service.get_participant(
            db, event_id=leave_in.event_id, user_id=current_user.id
        )
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No estás inscrito en este evento",
            )

        try:
            event_service.remove_participant(
                db, event_id=leave_in.event_id, user_id=current_user.id
            )
            db.commit()
            return {"message": "Has salido del evento exitosamente", "success": True}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al salir del evento: {str(e)}",
            )

    @staticmethod
    def list_participants(
        db: Session, event_id: int, skip: int = 0, limit: int = 100
    ) -> list[EventParticipantResponse]:
        event = event_service.get_by_id(db, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado",
            )
        return event_service.get_participants(
            db, event_id=event_id, skip=skip, limit=limit
        )


event_controller = EventController()
