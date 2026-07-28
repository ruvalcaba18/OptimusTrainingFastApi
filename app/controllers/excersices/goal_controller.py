from typing import List
from sqlalchemy.orm import Session
from app.services import goal_service
from app.models import Goal
from app.core.error_handlers import handle_controller_errors


class GoalController:

    @staticmethod
    @handle_controller_errors
    def list_goals(db: Session) -> List[Goal]:
        return goal_service.list_goals(db)


goal_controller = GoalController()
