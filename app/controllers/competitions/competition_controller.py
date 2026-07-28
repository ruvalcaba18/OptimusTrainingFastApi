from typing import Optional
from sqlalchemy.orm import Session

from app.models import User
from app.services import competition_service
from app.schemas.competitions import (
    CompetitionCreate,
    CompetitionUpdate,
    CompetitionResponse,
    JoinCompetitionRequest,
    ScoreUpdateRequest,
    CompetitionParticipantResponse,
    RankingResponse,
)
from app.controllers.competitions.exceptions import (
    CompetitionNotFoundError,
    CompetitionFullError,
    CompetitionCancelledError,
    CompetitionFinishedError,
    AlreadyJoinedCompetitionError,
    ParticipantNotFoundError,
)
from app.core.exceptions import ForbiddenError
from app.core.error_handlers import handle_controller_errors


class CompetitionController:

    @staticmethod
    @handle_controller_errors
    def create_competition(
        db: Session, comp_in: CompetitionCreate, current_user: User
    ) -> CompetitionResponse:
        comp = competition_service.create(
            db, creator_id=current_user.id, comp_in=comp_in
        )
        db.commit()
        count = competition_service.count_participants(db, comp.id)
        resp = CompetitionResponse.model_validate(comp)
        resp.participant_count = count
        return resp

    @staticmethod
    @handle_controller_errors
    def list_competitions(
        db: Session,
        sport_type: Optional[str] = None,
        comp_status: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[CompetitionResponse]:
        comps = competition_service.get_multi(
            db, sport_type=sport_type, status=comp_status, skip=skip, limit=limit
        )
        results = []
        for c in comps:
            count = competition_service.count_participants(db, c.id)
            resp = CompetitionResponse.model_validate(c)
            resp.participant_count = count
            results.append(resp)
        return results

    @staticmethod
    @handle_controller_errors
    def get_competition(db: Session, comp_id: int) -> CompetitionResponse:
        comp = competition_service.get_by_id(db, comp_id)
        if not comp:
            raise CompetitionNotFoundError()
        count = competition_service.count_participants(db, comp.id)
        resp = CompetitionResponse.model_validate(comp)
        resp.participant_count = count
        return resp

    @staticmethod
    @handle_controller_errors
    def update_competition(
        db: Session, comp_id: int, comp_in: CompetitionUpdate, current_user: User
    ) -> CompetitionResponse:
        comp = competition_service.get_by_id(db, comp_id)
        if not comp:
            raise CompetitionNotFoundError()
        if comp.creator_id != current_user.id:
            raise ForbiddenError("Solo el creador puede editar esta competencia")

        updated = competition_service.update(db, db_obj=comp, comp_in=comp_in)
        db.commit()
        count = competition_service.count_participants(db, updated.id)
        resp = CompetitionResponse.model_validate(updated)
        resp.participant_count = count
        return resp

    @staticmethod
    @handle_controller_errors
    def join_competition(
        db: Session, join_in: JoinCompetitionRequest, current_user: User
    ) -> CompetitionParticipantResponse:
        comp = competition_service.get_by_id_for_update(db, join_in.competition_id)
        if not comp:
            raise CompetitionNotFoundError()
        if comp.status == "cancelled":
            raise CompetitionCancelledError()
        if comp.status == "finished":
            raise CompetitionFinishedError()

        existing = competition_service.get_participant(
            db, comp_id=join_in.competition_id, user_id=current_user.id
        )
        if existing:
            raise AlreadyJoinedCompetitionError()

        if comp.max_participants is not None:
            current_count = competition_service.count_participants(db, comp.id)
            if current_count >= comp.max_participants:
                raise CompetitionFullError()

        participant = competition_service.add_participant(
            db, comp_id=join_in.competition_id, user_id=current_user.id
        )
        db.commit()
        return participant

    @staticmethod
    @handle_controller_errors
    def update_score(
        db: Session, score_in: ScoreUpdateRequest, current_user: User
    ) -> CompetitionParticipantResponse:
        comp = competition_service.get_by_id(db, score_in.competition_id)
        if not comp:
            raise CompetitionNotFoundError()
        if comp.creator_id != current_user.id:
            raise ForbiddenError("Solo el creador puede actualizar scores")

        participant = competition_service.get_participant_for_update(
            db, comp_id=score_in.competition_id, user_id=score_in.user_id
        )
        if not participant:
            raise ParticipantNotFoundError()

        updated = competition_service.update_score(
            db, participant=participant, score=score_in.score
        )
        competition_service.recalculate_positions(db, comp_id=score_in.competition_id)
        db.commit()
        db.refresh(updated)
        return updated

    @staticmethod
    @handle_controller_errors
    def get_ranking(
        db: Session, competition_id: int
    ) -> RankingResponse:
        comp = competition_service.get_by_id(db, competition_id)
        if not comp:
            raise CompetitionNotFoundError()
        participants = competition_service.get_ranking(db, comp_id=competition_id)
        return RankingResponse(
            competition_id=competition_id,
            participants=[
                CompetitionParticipantResponse.model_validate(p) for p in participants
            ],
        )


competition_controller = CompetitionController()
