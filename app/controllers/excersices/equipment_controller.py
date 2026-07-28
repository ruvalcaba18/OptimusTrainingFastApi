from typing import List
from sqlalchemy.orm import Session
from app.services import equipment_service
from app.models import Equipment
from app.core.error_handlers import handle_controller_errors


class EquipmentController:

    @staticmethod
    @handle_controller_errors
    def list_equipments(db: Session) -> List[Equipment]:
        return equipment_service.list_equipments(db)


equipment_controller = EquipmentController()
