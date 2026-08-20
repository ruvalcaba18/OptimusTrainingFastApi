from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import Excersice
from app.models import Condition, ExcersiceCondition
from app.models import Goal
from app.models import Equipment
from app.models import ExcersiceEquipment
from app.models import User

LEVEL_VALUES = {
    "NIV1": 1,
    "Básico": 1,
    "NIV2": 2,
    "Intermedio": 2,
    "NIV3": 3,
    "Avanzado": 3,
    "NIV4": 4,
    "Alto Rendimiento": 4,
}

class ExerciseSelector:
    
    def select_exercises(self, db: Session, user: User) -> List[Dict[str, Any]]:
        # Intentar utilizar la función optimizada de PostgreSQL
        if db.bind.dialect.name == "postgresql":
            try:
                with db.begin_nested():
                    result = db.execute(
                        text("SELECT * FROM fn_get_viable_exercises(:user_id)"),
                        {"user_id": user.id}
                    ).fetchall()
                    
                    selected_exercises = []
                    for row in result:
                        ex = Excersice(
                            id=row.exercise_id,
                            code=row.exercise_code,
                            name=row.exercise_name,
                            muscle_group=row.muscle_group,
                            pattern=row.pattern,
                            complexity=row.complexity
                        )
                        selected_exercises.append({
                            "exercise": ex,
                            "caution_warnings": row.caution_warnings,
                            "has_caution": len(row.caution_warnings) > 0
                        })
                    return selected_exercises
            except Exception:
                pass

        # Fallback local (SQLite para pruebas y base de datos sin migración)
        profile = user

        exercises = self._get_exercises_by_goal(db, profile.goal_id)

        user_condition_ids = [c.id for c in user.pathologies] + [c.id for c in user.diseases]
        user_equip_ids = {eq.id for eq in user.equipments}

        user_level_code = profile.level.code if profile.level else "NIV1"
        user_level_value = LEVEL_VALUES.get(user_level_code, 1)

        selected_exercises = []

        for ex in exercises:
            if not self._is_level_compatible(ex.level, user_level_value):
                continue

            is_forbidden, caution_warnings = self._evaluate_health_restrictions(db, ex.id, user_condition_ids)
            if is_forbidden:
                continue

            if not self._has_required_equipment(db, ex.id, user_equip_ids):
                continue

            selected_exercises.append({
                "exercise": ex,
                "caution_warnings": caution_warnings,
                "has_caution": len(caution_warnings) > 0
            })

        return selected_exercises

    def _fallback_all_exercises(self, db: Session) -> List[Dict[str, Any]]:
        exercises = db.query(Excersice).all()
        return [{"exercise": ex, "caution_warnings": [], "has_caution": False} for ex in exercises]

    def _get_exercises_by_goal(self, db: Session, goal_id: Optional[int]) -> List[Excersice]:
        query = db.query(Excersice)
        if goal_id:
            query = query.join(Excersice.goals).filter(Goal.id == goal_id)
        return query.all()

    def _is_level_compatible(self, ex_level: str, user_level_value: int) -> bool:
        ex_level_value = LEVEL_VALUES.get(ex_level, 1)
        return ex_level_value <= user_level_value

    def _evaluate_health_restrictions(
        self, db: Session, ex_id: int, user_condition_ids: List[int]
    ) -> Tuple[bool, List[str]]:
        relations = db.query(ExcersiceCondition).filter(
            ExcersiceCondition.excersice_id == ex_id
        ).all()

        is_forbidden = False
        caution_warnings = []
        for rel in relations:
            if rel.condition_id in user_condition_ids:
                if rel.relationship == "FORBIDDEN":
                    is_forbidden = True
                    break
                elif rel.relationship == "CAUTION":
                    cond = db.query(Condition).filter(Condition.id == rel.condition_id).first()
                    if cond:
                        caution_warnings.append(cond.name)

        return is_forbidden, caution_warnings

    def _has_required_equipment(self, db: Session, ex_id: int, user_equip_ids: set[int]) -> bool:
        ex_equip_relations = db.query(ExcersiceEquipment).filter(
            ExcersiceEquipment.excersice_id == ex_id
        ).all()

        for eq_rel in ex_equip_relations:
            if eq_rel.is_primary:
                eq_item = db.query(Equipment).filter(Equipment.id == eq_rel.equipment_id).first()
                if eq_item and eq_item.name not in ["Propio Peso", "Ninguna"]:
                    if eq_item.id not in user_equip_ids:
                        return False
        return True

exercise_selector = ExerciseSelector()
