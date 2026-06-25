from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services import level_service
from app.models import Level

class LevelController:

    @staticmethod
    def list_levels(db: Session) -> List[Level]:
        try:
            return level_service.list_levels(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar niveles: {str(e)}")

level_controller = LevelController()
