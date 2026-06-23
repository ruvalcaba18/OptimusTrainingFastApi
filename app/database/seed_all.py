import re
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.level import Level
from app.models.goal import Goal
from app.models.condition import Condition, ExcersiceCondition
from app.models.method import Method
from app.models.excersices import Excersice
from app.models.Enums.ExcersicePattern import ExcersicePattern

def extract_condition_codes(text):
    if not text:
        return []
    return re.findall(r'[A-Z]{3}\d{3}', text)

def clear_database(session: Session):
    print("Cleaning up existing tables...")
    session.query(ExcersiceCondition).delete()
    session.query(Excersice).delete()
    session.query(Method).delete()
    session.query(Condition).delete()
    session.query(Goal).delete()
    session.query(Level).delete()
    session.commit()

def seed_levels(session: Session, data_dir: Path) -> dict:
    print("Seeding levels...")
    levels_map = {}
    file_path = data_dir / "levels.tsv"
    
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
            session.add(lvl)
            levels_map[code] = lvl
            
    session.commit()
    return levels_map

def seed_goals(session: Session, data_dir: Path) -> dict:
    print("Seeding goals...")
    goals_map = {}
    file_path = data_dir / "goals.tsv"
    
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
            session.add(goal)
            goals_map[code] = goal
            
    session.commit()
    return goals_map

def seed_conditions(session: Session, data_dir: Path) -> dict:
    print("Seeding pathologies and diseases...")
    conditions_map = {}
    file_path = data_dir / "conditions.tsv"
    
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
            session.add(cond)
            conditions_map[code] = cond
            
    session.commit()
    return conditions_map

def seed_methods(session: Session, goals_map: dict, data_dir: Path):
    print("Seeding training methods...")
    file_path = data_dir / "methods.tsv"
    
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
            
            # Associate goals
            if goals_str:
                g_codes = [g.strip() for g in goals_str.split(",") if g.strip()]
                for g_code in g_codes:
                    if g_code in goals_map:
                        method.goals.append(goals_map[g_code])
                        
            session.add(method)
            
    session.commit()

def seed_exercises(session: Session, goals_map: dict, conditions_map: dict, data_dir: Path):
    print("Seeding exercises and their relationships (Phase 2 & 3)...")
    file_path = data_dir / "exercises.tsv"
    ex_count = 0
    
    valid_patterns = {member.value: member for member in ExcersicePattern}
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str or "\t" not in line_str:
                continue
            cols = [col.strip() for col in line_str.split("\t")]
            code = cols[0]
            
            # Read columns
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
            
            # Bridge tables columns (Phase 2)
            compat_str = cols[12] if len(cols) > 12 else ""
            caution_str = cols[13] if len(cols) > 13 else ""
            forbidden_str = cols[14] if len(cols) > 14 else ""
            
            if secondary_tool in ["Ninguna", "Ninguno", "Ningún"]:
                secondary_tool = None
                
            # Normalize pattern spellings
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
                    pattern_enum = matched_pattern
                else:
                    raise ValueError(f"Invalid pattern '{pattern_str}' for exercise {code}")
            else:
                pattern_enum = valid_patterns[pattern_str]
                
            ex = Excersice(
                code=code,
                name=name,
                muscle_group=muscle_group,
                pattern=pattern_enum,
                primary_tool=primary_tool,
                secondary_tool=secondary_tool,
                location=location,
                complexity=complexity,
                level=level_str,
                fatigue=fatigue,
                category=category
            )
            
            # Phase 3: Goals mapping
            if goals_str:
                g_codes = [g.strip() for g in goals_str.replace("-", ",").split(",") if g.strip()]
                for g_code in g_codes:
                    if g_code in goals_map:
                        ex.goals.append(goals_map[g_code])
                        
            session.add(ex)
            session.flush() # Flush to get exercise ID
            
            # Phase 2: Excersice conditions mapping
            # Compatibles
            compat_codes = extract_condition_codes(compat_str)
            for c_code in compat_codes:
                if c_code in conditions_map:
                    rel_obj = ExcersiceCondition(
                        excersice_id=ex.id,
                        condition_id=conditions_map[c_code].id,
                        relationship="COMPATIBLE"
                    )
                    session.add(rel_obj)
                    
            # Caution
            caution_codes = extract_condition_codes(caution_str)
            for c_code in caution_codes:
                if c_code in conditions_map:
                    rel_obj = ExcersiceCondition(
                        excersice_id=ex.id,
                        condition_id=conditions_map[c_code].id,
                        relationship="CAUTION"
                    )
                    session.add(rel_obj)
                    
            # Forbidden
            forbidden_codes = extract_condition_codes(forbidden_str)
            for c_code in forbidden_codes:
                if c_code in conditions_map:
                    rel_obj = ExcersiceCondition(
                        excersice_id=ex.id,
                        condition_id=conditions_map[c_code].id,
                        relationship="FORBIDDEN"
                    )
                    session.add(rel_obj)
                    
            ex_count += 1
            
    session.commit()
    print(f"Successfully seeded {ex_count} exercises!")

def seed_database():
    data_dir = Path(__file__).parent / "data"
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found at: {data_dir}")
        
    session = SessionLocal()
    try:
        clear_database(session)
        levels_map = seed_levels(session, data_dir)
        goals_map = seed_goals(session, data_dir)
        conditions_map = seed_conditions(session, data_dir)
        seed_methods(session, goals_map, data_dir)
        seed_exercises(session, goals_map, conditions_map, data_dir)
        print("Database seeding completed successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error during seeding: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
