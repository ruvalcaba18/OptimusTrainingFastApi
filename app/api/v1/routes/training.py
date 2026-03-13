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


@router.post("/assign/{coach_id}", response_model=CoachAthleteResponse)
def assign_coach(
    coach_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """El atleta actual se asigna al coach especificado."""
    return training_controller.assign_athlete_to_coach(db, coach_id, current_user)


@router.get("/my-athletes", response_model=List[CoachAthleteResponse])
def get_my_athletes(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """El coach ve sus atletas asignados."""
    return training_controller.list_my_athletes(db, current_user)


@router.post("/plans", response_model=TrainingPlanResponse)
def create_plan(
    plan_in: TrainingPlanCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """El coach crea un plan mensual para un atleta."""
    return training_controller.create_monthly_plan(db, plan_in, current_user)


@router.post("/plans/{plan_id}/workouts", response_model=DailyWorkoutResponse)
def add_workout_to_plan(
    plan_id: int,
    workout_in: DailyWorkoutCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """El coach añade un entrenamiento diario al plan."""
    return training_controller.add_workout_to_plan(db, plan_id, workout_in, current_user)


@router.put("/workouts/{workout_id}", response_model=DailyWorkoutResponse)
def modify_workout(
    workout_id: int,
    exercises: List[ExerciseDetailCreate],
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """El coach modifica los ejercicios de un entrenamiento."""
    return training_controller.modify_workout(db, workout_id, exercises, current_user)


@router.post("/plans/{plan_id}/accept", response_model=TrainingPlanResponse)
def accept_plan(
    plan_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """El atleta acepta el plan."""
    return training_controller.athlete_accept_plan(db, plan_id, current_user)


@router.post("/workouts/{workout_id}/validate", response_model=DailyWorkoutResponse)
def validate_workout(
    workout_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """El coach valida el entrenamiento diario."""
    return training_controller.validate_workout_completion(db, workout_id, current_user)


@router.get("/payment-status/{coach_id}")
def check_payment_status(
    coach_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2024),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Verificar si el coach es elegible para pago este mes."""
    # Podría requerirse scope de admin aquí
    return training_controller.check_payment_status(db, coach_id, month, year)
