import re
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Level
from app.models import Goal
from app.models import Condition, ExcersiceCondition
from app.models import Method
from app.models import Excersice
from app.models.Enums.ExcersicePattern import ExcersicePattern
from app.models import Equipment
from app.models import ExcersiceEquipment
from app.models import ProgrammingMatrix
from app.models import ExcersiceGoal
from app.models import MethodGoal

class DatabaseSeeder:
    def __init__(self, session: Session, data_dir: Path):
        self.session = session
        self.data_dir = data_dir
        self.levels_map = {}
        self.goals_map = {}
        self.conditions_map = {}
        self.equip_map = {}

    def seed_all(self, include_matrix: bool = True):
        self.clear_database()
        self.seed_levels()
        self.seed_goals()
        self.seed_conditions()
        self.seed_equipment()
        self.seed_methods()
        self.seed_exercises()
        if include_matrix:
            self.seed_programming_matrix()

    def clear_database(self):
        print("Cleaning up existing tables...")
        self.session.query(ExcersiceCondition).delete()
        self.session.query(ExcersiceEquipment).delete()
        self.session.query(ExcersiceGoal).delete()
        self.session.query(MethodGoal).delete()
        self.session.query(Excersice).delete()
        self.session.query(Method).delete()
        self.session.query(Condition).delete()
        self.session.query(Goal).delete()
        self.session.query(Level).delete()
        self.session.query(Equipment).delete()
        self.session.query(ProgrammingMatrix).delete()
        self.session.commit()

    def seed_levels(self):
        print("Seeding levels...")
        file_path = self.data_dir / "levels.tsv"
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str:
                    continue
                cols = line_str.split("\t")
                code = cols[0].strip()
                name = cols[1].strip()
                description = cols[2].strip() if len(cols) > 2 else ""
                
                lvl = Level(code=code, name=name, description=description)
                self.session.add(lvl)
                self.levels_map[code] = lvl
                
        self.session.commit()

    def seed_goals(self):
        print("Seeding goals...")
        file_path = self.data_dir / "goals.tsv"
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str:
                    continue
                cols = line_str.split("\t")
                code = cols[0].strip()
                name = cols[1].strip()
                description = cols[2].strip() if len(cols) > 2 else ""
                
                goal = Goal(code=code, name=name, description=description)
                self.session.add(goal)
                self.goals_map[code] = goal
        self.session.commit()

    def seed_conditions(self):
        print("Seeding pathologies and diseases...")
        file_path = self.data_dir / "conditions.tsv"
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str:
                    continue
                cols = line_str.split("\t")
                code = cols[0].strip()
                name = cols[1].strip()
                category = cols[2].strip() if len(cols) > 2 and cols[2].strip() else None
                cond_type = cols[3].strip() if len(cols) > 3 else "PATHOLOGY"
                
                cond = Condition(code=code, name=name, type=cond_type, category=category)
                self.session.add(cond)
                self.conditions_map[code] = cond
        self.session.commit()

    def seed_methods(self):
        print("Seeding training methods...")
        file_path = self.data_dir / "methods.tsv"
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str:
                    continue
                cols = line_str.split("\t")
                code = cols[0].strip()
                name = cols[1].strip()
                category = cols[2].strip()
                type_name = cols[3].strip()
                level_str = cols[4].strip()
                complexity = cols[5].strip()
                intensity = cols[6].strip() if len(cols) > 6 and cols[6].strip() else None
                tempo = cols[7].strip() if len(cols) > 7 and cols[7].strip() else None
                goals_str = cols[8].strip() if len(cols) > 8 and cols[8].strip() else None
                
                method = Method(
                    code=code,
                    name=name,
                    category=category,
                    type=type_name,
                    level=level_str,
                    complexity=complexity,
                    intensity=intensity,
                    tempo=tempo
                )
                
                if goals_str:
                    g_codes = [g.strip() for g in goals_str.split(",") if g.strip()]
                    for g_code in g_codes:
                        if g_code in self.goals_map:
                            method.goals.append(self.goals_map[g_code])
                            
                self.session.add(method)
        self.session.commit()

    def _extract_unique_equipment_names(self, file_path: Path) -> set:
        unique_names = set()
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str:
                    continue
                cols = [col.strip() for col in line_str.split("\t")]
                if len(cols) > 4 and cols[4]:
                    name = cols[4].strip()
                    if name not in ["Ninguna", "Ninguno", "Ningún", ""]:
                        unique_names.add(name)
                if len(cols) > 5 and cols[5]:
                    name = cols[5].strip()
                    if name not in ["Ninguna", "Ninguno", "Ningún", ""]:
                        unique_names.add(name)
        return unique_names

    def _save_equipment_to_db(self, unique_names: set):
        for name in sorted(list(unique_names)):
            eq = Equipment(name=name)
            self.session.add(eq)
            self.equip_map[name] = eq
        self.session.commit()
        for name, eq in self.equip_map.items():
            self.session.refresh(eq)

    def seed_equipment(self):
        print("Seeding equipment...")
        file_path = self.data_dir / "exercises.tsv"
        unique_names = self._extract_unique_equipment_names(file_path)
        self._save_equipment_to_db(unique_names)
        print(f"Seeded {len(self.equip_map)} unique equipment items.")

    def _extract_condition_codes(self, text: str) -> list:
        if not text:
            return []
        return re.findall(r'[A-Z]{3}\d{3}', text)

    def _normalize_pattern(self,
                           pattern_str: str, 
                           valid_patterns: dict, 
                           code: str) -> ExcersicePattern:
        
        if pattern_str == "Extensión de Hombro":
            pattern_str = "Extensión Hombro"
        elif pattern_str == "Flexión de Hombro":
            pattern_str = "Flexión Hombro"
        elif pattern_str == "Abducción de Hombro":
            pattern_str = "Abducción Hombro"
        elif pattern_str == "Locomocion":
            pattern_str = "Locomoción"
            
        if pattern_str not in valid_patterns:
            matched_pattern = None
            for val, member in valid_patterns.items():
                if val.lower() == pattern_str.lower():
                    matched_pattern = member
                    break
            if matched_pattern:
                return matched_pattern
            raise ValueError(f"Invalid pattern '{pattern_str}' for exercise {code}")
        return valid_patterns[pattern_str]

    def _associate_goals(self, ex: Excersice, goals_str: str):
        if goals_str:
            g_codes = [g.strip() for g in goals_str.replace("-", ",").split(",") if g.strip()]
            for g_code in g_codes:
                if g_code in self.goals_map:
                    ex.goals.append(self.goals_map[g_code])

    def _associate_equipment(self, ex_id: int, primary_tool: str, secondary_tool: str):
        if primary_tool and primary_tool not in ["Ninguna", "Ninguno", "Ningún", ""]:
            if primary_tool in self.equip_map:
                rel_eq = ExcersiceEquipment(
                    excersice_id=ex_id,
                    equipment_id=self.equip_map[primary_tool].id,
                    is_primary=True
                )
                self.session.add(rel_eq)
        if secondary_tool and secondary_tool not in ["Ninguna", "Ninguno", "Ningún", ""]:
            if secondary_tool in self.equip_map:
                rel_eq = ExcersiceEquipment(
                    excersice_id=ex_id,
                    equipment_id=self.equip_map[secondary_tool].id,
                    is_primary=False
                )
                self.session.add(rel_eq)

    def _associate_conditions(self, ex_id: int, compat_str: str, caution_str: str, forbidden_str: str):
        compat_codes = self._extract_condition_codes(compat_str)
        for c_code in compat_codes:
            if c_code in self.conditions_map:
                rel_obj = ExcersiceCondition(
                    excersice_id=ex_id,
                    condition_id=self.conditions_map[c_code].id,
                    relationship="COMPATIBLE"
                )
                self.session.add(rel_obj)
                
        caution_codes = self._extract_condition_codes(caution_str)
        for c_code in caution_codes:
            if c_code in self.conditions_map:
                rel_obj = ExcersiceCondition(
                    excersice_id=ex_id,
                    condition_id=self.conditions_map[c_code].id,
                    relationship="CAUTION"
                )
                self.session.add(rel_obj)
                
        forbidden_codes = self._extract_condition_codes(forbidden_str)
        for c_code in forbidden_codes:
            if c_code in self.conditions_map:
                rel_obj = ExcersiceCondition(
                    excersice_id=ex_id,
                    condition_id=self.conditions_map[c_code].id,
                    relationship="FORBIDDEN"
                )
                self.session.add(rel_obj)

    def seed_exercises(self):
        print("Seeding exercises and their relationships (Phase 2, 3 & 4)...")
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
                    code=code,
                    name=name,
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
                ex_count += 1
                
        self.session.commit()
        print(f"Successfully seeded {ex_count} exercises!")

    def seed_programming_matrix(self):
        print("Seeding programming matrix...")
        methods_by_code = {m.code: m for m in self.session.query(Method).all()}
        
        rules = [
            {"goal": "PG", "level": "NIV1", "volume": "Bajo-Medio", "sets": 3, "reps": "12-15 reps", "rest": "30-45s", "method_code": "FMT008"},
            {"goal": "PG", "level": "NIV2", "volume": "Medio", "sets": 4, "reps": "12-15 reps", "rest": "30s", "method_code": "FMT004"},
            {"goal": "PG", "level": "NIV3", "volume": "Alto", "sets": 4, "reps": "10-12 reps", "rest": "30s", "method_code": "FMT005"},
            {"goal": "PG", "level": "NIV4", "volume": "Muy Alto", "sets": 5, "reps": "10-12 reps", "rest": "30s", "method_code": "FMT005"},
            
            {"goal": "GMM", "level": "NIV1", "volume": "Bajo", "sets": 3, "reps": "10-12 reps", "rest": "60-90s", "method_code": "FMT001"},
            {"goal": "GMM", "level": "NIV2", "volume": "Medio", "sets": 3, "reps": "8-12 reps", "rest": "60-90s", "method_code": "FMT002"},
            {"goal": "GMM", "level": "NIV3", "volume": "Alto", "sets": 4, "reps": "8-12 reps", "rest": "60-90s", "method_code": "FMT006"},
            {"goal": "GMM", "level": "NIV4", "volume": "Muy Alto", "sets": 4, "reps": "6-10 reps", "rest": "90s", "method_code": "FMT007"},
            
            {"goal": "SB", "level": "NIV1", "volume": "Bajo", "sets": 2, "reps": "12-15 reps", "rest": "60s", "method_code": "FMT001"},
            {"goal": "SB", "level": "NIV2", "volume": "Bajo-Medio", "sets": 3, "reps": "12-15 reps", "rest": "60s", "method_code": "FMT001"},
            {"goal": "SB", "level": "NIV3", "volume": "Medio", "sets": 3, "reps": "10-12 reps", "rest": "45-60s", "method_code": "FMT008"},
            {"goal": "SB", "level": "NIV4", "volume": "Medio", "sets": 3, "reps": "10-12 reps", "rest": "45s", "method_code": "FMT008"},
            
            {"goal": "RD", "level": "NIV1", "volume": "Bajo", "sets": 3, "reps": "8-10 reps", "rest": "90-120s", "method_code": "FMT001"},
            {"goal": "RD", "level": "NIV2", "volume": "Medio", "sets": 3, "reps": "6-8 reps", "rest": "120s", "method_code": "FMT003"},
            {"goal": "RD", "level": "NIV3", "volume": "Alto", "sets": 4, "reps": "4-6 reps", "rest": "150-180s", "method_code": "FMT009"},
            {"goal": "RD", "level": "NIV4", "volume": "Muy Alto", "sets": 5, "reps": "1-5 reps", "rest": "180s", "method_code": "FMT009"},
        ]
        
        for r in rules:
            method = methods_by_code.get(r["method_code"])
            pm = ProgrammingMatrix(
                goal_code=r["goal"],
                level_code=r["level"],
                volume=r["volume"],
                sets=r["sets"],
                reps=r["reps"],
                rest=r["rest"],
                method_id=method.id if method else None
            )
            self.session.add(pm)
        self.session.commit()
        
        print("Programming matrix seeded successfully!")

def seed_database():
    data_dir = Path(__file__).parent / "data"
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found at: {data_dir}")
        
    session = SessionLocal()
    try:
        seeder = DatabaseSeeder(session, data_dir)
        seeder.seed_all()
        print("Database seeding completed successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error during seeding: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
