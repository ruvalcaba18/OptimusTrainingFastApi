import re
from pathlib import Path

from sqlalchemy.orm import Session

from app.database.seeders.base_seeder import BaseSeeder
from app.models import Condition, Goal, Level, Method


class CatalogsSeeder(BaseSeeder):
    def __init__(self, session: Session, data_dir: Path):
        super().__init__(session, data_dir)
        self.levels_map = {}
        self.goals_map = {}
        self.conditions_map = {}

    def seed(self) -> None:
        self.seed_levels()
        self.seed_goals()
        self.seed_conditions()
        self.seed_methods()

    def seed_levels(self):
        print("Seeding levels...")
        file_path = self.data_dir / "levels.tsv"
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "	" not in line_str:
                    continue
                cols = line_str.split("	")
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
                if not line_str or "	" not in line_str:
                    continue
                cols = line_str.split("	")
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
        spine_codes = {"PAT002", "PAT001", "PAT010"}
        disease_codes = {"ENF003", "ENF002", "ENF005", "ENF001"}
        joint_codes = {"PAT007", "PAT008", "PAT009"}
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "	" not in line_str:
                    continue
                cols = line_str.split("	")
                code = cols[0].strip()
                name = cols[1].strip()
                category = cols[2].strip() if len(cols) > 2 and cols[2].strip() else None
                cond_type = cols[3].strip() if len(cols) > 3 else "PATHOLOGY"
                warning_msg = None
                if code in spine_codes:
                    warning_msg = "Hemos detectado sensibilidad en tu columna; adaptaremos tu plan con alternativas seguras y limitaremos cargas axiales directas."
                elif code in disease_codes or code in joint_codes:
                    warning_msg = "Adaptaremos tu plan para que sea de bajo impacto, protegiendo tus articulaciones y sistema cardiovascular."
                cond = Condition(code=code, name=name, type=cond_type, category=category, warning_message=warning_msg)
                self.session.add(cond)
                self.conditions_map[code] = cond
        self.session.commit()

    def seed_methods(self):
        print("Seeding training methods...")
        file_path = self.data_dir / "methods.tsv"
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "	" not in line_str:
                    continue
                cols = line_str.split("	")
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
                    code=code, name=name, category=category, type=type_name,
                    level=level_str, complexity=complexity, intensity=intensity, tempo=tempo
                )
                if goals_str:
                    g_codes = [g.strip() for g in goals_str.split(",") if g.strip()]
                    for g_code in g_codes:
                        if g_code in self.goals_map:
                            method.goals.append(self.goals_map[g_code])
                self.session.add(method)
        self.session.commit()
