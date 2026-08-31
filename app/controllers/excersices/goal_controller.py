from typing import List

from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.models import Goal
from app.services import goal_service


class GoalController:

    @staticmethod
    @handle_controller_errors
    def list_goals(db: Session) -> List[Goal]:
        return goal_service.list_goals(db)


goal_controller = GoalController()
