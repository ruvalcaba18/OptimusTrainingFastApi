from datetime import datetime, date, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.training import CoachAthlete, TrainingPlan, DailyWorkout, ExerciseDetail, PlanStatus, WorkoutStatus
from app.models.coach import CoachProfile
from app.schemas.training import TrainingPlanCreate, DailyWorkoutCreate, ExerciseDetailCreate


class TrainingService:
    # ━━━━━━━━━━━━━━━━━━━━━━━━  Athlete Management  ━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def assign_athlete(db: Session, coach_id: int, athlete_id: int) -> CoachAthlete:
        """Asignar un atleta a un coach (máximo 10 activos)."""
        # Contar atletas activos
        active_count = db.query(CoachAthlete).filter(
            CoachAthlete.coach_id == coach_id,
            CoachAthlete.is_active == True
        ).count()
        if active_count >= 10:
            raise ValueError("El coach ya tiene el máximo de 10 atletas permitidos.")
        
        # Verificar si ya existe la relación
        existing = db.query(CoachAthlete).filter(
            CoachAthlete.coach_id == coach_id,
            CoachAthlete.athlete_id == athlete_id
        ).first()
        
        if existing:
            existing.is_active = True
            db.add(existing)
            db.flush()
            return existing
            
        db_rel = CoachAthlete(coach_id=coach_id, athlete_id=athlete_id)
        db.add(db_rel)
        db.flush()
        db.refresh(db_rel)
        return db_rel

    @staticmethod
    def list_coach_athletes(db: Session, coach_id: int) -> List[CoachAthlete]:
        return db.query(CoachAthlete).filter(
            CoachAthlete.coach_id == coach_id,
            CoachAthlete.is_active == True
        ).all()

    # ━━━━━━━━━━━━━━━━━━━━━━━━  Training Plan  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def create_plan(db: Session, coach_id: int, plan_in: TrainingPlanCreate) -> TrainingPlan:
        """Crear un plan de entrenamiento mensual."""
        # Verificar si ya existe un plan para este mes/año
        existing = db.query(TrainingPlan).filter(
            TrainingPlan.coach_id == coach_id,
            TrainingPlan.athlete_id == plan_in.athlete_id,
            TrainingPlan.month == plan_in.month,
            TrainingPlan.year == plan_in.year
        ).first()
        
        if existing:
            raise ValueError(f"Ya existe un plan para el mes {plan_in.month}/{plan_in.year}.")
            
        db_plan = TrainingPlan(
            coach_id=coach_id,
            athlete_id=plan_in.athlete_id,
            month=plan_in.month,
            year=plan_in.year,
            status=PlanStatus.DRAFT
        )
        db.add(db_plan)
        db.flush()
        db.refresh(db_plan)
        return db_plan

    @staticmethod
    def get_plan_by_id(db: Session, plan_id: int) -> Optional[TrainingPlan]:
        return db.query(TrainingPlan).filter(TrainingPlan.id == plan_id).first()

    @staticmethod
    def update_plan_status(db: Session, plan: TrainingPlan, status: PlanStatus) -> TrainingPlan:
        plan.status = status
        db.add(plan)
        db.flush()
        db.refresh(plan)
        return plan

    # ━━━━━━━━━━━━━━━━━━━━━━━━  Daily Workouts  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def add_workout(db: Session, plan_id: int, workout_in: DailyWorkoutCreate) -> DailyWorkout:
        """Añadir un entrenamiento diario con hasta 8 ejercicios."""
        db_workout = DailyWorkout(
            plan_id=plan_id,
            date=workout_in.date,
            status=WorkoutStatus.PENDING
        )
        db.add(db_workout)
        db.flush()
        
        for i, ex_in in enumerate(workout_in.exercises):
            db_ex = ExerciseDetail(
                workout_id=db_workout.id,
                name=ex_in.name,
                description=ex_in.description,
                sets=ex_in.sets,
                reps=ex_in.reps,
                weight=ex_in.weight,
                order=i
            )
            db.add(db_ex)
            
        db.flush()
        db.refresh(db_workout)
        return db_workout

    @staticmethod
    def get_workout_by_id(db: Session, workout_id: int) -> Optional[DailyWorkout]:
        return db.query(DailyWorkout).filter(DailyWorkout.id == workout_id).first()

    @staticmethod
    def update_workout_exercises(
        db: Session, workout_id: int, exercises_in: List[ExerciseDetailCreate]
    ) -> DailyWorkout:
        """Modificar ejercicios de un entrenamiento (realizado por el coach)."""
        db_workout = db.query(DailyWorkout).filter(DailyWorkout.id == workout_id).first()
        if not db_workout:
            return None
            
        # Eliminar ejercicios anteriores
        db.query(ExerciseDetail).filter(ExerciseDetail.workout_id == workout_id).delete()
        
        # Añadir nuevos (max 8)
        for i, ex_in in enumerate(exercises_in[:8]):
            db_ex = ExerciseDetail(
                workout_id=workout_id,
                name=ex_in.name,
                description=ex_in.description,
                sets=ex_in.sets,
                reps=ex_in.reps,
                weight=ex_in.weight,
                order=i
            )
            db.add(db_ex)
            
        db.flush()
        db.refresh(db_workout)
        return db_workout

    @staticmethod
    def validate_daily_workout(db: Session, workout_id: int) -> DailyWorkout:
        """El coach valida que el atleta realizó el ejercicio."""
        db_workout = db.query(DailyWorkout).filter(DailyWorkout.id == workout_id).first()
        if not db_workout:
            return None
            
        db_workout.coach_validated = True
        db_workout.status = WorkoutStatus.COMPLETED
        db_workout.validation_date = datetime.now()
        
        db.add(db_workout)
        db.flush()
        db.refresh(db_workout)
        return db_workout

    # ━━━━━━━━━━━━━━━━━━━━━━━━  Business Logic  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def can_see_next_workout(db: Session, plan_id: int, current_date: date) -> bool:
        """
        El atleta puede ver el siguiente ejercicio si el anterior fue validado.
        Asumiendo orden cronológico.
        """
        # Buscar el entrenamiento del día anterior o el último completado
        last_workout = db.query(DailyWorkout).filter(
            DailyWorkout.plan_id == plan_id,
            DailyWorkout.date < current_date
        ).order_by(DailyWorkout.date.desc()).first()
        
        if not last_workout:
            # Es el primer día del plan
            return True
            
        return last_workout.coach_validated

    @staticmethod
    def check_coach_payment_eligibility(
        db: Session, coach_id: int, month: int, year: int
    ) -> bool:
        """
        Un coach debe haber validado al menos 15 días en el mes 
        para recibir su pago.
        """
        validated_days = db.query(DailyWorkout).join(TrainingPlan).filter(
            TrainingPlan.coach_id == coach_id,
            TrainingPlan.month == month,
            TrainingPlan.year == year,
            DailyWorkout.coach_validated == True
        ).count()
        
        return validated_days >= 15


training_service = TrainingService()
