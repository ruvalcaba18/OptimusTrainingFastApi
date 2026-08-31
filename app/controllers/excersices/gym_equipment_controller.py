from typing import List, final

from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.models.excersice.gym_equipment import GymEquipmentModel
from app.services.excersice.gym_equipment_service import gym_equipment_service


@final
class GymEquipmentController:
    @staticmethod
    @handle_controller_errors
    def list_gym_equipment(db: Session) -> List[GymEquipmentModel]:
        return gym_equipment_service.list_gym_equipment(db)

gym_equipment_controller = GymEquipmentController()
