from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Condition, Excersice, ExcersiceCondition, Goal


class ExcersiceService:
    def list_excersices(
        self,
        db: Session,
        name: Optional[str] = None,
        muscle_group: Optional[str] = None,
        pattern: Optional[str] = None,
        level: Optional[str] = None,
        goal_code: Optional[str] = None,
        exclude_condition_codes: Optional[List[str]] = None,
    ) -> List[Excersice]:
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
                    ExcersiceCondition.relationship == "FORBIDDEN"
                )
            )
            query = query.filter(~Excersice.id.in_(forbidden_subquery))

        return query.order_by(Excersice.code).all()

excersice_service = ExcersiceService()
