from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services import equipment_service
from app.models import Equipment

class EquipmentController:

    @staticmethod
    def list_equipments(db: Session) -> List[Equipment]:
        try:
            return equipment_service.list_equipments(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar equipamientos: {str(e)}")

equipment_controller = EquipmentController()
