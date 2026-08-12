import re
from typing import final
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
from app.models import SessionDuration
from app.models import WorkoutPlace
from app.models import WorkoutHybridPlaces
from app.models import EverydayItem
from app.models import GymEquipmentModel, HomeEquipmentModel, OutdoorEquipmentModel
from app.models.Enums.GymEquipment import GymEquipment
from app.models.Enums.HomeEquipment import HomeEquipment
from app.models.Enums.OutdoorEquipment import OutdoorEquipment
from app.models.Enums.EverydayItems import EverydayItems

@final
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
        self.seed_session_durations()
        self.seed_workout_places()
        self.seed_workout_hybrid_places()
        self.seed_everyday_items()
        self.seed_gym_equipment()
        self.seed_home_equipment()
        self.seed_outdoor_equipment()
        
        if include_matrix:
            self.seed_programming_matrix()

    def clear_database(self):
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
        self.session.query(SessionDuration).delete()
        self.session.query(WorkoutPlace).delete()
        self.session.query(WorkoutHybridPlaces).delete()
        self.session.query(EverydayItem).delete()
        self.session.query(GymEquipmentModel).delete()
        self.session.query(HomeEquipmentModel).delete()
        self.session.query(OutdoorEquipmentModel).delete()
        
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
        

    def seed_session_durations(self):
        print("Seeding session durations...")
        data = [
            ("EXPRESS",  "Express (15-30 min)",   "Sesiones rápidas y de alta intensidad."),
            ("STANDARD", "Estándar (45-60 min)",   "El tiempo ideal para un entrenamiento completo."),
            ("EXTENDED", "Extendido (90+ min)",     "Para quienes disfrutan de sesiones largas y detalladas."),
            ("VARIABLE", "Variable",               "Mi tiempo cambia cada día y necesito flexibilidad."),
        ]
        for code, name, description in data:
            self.session.add(SessionDuration(code=code, name=name, description=description))
        self.session.commit()
    
    
    def seed_workout_hybrid_places(self):
        
        data = [
            ("GYM", "Gimnasio" , "Haz pagado el gimnasio o deseas ir a un gimnasio"),
            ("HOUSE", "Casa", "Deseas hacer ejercicio en casa"),
            ("FREE", "Aire Libre", "Deseas hacer ejercicio al aire libre o mixto")
        ]    
        
        for code, name , description in data:
            self.session.add(WorkoutHybridPlaces(code=code, name=name, description=description))
        self.session.commit()

    def seed_workout_places(self):
        print("Seeding workout places...")
        data = [
            ("gimnasio", "Gimnasio completo", "Tengo acceso a máquinas, pesas y racks."),
            ("casa",     "En casa",           "Entrenaré en mi hogar, con o sin equipo."),
            ("afuera",   "Al aire libre",     "Prefiero parques, pistas o barras al aire libre."),
            ("mixto",    "Híbrido",           "Combinaré diferentes lugares (casa, gym o parque)."),
        ]
        for code, name, description in data:
            self.session.add(WorkoutPlace(code=code, name=name, description=description))
        self.session.commit()
        
    def seed_everyday_items(self):
        print("Seeding everyday items...")
        mappings = {
            EverydayItems.CHAIR: ("chair", "Silla de comedor o cualquier tipo de silla que se tenga en casa", "Silla,Banco"),
            EverydayItems.WATER_JUGS: ("waterJugs", "Cualquier tipo de garrafón es bueno incluso si no se tiene uno de 5 o 20 litros", "Garrafón,Peso"),
            EverydayItems.LOADED_BACKPACK: ("loadedBackpack", "Puedes cargarla de cualquier tipo de cosa en caso de no tener libros o arroz.", "Mochila,Peso"),
            EverydayItems.TOWELS: ("towels", "Cualquier tipo de toalla de cualquier tamaño", "Toalla"),
            EverydayItems.BROOMSTICK: ("broomstick", "O cualquier tipo de palo que te ayude a hacer ejercicio.", "Palo"),
            EverydayItems.STAIRS: ("stairs", " o cualquier parte que esté un poco elevada que te ayude a subir y bajar.", "Escalón"),
            EverydayItems.SOFA: ("sofa", "Sofá o Sillón", "Sofá"),
            EverydayItems.DETERGENT_BOTTLES: ("detergentBottles", "o botellas de agua", "Detergente,Peso"),
            EverydayItems.THICK_BOOKS: ("thickBooks", "o cualquier tipo de libro", "Libros,Peso"),
            EverydayItems.CLEAR_WALL: ("clearWall", "Pared Despejada", "Pared")
        }
        for enum_val, (code, description, mapping) in mappings.items():
            self.session.add(EverydayItem(code=code, name=enum_val.value, description=description, mapping=mapping))
        self.session.commit()

    def seed_gym_equipment(self):
        print("Seeding gym equipment...")
        mappings = {
            GymEquipment.DUMBBELLS: ("dumbbells", "Mancuernas,Mancuerna"),
            GymEquipment.MACHINES: ("machines", "Máquina"),
            GymEquipment.CABLES: ("cables", "Polea"),
            GymEquipment.RACKS: ("racks", "Smith,Máquina Smith"),
            GymEquipment.BARBELL: ("barbell", "Barra"),
            GymEquipment.PLYO_BOX: ("plyoBox", "Cajón Pliométrico"),
            GymEquipment.HEAVY_BAG: ("heavyBag", "Costal"),
            GymEquipment.ASSAULT_BIKE: ("assaultBike", "Bicicleta"),
            GymEquipment.BENCHES: ("benches", "Banco"),
            GymEquipment.KETTLEBELLS: ("kettlebells", "Kettlebell")
        }
        for enum_val, (code, mapping) in mappings.items():
            self.session.add(GymEquipmentModel(code=code, name=enum_val.value, mapping=mapping))
        self.session.commit()

    def seed_home_equipment(self):
        print("Seeding home equipment...")
        mappings = {
            HomeEquipment.RESISTANCE_BANDS: ("resistanceBands", "Banda"),
            HomeEquipment.MINI_BANDS: ("miniBands", "Banda"),
            HomeEquipment.ADJUSTABLE_DUMBBELLS: ("adjustableDumbbells", "Mancuernas,Mancuerna"),
            HomeEquipment.JUMP_ROPE: ("jumpRope", "Cuerda"),
            HomeEquipment.PULLUP_RACK: ("pullupRack", "Smith"),
            HomeEquipment.PULLUP_BAR: ("pullupBar", "Barra"),
            HomeEquipment.YOGA_MAT: ("yogaMat", "Colchoneta"),
            HomeEquipment.AB_WHEEL: ("abWheel", "Rueda"),
            HomeEquipment.ANKLE_WEIGHTS: ("ankleWeights", "Peso"),
            HomeEquipment.SWISS_BALL: ("swissBall", "Pelota")
        }
        for enum_val, (code, mapping) in mappings.items():
            self.session.add(HomeEquipmentModel(code=code, name=enum_val.value, mapping=mapping))
        self.session.commit()

    def seed_outdoor_equipment(self):
        print("Seeding outdoor equipment...")
        mappings = {
            OutdoorEquipment.TRACK: ("track", "Pista"),
            OutdoorEquipment.PULLUP_BARS: ("pullupBars", "Barra"),
            OutdoorEquipment.PARALLEL_BARS: ("parallelBars", "Paralelas"),
            OutdoorEquipment.CONCRETE_BENCHES: ("concreteBenches", "Banco"),
            OutdoorEquipment.MONKEY_BARS: ("monkeyBars", "Pasamanos"),
            OutdoorEquipment.HILLS: ("hills", "Cuesta"),
            OutdoorEquipment.BLEACHERS: ("bleachers", "Gradas"),
            OutdoorEquipment.RINGS: ("rings", "Anillas"),
            OutdoorEquipment.LOW_WALLS: ("lowWalls", "Pared"),
            OutdoorEquipment.SAND: ("sand", "Arena")
        }
        for enum_val, (code, mapping) in mappings.items():
            self.session.add(OutdoorEquipmentModel(code=code, name=enum_val.value, mapping=mapping))
        self.session.commit()

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
