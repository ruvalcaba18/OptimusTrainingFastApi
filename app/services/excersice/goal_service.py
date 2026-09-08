
from sqlalchemy.orm import Session

from app.models import Goal


class GoalService:
    def list_goals(self, db: Session) -> list[Goal]:
        return db.query(Goal).order_by(Goal.code).all()

goal_service = GoalService()
