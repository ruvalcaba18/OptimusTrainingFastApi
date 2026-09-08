
from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.models import Condition
from app.services import condition_service


class ConditionController:

    @staticmethod
    @handle_controller_errors
    def list_conditions(db: Session, type: str | None = None) -> list[Condition]:
        return condition_service.list_conditions(db, type=type)


condition_controller = ConditionController()
