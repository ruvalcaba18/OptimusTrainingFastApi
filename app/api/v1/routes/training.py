from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.controllers.training_controller import training_controller
from app.models.user import User
from app.schemas.training import (
    TrainingPlanCreate,
    TrainingPlanResponse,
    DailyWorkoutCreate,
    DailyWorkoutResponse,
    ExerciseDetailCreate,
    CoachAthleteResponse
)

router = APIRouter()


@router.post(
    "/assign/{coach_id}",
    response_model=CoachAthleteResponse,
    summary="Vincular Atleta con Coach",
    response_description="La relación coach-atleta creada con éxito.",
)
def assign_coach(
    coach_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return training_controller.assign_athlete_to_coach(db, coach_id, current_user)


@router.get(
    "/my-athletes",
    response_model=List[CoachAthleteResponse],
    summary="Listar Atletas del Coach",
    response_description="Lista de atletas actualmente bajo el mando del coach.",
)
def get_my_athletes(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return training_controller.list_my_athletes(db, current_user)


@router.post(
    "/plans",
    response_model=TrainingPlanResponse,
    summary="Crear Plan de Entrenamiento Mensual",
    response_description="El plan de entrenamiento inicializado.",
)
def create_plan(
    plan_in: TrainingPlanCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return training_controller.create_monthly_plan(db, plan_in, current_user)


@router.post(
    "/plans/{plan_id}/workouts",
    response_model=DailyWorkoutResponse,
    summary="Agregar Entrenamiento Diario al Plan",
    response_description="El entrenamiento diario creado con sus ejercicios.",
)
def add_workout_to_plan(
    plan_id: int,
    workout_in: DailyWorkoutCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return training_controller.add_workout_to_plan(db, plan_id, workout_in, current_user)


@router.put(
    "/workouts/{workout_id}",
    response_model=DailyWorkoutResponse,
    summary="Modificar Ejercicios de un Entrenamiento",
    response_description="El entrenamiento actualizado.",
)
def modify_workout(
    workout_id: int,
    exercises: List[ExerciseDetailCreate],
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return training_controller.modify_workout(db, workout_id, exercises, current_user)


@router.post(
    "/plans/{plan_id}/accept",
    response_model=TrainingPlanResponse,
    summary="Aceptar Plan (Atleta)",
    response_description="El plan con estado actualizado a 'ACCEPTED'.",
)
def accept_plan(
    plan_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return training_controller.athlete_accept_plan(db, plan_id, current_user)


@router.post(
    "/workouts/{workout_id}/validate",
    response_model=DailyWorkoutResponse,
    summary="Validar Ejecución de Entrenamiento",
    response_description="El entrenamiento marcado como completado y validado.",
)
def validate_workout(
    workout_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return training_controller.validate_workout_completion(db, workout_id, current_user)


@router.get(
    "/payment-status/{coach_id}",
    summary="Consultar Elegibilidad de Pago del Coach",
    response_description="Objeto con el estatus de elegibilidad y la razón.",
)
def check_payment_status(
    coach_id: int,
    month: int = Query(..., ge=1, le=12, description="Mes a consultar (1-12)"),
    year: int = Query(..., ge=2024, description="Año a consultar"),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return training_controller.check_payment_status(db, coach_id, month, year)
