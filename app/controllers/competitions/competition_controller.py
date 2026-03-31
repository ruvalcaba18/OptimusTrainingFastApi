from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.competition_service import competition_service
from app.schemas.competitions import (
    CompetitionCreate,
    CompetitionUpdate,
    CompetitionResponse,
    JoinCompetitionRequest,
    ScoreUpdateRequest,
    CompetitionParticipantResponse,
    RankingResponse,
)


class CompetitionController:

                                                                       
    @staticmethod
    def create_competition(
        db: Session, comp_in: CompetitionCreate, current_user: User
    ) -> CompetitionResponse:
        try:
            comp = competition_service.create(
                db, creator_id=current_user.id, comp_in=comp_in
            )
            db.commit()
            count = competition_service.count_participants(db, comp.id)
            resp = CompetitionResponse.model_validate(comp)
            resp.participant_count = count
            return resp
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear competencia: {str(e)}",
            )

    @staticmethod
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
    def get_competition(db: Session, comp_id: int) -> CompetitionResponse:
        comp = competition_service.get_by_id(db, comp_id)
        if not comp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Competencia no encontrada",
            )
        count = competition_service.count_participants(db, comp.id)
        resp = CompetitionResponse.model_validate(comp)
        resp.participant_count = count
        return resp

    @staticmethod
    def update_competition(
        db: Session, comp_id: int, comp_in: CompetitionUpdate, current_user: User
    ) -> CompetitionResponse:
        comp = competition_service.get_by_id(db, comp_id)
        if not comp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Competencia no encontrada",
            )
        if comp.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el creador puede editar esta competencia",
            )

        try:
            updated = competition_service.update(db, db_obj=comp, comp_in=comp_in)
            db.commit()
            count = competition_service.count_participants(db, updated.id)
            resp = CompetitionResponse.model_validate(updated)
            resp.participant_count = count
            return resp
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar competencia: {str(e)}",
            )

                                                                       
    @staticmethod
    def join_competition(
        db: Session, join_in: JoinCompetitionRequest, current_user: User
    ) -> CompetitionParticipantResponse:
                           
        comp = competition_service.get_by_id_for_update(db, join_in.competition_id)
        if not comp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Competencia no encontrada",
            )
        if comp.status == "cancelled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes inscribirte en una competencia cancelada",
            )
        if comp.status == "finished":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta competencia ya finalizó",
            )

                              
        existing = competition_service.get_participant(
            db, comp_id=join_in.competition_id, user_id=current_user.id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya estás inscrito en esta competencia",
            )

                                
        if comp.max_participants is not None:
            current_count = competition_service.count_participants(db, comp.id)
            if current_count >= comp.max_participants:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La competencia ha alcanzado el máximo de participantes",
                )

                
        try:
            participant = competition_service.add_participant(
                db, comp_id=join_in.competition_id, user_id=current_user.id
            )
            db.commit()
            return participant
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al inscribirse: {str(e)}",
            )

                                                                       
    @staticmethod
    def update_score(
        db: Session, score_in: ScoreUpdateRequest, current_user: User
    ) -> CompetitionParticipantResponse:
        comp = competition_service.get_by_id(db, score_in.competition_id)
        if not comp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Competencia no encontrada",
            )
        if comp.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el creador puede actualizar scores",
            )

                                 
        participant = competition_service.get_participant_for_update(
            db, comp_id=score_in.competition_id, user_id=score_in.user_id
        )
        if not participant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante no encontrado en esta competencia",
            )

        try:
                                  
            updated = competition_service.update_score(
                db, participant=participant, score=score_in.score
            )
                                      
            competition_service.recalculate_positions(db, comp_id=score_in.competition_id)
            db.commit()
                                             
            db.refresh(updated)
            return updated
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar score: {str(e)}",
            )

                                                                       
    @staticmethod
    def get_ranking(
        db: Session, competition_id: int
    ) -> RankingResponse:
        comp = competition_service.get_by_id(db, competition_id)
        if not comp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Competencia no encontrada",
            )
        participants = competition_service.get_ranking(db, comp_id=competition_id)
        return RankingResponse(
            competition_id=competition_id,
            participants=[
                CompetitionParticipantResponse.model_validate(p) for p in participants
            ],
        )


competition_controller = CompetitionController()
