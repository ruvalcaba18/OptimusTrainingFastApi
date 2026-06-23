from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.excersice_service import excersice_service
from app.models.excersices import Excersice

class ExcersiceController:

    @staticmethod
    def list_excersices(
        db: Session,
        muscle_group: Optional[str] = None,
        pattern: Optional[str] = None,
        level: Optional[str] = None,
        goal_code: Optional[str] = None,
        exclude_condition_codes: Optional[List[str]] = None,
    ) -> List[Excersice]:
        try:
            return excersice_service.list_excersices(
                db,
                muscle_group=muscle_group,
                pattern=pattern,
                level=level,
                goal_code=goal_code,
                exclude_condition_codes=exclude_condition_codes,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar ejercicios: {str(e)}")

excersice_controller = ExcersiceController()
