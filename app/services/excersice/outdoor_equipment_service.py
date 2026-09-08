from typing import final

from sqlalchemy.orm import Session

from app.models.excersice.outdoor_equipment import OutdoorEquipmentModel


@final
class OutdoorEquipmentService:
    def list_outdoor_equipment(self, db: Session) -> list[OutdoorEquipmentModel]:
        return db.query(OutdoorEquipmentModel).order_by(OutdoorEquipmentModel.id).all()

outdoor_equipment_service = OutdoorEquipmentService()
