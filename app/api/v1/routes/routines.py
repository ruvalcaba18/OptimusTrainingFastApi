from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.events import event_bus
from app.events.domain import RoutineGeneratedEvent
from app.models import User, UserRoutine
from app.schemas.training import UserRoutineResponseSchema, UserRoutineUpdateSchema
from app.services import routine_generator

router = APIRouter()

@router.post("/generate", summary="Generar una rutina de entrenamiento personalizada", status_code=status.HTTP_200_OK)
def generate_my_routine(
    background_tasks: BackgroundTasks,
    day: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    try:
        if day is not None:
            result = routine_generator.generate_and_save_daily_routine(db, user=current_user, day=day)
            background_tasks.add_task(
                event_bus.dispatch,
                RoutineGeneratedEvent(
                    user_id=current_user.id,
                    weeks_count=1,
                    trigger_source="daily_fetch",
                    day=day,
                )
            )
            return result

        result = routine_generator.generate_and_save_monthly_routine(db, user=current_user)
        weeks_count = len(result.get("weeks", []))
        background_tasks.add_task(
            event_bus.dispatch,
            RoutineGeneratedEvent(
                user_id=current_user.id,
                weeks_count=weeks_count,
                trigger_source="onboarding",
            )
        )
        return result
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

@router.put("/week/{week}", summary="Modificar o regenerar rutina de una semana específica (Solo Premium)", status_code=status.HTTP_200_OK)
def update_or_regenerate_week_routine(
    week: int,
    day: Optional[int] = None,
    profile_in: Optional[UserRoutineUpdateSchema] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    return routine_generator.update_or_regenerate_week_routine(
        db=db,
        user=current_user,
        week=week,
        day=day,
        update_data=profile_in
    )

