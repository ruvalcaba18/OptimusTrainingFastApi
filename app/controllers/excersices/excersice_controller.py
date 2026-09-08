from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.models import Excersice
from app.services import excersice_service


class ExcersiceController:
    @staticmethod
    @handle_controller_errors
    def list_excersices(
        db: Session,
        name: str | None = None,
        muscle_group: str | None = None,
        pattern: str | None = None,
        level: str | None = None,
        goal_code: str | None = None,
        exclude_condition_codes: list[str] | None = None,
    ) -> list[Excersice]:

        return excersice_service.list_excersices(
            db,
            name=name,
            muscle_group=muscle_group,
            pattern=pattern,
            level=level,
            goal_code=goal_code,
            exclude_condition_codes=exclude_condition_codes,
        )


excersice_controller = ExcersiceController()
