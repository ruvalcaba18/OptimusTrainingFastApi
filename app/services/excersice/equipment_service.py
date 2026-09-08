from sqlalchemy.orm import Session

from app.models import Equipment


class EquipmentService:
    def list_equipments(self, db: Session) -> list[Equipment]:
        return db.query(Equipment).order_by(Equipment.name).all()


equipment_service = EquipmentService()
