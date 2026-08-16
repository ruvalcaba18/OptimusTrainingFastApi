import random
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models import User
from app.models import ProgrammingMatrix
from app.services.training.exercise_selector import exercise_selector

class RoutineGenerator:
    @staticmethod
    def generate_routine(db: Session, user: User, day: Optional[int] = None) -> Dict[str, Any]:
        """
        Generador automático de rutinas personalizadas (Fase 7).
        Obtiene los ejercicios viables filtrados por salud, nivel y equipamiento,
        y les aplica las variables de la matriz de programación correspondientes.
        """
        profile = user
        if not profile.goal_id:
            raise ValueError("El usuario no tiene un perfil configurado.")

        # Obtener los ejercicios válidos para el usuario
        viable_exercises = exercise_selector.select_exercises(db, user)
        if not viable_exercises:
            return {
                "user_id": user.id,
                "goal": profile.goal.name if profile.goal else "N/A",
                "level": profile.level.name if profile.level else "N/A",
                "volume": "N/A",
                "sets": 0,
                "reps": "N/A",
                "rest": "N/A",
                "method_name": "N/A",
                "exercises": [],
                "message": "No se encontraron ejercicios compatibles con tu perfil, equipamiento o salud."
            }

        # Obtener las reglas de programación para el objetivo y nivel del usuario
        goal_code = profile.goal.code if profile.goal else "PG"
        level_code = profile.level.code if profile.level else "NIV1"

        matrix_rule = db.query(ProgrammingMatrix).filter(
            ProgrammingMatrix.goal_code == goal_code,
            ProgrammingMatrix.level_code == level_code
        ).first()

        # Valores por defecto en caso de no encontrarse una regla en la matriz
        volume = matrix_rule.volume if matrix_rule else "Medio"
        sets = matrix_rule.sets if matrix_rule else 3
        reps = matrix_rule.reps if matrix_rule else "12 reps"
        rest = matrix_rule.rest if matrix_rule else "60s"
        method_name = matrix_rule.method.name if (matrix_rule and matrix_rule.method) else "Series Tradicionales"

        # Determinar cantidad de ejercicios según la duración elegida
        duration_code = (user.session_duration_code or "").upper()
        if duration_code == "EXPRESS":
            num_exercises = 3
        elif duration_code == "STANDARD":
            num_exercises = 5
        elif duration_code == "EXTENDED":
            num_exercises = 7
        else:
            num_exercises = 4  # Para VARIABLE o None

        sample_size = min(len(viable_exercises), num_exercises)

        if day is not None:
            # Sembrar el generador aleatorio para que el día siempre dé la misma rutina al mismo usuario
            local_random = random.Random(f"{user.id}_{day}")
            selected_sample = local_random.sample(viable_exercises, sample_size)
        else:
            selected_sample = random.sample(viable_exercises, sample_size)

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

        return {
            "user_id": user.id,
            "goal": profile.goal.name if profile.goal else "N/A",
            "level": profile.level.name if profile.level else "N/A",
            "volume": volume,
            "sets": sets,
            "reps": reps,
            "rest": rest,
            "method_name": method_name,
            "day": day,
            "exercises": routine_exercises
        }

routine_generator = RoutineGenerator()
