from typing import final

from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.models.excersice.outdoor_equipment import OutdoorEquipmentModel
from app.services.excersice.outdoor_equipment_service import outdoor_equipment_service


@final
class OutdoorEquipmentController:
    @staticmethod
    @handle_controller_errors
    def list_outdoor_equipment(db: Session) -> list[OutdoorEquipmentModel]:
        return outdoor_equipment_service.list_outdoor_equipment(db)


outdoor_equipment_controller = OutdoorEquipmentController()
