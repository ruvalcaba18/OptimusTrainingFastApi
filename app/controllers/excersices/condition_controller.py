from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services import condition_service
from app.models import Condition

class ConditionController:

    @staticmethod
    def list_conditions(db: Session, type: Optional[str] = None) -> List[Condition]:
        try:
            return condition_service.list_conditions(db, type=type)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar condiciones médicas: {str(e)}")

condition_controller = ConditionController()
