from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.api import deps
from app.models.user import User
from app.models.prompt_log import PromptLog
from app.schemas.prompts.prompt_log_response import PromptLogResponse

router = APIRouter()

@router.get("/", response_model=List[PromptLogResponse],
            summary="Dashboard de prompts: Obtiene el historial de prompts del usuario autenticado.")
def get_prompt_logs(db: Session = Depends(get_db), current_user: User = Depends(deps.get_current_user)):
    logs = db.query(PromptLog).order_by(PromptLog.created_at.desc()).all()
    
    ADMIN_EMAILS = [
        "tu_correo@admin.com",
        "otro_admin@admin.com"
    ]

    # Verificar si el usuario autenticado está en la lista de administradores
    if current_user.email in ADMIN_EMAILS:
        return logs 
    else:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este recurso. Solo administradores.")
   