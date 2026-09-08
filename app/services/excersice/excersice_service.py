from sqlalchemy.orm import Session

from app.models import Condition, Excersice, ExcersiceCondition, Goal


class ExcersiceService:
    def list_excersices(
        self,
        db: Session,
        name: str | None = None,
        muscle_group: str | None = None,
        pattern: str | None = None,
        level: str | None = None,
        goal_code: str | None = None,
        exclude_condition_codes: list[str] | None = None,
    ) -> list[Excersice]:
        query = db.query(Excersice)

        if name:
            query = query.filter(Excersice.name.ilike(f"%{name}%"))

        if muscle_group:
            query = query.filter(Excersice.muscle_group == muscle_group)

        if pattern:
            query = query.filter(Excersice.pattern == pattern)

        if level:
            query = query.filter(Excersice.level == level)

        if goal_code:
            query = query.join(Excersice.goals).filter(Goal.code == goal_code)

        if exclude_condition_codes:
            forbidden_subquery = (
                db.query(ExcersiceCondition.excersice_id)
                .join(Condition)
                .filter(
                    Condition.code.in_(exclude_condition_codes),
                    ExcersiceCondition.relationship == "FORBIDDEN",
                )
            )
            query = query.filter(~Excersice.id.in_(forbidden_subquery))

        return query.order_by(Excersice.code).all()


excersice_service = ExcersiceService()
