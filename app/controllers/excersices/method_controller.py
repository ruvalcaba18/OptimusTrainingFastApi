from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.method_service import method_service
from app.models.method import Method

class MethodController:

    @staticmethod
    def list_methods(db: Session, category: Optional[str] = None) -> List[Method]:
        try:
            return method_service.list_methods(db, category=category)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar métodos: {str(e)}")

method_controller = MethodController()
