from typing import final

from sqlalchemy.orm import Session

from app.models.excersice.gym_equipment import GymEquipmentModel


@final
class GymEquipmentService:
    def list_gym_equipment(self, db: Session) -> list[GymEquipmentModel]:
        return db.query(GymEquipmentModel).order_by(GymEquipmentModel.id).all()

gym_equipment_service = GymEquipmentService()
