"""
Competition service — data-access layer con ACID.

ACID guarantees:
  - Atomicity: flush() sin commit (commit en controller).
  - Consistency: UniqueConstraint + validación de capacidad pre-insert.
  - Isolation: with_for_update() en join y score update.
  - Idempotency: score update es idempotente (PUT semántico).
"""
from typing import List, Optional

from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from app.models.competition import Competition, CompetitionParticipant
from app.schemas.competitions import CompetitionCreate, CompetitionUpdate


class CompetitionService:

    # ━━━━━━━━━━━━━━━━━━━━━  Competition CRUD  ━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def create(
        db: Session, creator_id: int, comp_in: CompetitionCreate
    ) -> Competition:
        db_comp = Competition(
            creator_id=creator_id,
            title=comp_in.title,
            description=comp_in.description,
            sport_type=comp_in.sport_type,
            status="upcoming",
            location_name=comp_in.location_name,
            latitude=comp_in.latitude,
            longitude=comp_in.longitude,
            start_date=comp_in.start_date,
            end_date=comp_in.end_date,
            max_participants=comp_in.max_participants,
            rules=comp_in.rules,
            prize_description=comp_in.prize_description,
            cover_image_url=comp_in.cover_image_url,
        )
        db.add(db_comp)
        db.flush()
        db.refresh(db_comp)
        return db_comp

    @staticmethod
    def get_by_id(db: Session, comp_id: int) -> Optional[Competition]:
        return db.query(Competition).filter(Competition.id == comp_id).first()

    @staticmethod
    def get_by_id_for_update(db: Session, comp_id: int) -> Optional[Competition]:
        """Row-level lock — bloquea la competencia durante la transacción."""
        return (
            db.query(Competition)
            .filter(Competition.id == comp_id)
            .with_for_update()
            .first()
        )

    @staticmethod
    def get_multi(
        db: Session,
        sport_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Competition]:
        query = db.query(Competition)
        if sport_type:
            query = query.filter(Competition.sport_type == sport_type)
        if status:
            query = query.filter(Competition.status == status)
        return (
            query.order_by(Competition.start_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        db: Session, db_obj: Competition, comp_in: CompetitionUpdate
    ) -> Competition:
        update_data = comp_in.model_dump(exclude_unset=True)

        if "status" in update_data and update_data["status"] is not None:
            update_data["status"] = update_data["status"].value

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    # ━━━━━━━━━━━━━━━━━━━━  Participants (ACID)  ━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def get_participant(
        db: Session, comp_id: int, user_id: int
    ) -> Optional[CompetitionParticipant]:
        return (
            db.query(CompetitionParticipant)
            .filter(
                CompetitionParticipant.competition_id == comp_id,
                CompetitionParticipant.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def get_participant_for_update(
        db: Session, comp_id: int, user_id: int
    ) -> Optional[CompetitionParticipant]:
        """Row-level lock en el participante para score update."""
        return (
            db.query(CompetitionParticipant)
            .filter(
                CompetitionParticipant.competition_id == comp_id,
                CompetitionParticipant.user_id == user_id,
            )
            .with_for_update()
            .first()
        )

    @staticmethod
    def count_participants(db: Session, comp_id: int) -> int:
        return (
            db.query(sa_func.count(CompetitionParticipant.id))
            .filter(CompetitionParticipant.competition_id == comp_id)
            .scalar()
        )

    @staticmethod
    def add_participant(
        db: Session, comp_id: int, user_id: int
    ) -> CompetitionParticipant:
        participant = CompetitionParticipant(
            competition_id=comp_id,
            user_id=user_id,
        )
        db.add(participant)
        db.flush()
        db.refresh(participant)
        return participant

    @staticmethod
    def update_score(
        db: Session, participant: CompetitionParticipant, score: float
    ) -> CompetitionParticipant:
        """Idempotente — siempre establece el score al valor dado."""
        participant.score = score
        db.add(participant)
        db.flush()
        db.refresh(participant)
        return participant

    @staticmethod
    def recalculate_positions(db: Session, comp_id: int) -> None:
        """
        Recalcula las posiciones de todos los participantes con score,
        ordenados de mayor a menor.
        """
        participants = (
            db.query(CompetitionParticipant)
            .filter(
                CompetitionParticipant.competition_id == comp_id,
                CompetitionParticipant.score.isnot(None),
            )
            .order_by(CompetitionParticipant.score.desc())
            .all()
        )
        for i, p in enumerate(participants, start=1):
            p.position = i
            db.add(p)
        db.flush()

    @staticmethod
    def get_ranking(
        db: Session, comp_id: int
    ) -> List[CompetitionParticipant]:
        return (
            db.query(CompetitionParticipant)
            .filter(CompetitionParticipant.competition_id == comp_id)
            .order_by(
                CompetitionParticipant.position.asc().nullslast(),
                CompetitionParticipant.joined_at.asc(),
            )
            .all()
        )

    @staticmethod
    def get_participants(
        db: Session, comp_id: int, skip: int = 0, limit: int = 100
    ) -> List[CompetitionParticipant]:
        return (
            db.query(CompetitionParticipant)
            .filter(CompetitionParticipant.competition_id == comp_id)
            .order_by(CompetitionParticipant.joined_at)
            .offset(skip)
            .limit(limit)
            .all()
        )


competition_service = CompetitionService()
