from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models import User
from app.services import routine_generator

router = APIRouter()

@router.post("/generate", summary="Generar una rutina de entrenamiento personalizada", status_code=status.HTTP_200_OK)
def generate_my_routine(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    try:
        routine = routine_generator.generate_routine(db, user=current_user)
        return routine
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al generar rutina: {str(e)}"
        )
