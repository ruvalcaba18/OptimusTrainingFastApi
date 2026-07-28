from typing import List, Optional
from sqlalchemy.orm import Session
from app.services import excersice_service
from app.models import Excersice
from app.core.error_handlers import handle_controller_errors


class ExcersiceController:

    @staticmethod
    @handle_controller_errors
    def list_excersices(
        db: Session,
        muscle_group: Optional[str] = None,
        pattern: Optional[str] = None,
        level: Optional[str] = None,
        goal_code: Optional[str] = None,
        exclude_condition_codes: Optional[List[str]] = None,
    ) -> List[Excersice]:
        return excersice_service.list_excersices(
            db,
            muscle_group=muscle_group,
            pattern=pattern,
            level=level,
            goal_code=goal_code,
            exclude_condition_codes=exclude_condition_codes,
        )


excersice_controller = ExcersiceController()
