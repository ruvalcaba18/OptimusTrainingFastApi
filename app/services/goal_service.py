from typing import List
from sqlalchemy.orm import Session
from app.models.goal import Goal

class GoalService:
    def list_goals(self, db: Session) -> List[Goal]:
        return db.query(Goal).order_by(Goal.code).all()

goal_service = GoalService()
