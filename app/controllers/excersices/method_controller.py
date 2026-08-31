from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.models import Method
from app.services import method_service


class MethodController:

    @staticmethod
    @handle_controller_errors
    def list_methods(db: Session, category: Optional[str] = None) -> List[Method]:
        return method_service.list_methods(db, category=category)


method_controller = MethodController()
