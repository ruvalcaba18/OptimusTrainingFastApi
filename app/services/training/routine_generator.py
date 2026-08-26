import random
from typing import Dict, Any, List, Optional, final
from sqlalchemy.orm import Session
from app.models import User, UserRoutine, ProgrammingMatrix
from app.models.Enums.UserTier import UserTier
from app.services.training.exercise_selector import exercise_selector
from app.schemas.training.user_routine_schema import UserRoutineUpdateSchema

@final
class RoutineGenerator:
    
    @staticmethod
    def generate_routine(db: Session, user: User, day: Optional[int] = None) -> Dict[str, Any]:
        
        if not user.goal_id:
            raise ValueError("El usuario no tiene un perfil configurado.")

        viable_exercises = exercise_selector.select_exercises(db, user)
        
        if not viable_exercises:
            return RoutineGenerator._empty_fallback_routine(user)

        rules = RoutineGenerator._get_programming_rules(db, user)

        num_exercises = RoutineGenerator._determine_exercise_count(user.session_duration_code)
        sample_size = min(len(viable_exercises), num_exercises)

        selected_sample = RoutineGenerator._sample_exercises(user.id, viable_exercises, sample_size, day)

        routine_exercises = RoutineGenerator._format_selected_exercises(selected_sample)

        return {
            "goal": user.goal.name if user.goal else "N/A",
            "level": user.level.name if user.level else "N/A",
            "volume": rules["volume"],
            "sets": rules["sets"],
            "reps": rules["reps"],
            "rest": rules["rest"],
            "method_name": rules["method_name"],
            "day": day,
            "exercises": routine_exercises
        }

    @staticmethod
    def _empty_fallback_routine(user: User) -> Dict[str, Any]:
        return {
            "goal": user.goal.name if user.goal else "N/A",
            "level": user.level.name if user.level else "N/A",
            "volume": "N/A",
            "sets": 0,
            "reps": "N/A",
            "rest": "N/A",
            "method_name": "N/A",
            "exercises": [],
            "message": "No se encontraron ejercicios compatibles con tu perfil, equipamiento o salud."
        }

    @staticmethod
    def _get_programming_rules(db: Session, user: User) -> Dict[str, Any]:
        goal_code = user.goal.code if user.goal else "PG"
        level_code = user.level.code if user.level else "NIV1"

        matrix_rule = db.query(ProgrammingMatrix).filter(
            ProgrammingMatrix.goal_code == goal_code,
            ProgrammingMatrix.level_code == level_code
        ).first()

        return {
            "volume": matrix_rule.volume if matrix_rule else "Medio",
            "sets": matrix_rule.sets if matrix_rule else 3,
            "reps": matrix_rule.reps if matrix_rule else "12 reps",
            "rest": matrix_rule.rest if matrix_rule else "60s",
            "method_name": matrix_rule.method.name if (matrix_rule and matrix_rule.method) else "Series Tradicionales"
        }

    @staticmethod
    def _determine_exercise_count(duration_code: Optional[str]) -> int:
        code = (duration_code or "").upper()
        if code == "EXPRESS":
            return 3
        elif code == "STANDARD":
            return 5
        elif code == "EXTENDED":
            return 7
        return 4

    @staticmethod
    def _sample_exercises(user_id: int, exercises: List[Dict[str, Any]], count: int, day: Optional[int]) -> List[Dict[str, Any]]:
        if day is not None:
            local_random = random.Random(f"{user_id}_{day}")
            return local_random.sample(exercises, count)
        return random.sample(exercises, count)

    @staticmethod
    def _format_selected_exercises(selected_sample: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        routine_exercises = []
        for item in selected_sample:
            ex = item["exercise"]
            routine_exercises.append({
                "id": ex.id,
                "code": ex.code,
                "name": ex.name,
                "muscle_group": ex.muscle_group,
                "pattern": ex.pattern.value if hasattr(ex.pattern, "value") else str(ex.pattern),
                "complexity": ex.complexity,
                "caution_warnings": item["caution_warnings"],
                "has_caution": item["has_caution"]
            })
        return routine_exercises

    @staticmethod
    def _save_or_update_routine(db: Session, user_id: int, week: int, day: int, routine: Dict[str, Any]) -> None:
        
        existing = db.query(UserRoutine).filter(
            UserRoutine.user_id == user_id,
            UserRoutine.week == week,
            UserRoutine.day == day
        ).first()
        
        if existing:
            existing.goal = routine["goal"]
            existing.level = routine["level"]
            existing.volume = routine["volume"]
            existing.sets = routine["sets"]
            existing.reps = routine["reps"]
            existing.rest = routine["rest"]
            existing.method_name = routine["method_name"]
            existing.exercises = routine["exercises"]
        else:
            new_routine = UserRoutine(
                user_id=user_id,
                week=week,
                day=day,
                goal=routine["goal"],
                level=routine["level"],
                volume=routine["volume"],
                sets=routine["sets"],
                reps=routine["reps"],
                rest=routine["rest"],
                method_name=routine["method_name"],
                exercises=routine["exercises"]
            )
            db.add(new_routine)

    @staticmethod
    def generate_and_save_monthly_routine(db: Session, user: User) -> Dict[str, Any]:
 
        if user.specific_days:
            try:
                days = [int(d) for d in user.specific_days.split(",") if d.strip()]
            except Exception:
                days = [1, 3, 5]
        else:
            days = [1, 3, 5]
            
        first_routine = None
        for week in [1, 2, 3, 4]:
            for day_val in days:
                seed_day = (week - 1) * 7 + day_val
                routine = RoutineGenerator.generate_routine(db, user=user, day=seed_day)
                
                RoutineGenerator._save_or_update_routine(db, user.id, week, day_val, routine)
                
                if week == 1 and (first_routine is None or day_val == days[0]):
                    first_routine = routine
        db.commit()
        return first_routine

    @staticmethod
    def generate_and_save_daily_routine(db: Session, user: User, day: int) -> Dict[str, Any]:
   
        routine = RoutineGenerator.generate_routine(db, user=user, day=day)
        RoutineGenerator._save_or_update_routine(db, user.id, 1, day, routine)
        db.commit()
        return routine

    @staticmethod
    def update_user_routine(db: Session, user: User, day: int, update_data: UserRoutineUpdateSchema) -> UserRoutine:
   
        if user.tier != UserTier.PREMIUM:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Esta funcionalidad de edición manual de rutinas es exclusiva para usuarios Premium."
            )
            
        existing = db.query(UserRoutine).filter(
            UserRoutine.user_id == user.id,
            UserRoutine.day == day
        ).first()
        
        if not existing:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró una rutina generada para este día. Debes generarla primero."
            )
            
        if update_data.goal is not None:
            existing.goal = update_data.goal
        if update_data.level is not None:
            existing.level = update_data.level
        if update_data.volume is not None:
            existing.volume = update_data.volume
        if update_data.sets is not None:
            existing.sets = update_data.sets
        if update_data.reps is not None:
            existing.reps = update_data.reps
        if update_data.rest is not None:
            existing.rest = update_data.rest
        if update_data.method_name is not None:
            existing.method_name = update_data.method_name
        if update_data.exercises is not None:
            existing.exercises = update_data.exercises
            
        db.commit()
        db.refresh(existing)
        return existing

    @staticmethod
    def get_monthly_plan(db: Session, user: User) -> Dict[str, Any]:
        routines = db.query(UserRoutine).filter(
            UserRoutine.user_id == user.id
        ).order_by(UserRoutine.week, UserRoutine.day).all()

        weeks_map: Dict[int, list] = {}
        for routine in routines:
            weeks_map.setdefault(routine.week, []).append(routine.day)

        weeks = [
            {"week": week, "days": sorted(days)}
            for week, days in sorted(weeks_map.items())
        ]

        return {"weeks": weeks}

    @staticmethod
    def get_routine_for_day(db: Session, user: User, week: int, day: int) -> UserRoutine:
        routine = db.query(UserRoutine).filter(
            UserRoutine.user_id == user.id,
            UserRoutine.week == week,
            UserRoutine.day == day
        ).first()

        if not routine:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró rutina para semana {week}, día {day}."
            )

        return routine


routine_generator = RoutineGenerator()
