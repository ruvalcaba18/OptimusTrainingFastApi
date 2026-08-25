from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models import User, UserRoutine
from app.services import routine_generator
from typing import Optional
from app.schemas.training import UserRoutineUpdateSchema, UserRoutineResponseSchema

router = APIRouter()

@router.post("/generate", summary="Generar una rutina de entrenamiento personalizada", status_code=status.HTTP_200_OK)
def generate_my_routine(
    day: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    try:
        if day is not None:
            return routine_generator.generate_and_save_daily_routine(db, user=current_user, day=day)
        return routine_generator.generate_and_save_monthly_routine(db, user=current_user)
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

@router.get("/my-plan", summary="Obtener el plan mensual guardado (semanas y días)", status_code=status.HTTP_200_OK)
def get_my_plan(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    return routine_generator.get_monthly_plan(db, user=current_user)

@router.get("/day/{week}/{day}", summary="Obtener la rutina guardada de un día específico", response_model=UserRoutineResponseSchema)
def get_routine_day(
    week: int,
    day: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> UserRoutine:
    return routine_generator.get_routine_for_day(db, user=current_user, week=week, day=day)

@router.put("/day/{day}", summary="Modificar rutina estática de un día específico (Premium)", response_model=UserRoutineResponseSchema)
def update_my_routine(
    day: int,
    profile_in: UserRoutineUpdateSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> UserRoutine:
    return routine_generator.update_user_routine(db, user=current_user, day=day, update_data=profile_in)
