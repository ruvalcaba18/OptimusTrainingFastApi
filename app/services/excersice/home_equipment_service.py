from typing import List, final

from sqlalchemy.orm import Session

from app.models.excersice.home_equipment import HomeEquipmentModel


@final
class HomeEquipmentService:
    def list_home_equipment(self, db: Session) -> List[HomeEquipmentModel]:
        return db.query(HomeEquipmentModel).order_by(HomeEquipmentModel.id).all()

home_equipment_service = HomeEquipmentService()
