import re
from pathlib import Path

from sqlalchemy.orm import Session

from app.database.seeders.base_seeder import BaseSeeder
from app.models import (
    Excersice,
    ExcersiceCondition,
    ExcersiceEquipment,
    ExcersiceMuscle,
)
from app.models.Enums.ExcersicePattern import ExcersicePattern


class ExercisesSeeder(BaseSeeder):
    def __init__(self, session: Session, data_dir: Path, goals_map: dict, conditions_map: dict, equip_map: dict, muscles_map: dict):
        super().__init__(session, data_dir)
        self.goals_map = goals_map
        self.conditions_map = conditions_map
        self.equip_map = equip_map
        self.muscles_map = muscles_map

    def seed(self) -> None:
        print("Seeding exercises and their relationships...")
        self._seed_base_exercises()
        self._seed_exercisedb_exercises()

    def _seed_base_exercises(self):
        file_path = self.data_dir / "exercises.tsv"
        ex_count = 0
        valid_patterns = {member.value: member for member in ExcersicePattern}

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str:
                    continue
                cols = [col.strip() for col in line_str.split("\t")]
                code = cols[0]
                muscle_group = cols[1]
                name = cols[2]
                pattern_str = cols[3]
                primary_tool = cols[4]
                secondary_tool = cols[5] if len(cols) > 5 and cols[5] else None
                location = cols[6]
                complexity = cols[7]
                level_str = cols[8]
                fatigue = cols[9]
                goals_str = cols[10] if len(cols) > 10 else ""
                category = cols[11] if len(cols) > 11 else ""
                compat_str = cols[12] if len(cols) > 12 else ""
                caution_str = cols[13] if len(cols) > 13 else ""
                forbidden_str = cols[14] if len(cols) > 14 else ""

                if secondary_tool in ["Ninguna", "Ninguno", "Ningún"]:
                    secondary_tool = None

                pattern_enum = self._normalize_pattern(pattern_str, valid_patterns, code)

                ex = Excersice(
                    code=code, name=name, muscle_group=muscle_group, pattern=pattern_enum,
                    location=location, complexity=complexity, level=level_str, fatigue=fatigue, category=category
                )

                self._associate_goals(ex, goals_str)
                self.session.add(ex)
                self.session.flush()

                self._associate_equipment(ex.id, primary_tool, secondary_tool)
                self._associate_conditions(ex.id, compat_str, caution_str, forbidden_str)
                self._associate_muscles(ex.id, muscle_group, pattern_str)
                ex_count += 1

        self.session.commit()
        print(f"Successfully seeded {ex_count} base exercises!")

    def _seed_exercisedb_exercises(self):
        file_path = self.data_dir / "exercisedb_exercises.tsv"
        if not file_path.exists():
            return
        print("Enriching and seeding ExerciseDB exercises with image CDN...")
        valid_patterns = {member.value: member for member in ExcersicePattern}
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str or line_str.startswith("exercise_id\t"):
                    continue
                cols = [col.strip() for col in line_str.split("\t")]
                exercise_id = cols[0]
                code = cols[1]
                name = cols[2]
                image_url = cols[3]
                muscle_group = cols[4]
                pattern_str = cols[5]
                primary_tool = cols[6]
                secondary_tool = cols[7] if len(cols) > 7 and cols[7] != "Ninguna" else None
                location = cols[8]
                complexity = cols[9]
                level_str = cols[10]
                fatigue = cols[11]
                goals_str = cols[12] if len(cols) > 12 else ""
                category = cols[13] if len(cols) > 13 else ""
                compat_str = cols[14] if len(cols) > 14 else ""
                caution_str = cols[15] if len(cols) > 15 else ""
                forbidden_str = cols[16] if len(cols) > 16 else ""
                target_muscles = cols[17] if len(cols) > 17 else ""
                secondary_muscles = cols[18] if len(cols) > 18 else ""

                existing_ex = self.session.query(Excersice).filter(Excersice.code == code).first()
                if existing_ex:
                    existing_ex.exercise_id = exercise_id
                    existing_ex.image_url = image_url
                    ex_id = existing_ex.id
                else:
                    pattern_enum = self._normalize_pattern(pattern_str, valid_patterns, code)
                    ex = Excersice(
                        code=code,
                        exercise_id=exercise_id,
                        name=name,
                        image_url=image_url,
                        muscle_group=muscle_group,
                        pattern=pattern_enum,
                        location=location,
                        complexity=complexity,
                        level=level_str,
                        fatigue=fatigue,
                        category=category
                    )
                    self._associate_goals(ex, goals_str)
                    self.session.add(ex)
                    self.session.flush()
                    self._associate_equipment(ex.id, primary_tool, secondary_tool)
                    self._associate_conditions(ex.id, compat_str, caution_str, forbidden_str)
                    ex_id = ex.id

                # Asociar target muscles y secondary muscles explícitos
                if target_muscles:
                    for tm in [m.strip() for m in target_muscles.split(",") if m.strip()]:
                        muscle = self.muscles_map.get(tm)
                        if muscle:
                            self.session.add(ExcersiceMuscle(excersice_id=ex_id, muscle_id=muscle.id, is_primary=True))
                if secondary_muscles:
                    for sm in [m.strip() for m in secondary_muscles.split(",") if m.strip()]:
                        muscle = self.muscles_map.get(sm)
                        if muscle:
                            self.session.add(ExcersiceMuscle(excersice_id=ex_id, muscle_id=muscle.id, is_primary=False))

        self.session.commit()
        print("ExerciseDB exercises synced successfully.")

    def _normalize_pattern(self, pattern_str: str, valid_patterns: dict, code: str) -> ExcersicePattern:
        if pattern_str == "Extensión de Hombro": pattern_str = "Extensión Hombro"
        elif pattern_str == "Flexión de Hombro": pattern_str = "Flexión Hombro"
        elif pattern_str == "Abducción de Hombro": pattern_str = "Abducción Hombro"
        elif pattern_str == "Locomocion": pattern_str = "Locomoción"

        if pattern_str not in valid_patterns:
            for val, member in valid_patterns.items():
                if val.lower() == pattern_str.lower():
                    return member
            raise ValueError(f"Invalid pattern '{pattern_str}' for exercise {code}")
        return valid_patterns[pattern_str]

    def _associate_goals(self, ex: Excersice, goals_str: str):
        if goals_str:
            g_codes = [g.strip() for g in goals_str.replace("-", ",").split(",") if g.strip()]
            for g_code in g_codes:
                if g_code in self.goals_map:
                    ex.goals.append(self.goals_map[g_code])

    def _associate_equipment(self, ex_id: int, primary_tool: str, secondary_tool: str):
        if primary_tool and primary_tool not in ["Ninguna", "Ninguno", "Ningún", ""] and primary_tool in self.equip_map:
            self.session.add(ExcersiceEquipment(excersice_id=ex_id, equipment_id=self.equip_map[primary_tool].id, is_primary=True))
        if secondary_tool and secondary_tool not in ["Ninguna", "Ninguno", "Ningún", ""] and secondary_tool in self.equip_map:
            self.session.add(ExcersiceEquipment(excersice_id=ex_id, equipment_id=self.equip_map[secondary_tool].id, is_primary=False))

    def _associate_conditions(self, ex_id: int, compat_str: str, caution_str: str, forbidden_str: str):
        for c_code in re.findall(r'[A-Z]{3}\d{3}', compat_str or ""):
            if c_code in self.conditions_map:
                self.session.add(ExcersiceCondition(excersice_id=ex_id, condition_id=self.conditions_map[c_code].id, relationship="COMPATIBLE"))
        for c_code in re.findall(r'[A-Z]{3}\d{3}', caution_str or ""):
            if c_code in self.conditions_map:
                self.session.add(ExcersiceCondition(excersice_id=ex_id, condition_id=self.conditions_map[c_code].id, relationship="CAUTION"))
        for c_code in re.findall(r'[A-Z]{3}\d{3}', forbidden_str or ""):
            if c_code in self.conditions_map:
                self.session.add(ExcersiceCondition(excersice_id=ex_id, condition_id=self.conditions_map[c_code].id, relationship="FORBIDDEN"))

    def _associate_muscles(self, ex_id: int, muscle_group: str, pattern: str):
        mg_mapping = {
            "Pierna": ["QUADRICEPS", "HAMSTRINGS", "GLUTEUS MAXIMUS", "GASTROCNEMIUS", "SOLEUS"],
            "Espalda": ["LATISSIMUS DORSI", "TRAPEZIUS MIDDLE FIBERS", "ERECTOR SPINAE", "TERES MAJOR"],
            "Pecho": ["PECTORALIS MAJOR STERNAL HEAD", "PECTORALIS MAJOR CLAVICULAR HEAD", "ANTERIOR DELTOID", "TRICEPS BRACHII"],
            "Hombro": ["ANTERIOR DELTOID", "LATERAL DELTOID", "POSTERIOR DELTOID", "TRAPEZIUS UPPER FIBERS"],
            "Bíceps": ["BICEPS BRACHII", "BRACHIALIS", "BRACHIORADIALIS"],
            "Tríceps": ["TRICEPS BRACHII", "WRIST EXTENSORS"],
            "Brazo General": ["BICEPS BRACHII", "TRICEPS BRACHII", "BRACHIALIS", "BRACHIORADIALIS"],
            "Abdomen": ["RECTUS ABDOMINIS", "OBLIQUES", "TRANSVERSUS ABDOMINIS"],
            "Resistencia": ["QUADRICEPS", "HAMSTRINGS", "GASTROCNEMIUS", "GLUTEUS MAXIMUS", "RECTUS ABDOMINIS"]
        }
        for idx, m_name in enumerate(mg_mapping.get(muscle_group, [])):
            muscle = self.muscles_map.get(m_name)
            if muscle:
                self.session.add(ExcersiceMuscle(excersice_id=ex_id, muscle_id=muscle.id, is_primary=(idx == 0)))
