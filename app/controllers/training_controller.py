from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.training_service import training_service
from app.services.coach_service import coach_service
from app.schemas.training import (
    TrainingPlanCreate,
    TrainingPlanResponse,
    DailyWorkoutCreate,
    DailyWorkoutResponse,
    ExerciseDetailCreate,
    PlanStatus,
    CoachAthleteResponse
)


class TrainingController:

    # ━━━━━━━━━━━━━━━━━━━━━━━━  Athlete Management  ━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def assign_athlete_to_coach(
        db: Session, coach_id: int, current_user: User
    ) -> CoachAthleteResponse:
        """Asignar un atleta al coach especificado."""
        # Verificar que el coach existe
        coach = coach_service.get_by_id(db, coach_id)
        if not coach:
            raise HTTPException(status_code=404, detail="Coach no encontrado")
            
        try:
            # Aquí asumimos que el current_user es el atleta que quiere al coach
            # o que hay una lógica previa de "requerimiento de servicio"
            relation = training_service.assign_athlete(db, coach_id, current_user.id)
            db.commit()
            return relation
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al asignar atleta: {str(e)}")

    @staticmethod
    def list_my_athletes(db: Session, current_user: User) -> List[CoachAthleteResponse]:
        """Listar atletas asignados al coach (current_user)."""
        coach = coach_service.get_by_user_id(db, current_user.id)
        if not coach:
            raise HTTPException(status_code=404, detail="Perfil de coach no encontrado")
            
        return training_service.list_coach_athletes(db, coach.id)

    # ━━━━━━━━━━━━━━━━━━━━━━━━  Training Plan  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def create_monthly_plan(
        db: Session, plan_in: TrainingPlanCreate, current_user: User
    ) -> TrainingPlanResponse:
        """Coach crea un plan mensual para un atleta."""
        coach = coach_service.get_by_user_id(db, current_user.id)
        if not coach:
            raise HTTPException(status_code=403, detail="Solo coaches pueden crear planes")
            
        try:
            plan = training_service.create_plan(db, coach.id, plan_in)
            db.commit()
            return plan
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def add_workout_to_plan(
        db: Session, plan_id: int, workout_in: DailyWorkoutCreate, current_user: User
    ) -> DailyWorkoutResponse:
        """Coach añade un entrenamiento a un plan."""
        plan = training_service.get_plan_by_id(db, plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan no encontrado")
            
        coach = coach_service.get_by_user_id(db, current_user.id)
        if not coach or plan.coach_id != coach.id:
            raise HTTPException(status_code=403, detail="No autorizado para editar este plan")
            
        try:
            workout = training_service.add_workout(db, plan_id, workout_in)
            db.commit()
            return workout
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def modify_workout(
        db: Session, workout_id: int, exercises: List[ExerciseDetailCreate], current_user: User
    ) -> DailyWorkoutResponse:
        """Coach modifica los ejercicios de un entrenamiento."""
        workout = training_service.get_workout_by_id(db, workout_id)
        if not workout:
            raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
            
        plan = training_service.get_plan_by_id(db, workout.plan_id)
        coach = coach_service.get_by_user_id(db, current_user.id)
        if not coach or plan.coach_id != coach.id:
            raise HTTPException(status_code=403, detail="No autorizado para modificar este entrenamiento")
            
        try:
            updated = training_service.update_workout_exercises(db, workout_id, exercises)
            db.commit()
            return updated
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def athlete_accept_plan(db: Session, plan_id: int, current_user: User) -> TrainingPlanResponse:
        """Atleta acepta el plan propuesto."""
        plan = training_service.get_plan_by_id(db, plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan no encontrado")
        if plan.athlete_id != current_user.id:
            raise HTTPException(status_code=403, detail="Solo el atleta asignado puede aceptar el plan")
            
        try:
            plan = training_service.update_plan_status(db, plan, PlanStatus.ACCEPTED)
            db.commit()
            return plan
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    # ━━━━━━━━━━━━━━━━━━━━━━━━  Validation  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def validate_workout_completion(
        db: Session, workout_id: int, current_user: User
    ) -> DailyWorkoutResponse:
        """Coach valida que el atleta hizo el ejercicio."""
        workout = training_service.get_workout_by_id(db, workout_id)
        if not workout:
            raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
            
        plan = training_service.get_plan_by_id(db, workout.plan_id)
        coach = coach_service.get_by_user_id(db, current_user.id)
        if not coach or plan.coach_id != coach.id:
            raise HTTPException(status_code=403, detail="No autorizado para validar")
            
        try:
            validated = training_service.validate_daily_workout(db, workout_id)
            db.commit()
            return validated
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def check_payment_status(db: Session, coach_id: int, month: int, year: int) -> dict:
        """Verificar si el coach es elegible para pago."""
        is_eligible = training_service.check_coach_payment_eligibility(db, coach_id, month, year)
        return {
            "coach_id": coach_id,
            "month": month,
            "year": year,
            "eligible_for_payment": is_eligible,
            "reason": "Debe validar al menos 15 días de entrenamiento" if not is_eligible else "OK"
        }


training_controller = TrainingController()
