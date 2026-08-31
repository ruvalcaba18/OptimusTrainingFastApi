from typing import List

from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.models import Equipment
from app.services import equipment_service


class EquipmentController:

    @staticmethod
    @handle_controller_errors
    def list_equipments(db: Session) -> List[Equipment]:
        return equipment_service.list_equipments(db)

    @staticmethod
    @handle_controller_errors
    def get_equipment_categories(db: Session) -> dict:
        from app.models.excersice.everyday_item import EverydayItem
        from app.models.excersice.gym_equipment import GymEquipmentModel
        from app.models.excersice.home_equipment import HomeEquipmentModel
        from app.models.excersice.outdoor_equipment import OutdoorEquipmentModel
        
        gym = db.query(GymEquipmentModel).order_by(GymEquipmentModel.id).all()
        home = db.query(HomeEquipmentModel).order_by(HomeEquipmentModel.id).all()
        outdoor = db.query(OutdoorEquipmentModel).order_by(OutdoorEquipmentModel.id).all()
        everyday = db.query(EverydayItem).order_by(EverydayItem.id).all()
        
        return {
            "gym": gym,
            "home": home,
            "outdoor": outdoor,
            "everyday": everyday
        }


equipment_controller = EquipmentController()
