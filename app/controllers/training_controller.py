from typing import List

from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.core.exceptions import BadRequestError, ForbiddenError, NotFoundError
from app.models import User
from app.schemas.training import (
    CoachAthleteResponse,
    DailyWorkoutCreate,
    DailyWorkoutResponse,
    ExerciseDetailCreate,
    PlanStatus,
    TrainingPlanCreate,
    TrainingPlanResponse,
)
from app.services import coach_service, training_service


class TrainingController:

    @staticmethod
    @handle_controller_errors
    def assign_athlete_to_coach(
        db: Session, coach_id: int, current_user: User
    ) -> CoachAthleteResponse:
        coach = coach_service.get_by_id(db, coach_id)
        if not coach:
            raise NotFoundError("Coach no encontrado")

        relation = training_service.assign_athlete(db, coach_id, current_user.id)
        db.commit()
        return relation

    @staticmethod
    @handle_controller_errors
    def list_my_athletes(db: Session, current_user: User) -> List[CoachAthleteResponse]:
        coach = coach_service.get_by_user_id(db, current_user.id)
        if not coach:
            raise NotFoundError("Perfil de coach no encontrado")

        return training_service.list_coach_athletes(db, coach.id)

    @staticmethod
    @handle_controller_errors
    def create_monthly_plan(
        db: Session, plan_in: TrainingPlanCreate, current_user: User
    ) -> TrainingPlanResponse:
        coach = coach_service.get_by_user_id(db, current_user.id)
        if not coach:
            raise ForbiddenError("Solo coaches pueden crear planes")

        plan = training_service.create_plan(db, coach.id, plan_in)
        db.commit()
        return plan

    @staticmethod
    @handle_controller_errors
    def add_workout_to_plan(
        db: Session, plan_id: int, workout_in: DailyWorkoutCreate, current_user: User
    ) -> DailyWorkoutResponse:
        plan = training_service.get_plan_by_id(db, plan_id)
        if not plan:
            raise NotFoundError("Plan no encontrado")

        coach = coach_service.get_by_user_id(db, current_user.id)
        if not coach or plan.coach_id != coach.id:
            raise ForbiddenError("No autorizado para editar este plan")

        workout = training_service.add_workout(db, plan_id, workout_in)
        db.commit()
        return workout

    @staticmethod
    @handle_controller_errors
    def modify_workout(
        db: Session, workout_id: int, exercises: List[ExerciseDetailCreate], current_user: User
    ) -> DailyWorkoutResponse:
        workout = training_service.get_workout_by_id(db, workout_id)
        if not workout:
            raise NotFoundError("Entrenamiento no encontrado")

        plan = training_service.get_plan_by_id(db, workout.plan_id)
        coach = coach_service.get_by_user_id(db, current_user.id)
        if not coach or plan.coach_id != coach.id:
            raise ForbiddenError("No autorizado para modificar este entrenamiento")

        updated = training_service.update_workout_exercises(db, workout_id, exercises)
        db.commit()
        return updated

    @staticmethod
    @handle_controller_errors
    def athlete_accept_plan(db: Session, plan_id: int, current_user: User) -> TrainingPlanResponse:
        plan = training_service.get_plan_by_id(db, plan_id)
        if not plan:
            raise NotFoundError("Plan no encontrado")
        if plan.athlete_id != current_user.id:
            raise ForbiddenError("Solo el atleta asignado puede aceptar el plan")

        plan = training_service.update_plan_status(db, plan, PlanStatus.ACCEPTED)
        db.commit()
        return plan

    @staticmethod
    @handle_controller_errors
    def validate_workout_completion(
        db: Session, workout_id: int, current_user: User
    ) -> DailyWorkoutResponse:
        workout = training_service.get_workout_by_id(db, workout_id)
        if not workout:
            raise NotFoundError("Entrenamiento no encontrado")

        plan = training_service.get_plan_by_id(db, workout.plan_id)
        coach = coach_service.get_by_user_id(db, current_user.id)
        if not coach or plan.coach_id != coach.id:
            raise ForbiddenError("No autorizado para validar")

        validated = training_service.validate_daily_workout(db, workout_id)
        db.commit()
        return validated

    @staticmethod
    @handle_controller_errors
    def check_payment_status(db: Session, coach_id: int, month: int, year: int) -> dict:
        is_eligible = training_service.check_coach_payment_eligibility(db, coach_id, month, year)
        return {
            "coach_id": coach_id,
            "month": month,
            "year": year,
            "eligible_for_payment": is_eligible,
            "reason": "Debe validar al menos 15 días de entrenamiento" if not is_eligible else "OK",
        }


training_controller = TrainingController()
