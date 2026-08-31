from typing import List

from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.models import Level
from app.services import level_service


class LevelController:

    @staticmethod
    @handle_controller_errors
    def list_levels(db: Session) -> List[Level]:
        return level_service.list_levels(db)


level_controller = LevelController()
