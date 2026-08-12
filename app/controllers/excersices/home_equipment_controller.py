from typing import List, final
from sqlalchemy.orm import Session
from app.services.excersice.home_equipment_service import home_equipment_service
from app.models.excersice.home_equipment import HomeEquipmentModel
from app.core.error_handlers import handle_controller_errors

@final
class HomeEquipmentController:
    @staticmethod
    @handle_controller_errors
    def list_home_equipment(db: Session) -> List[HomeEquipmentModel]:
        return home_equipment_service.list_home_equipment(db)

home_equipment_controller = HomeEquipmentController()
