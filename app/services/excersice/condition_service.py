from sqlalchemy.orm import Session

from app.models import Condition


class ConditionService:
    def list_conditions(self, db: Session, type: str | None = None) -> list[Condition]:
        query = db.query(Condition)

        if type:
            query = query.filter(Condition.type == type)

        return query.order_by(Condition.code).all()


condition_service = ConditionService()
