from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.goal_service import goal_service
from app.models.goal import Goal

class GoalController:

    @staticmethod
    def list_goals(db: Session) -> List[Goal]:
        try:
            return goal_service.list_goals(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar objetivos: {str(e)}")

goal_controller = GoalController()
