from pathlib import Path

from sqlalchemy.orm import Session

from app.database.seeders.base_seeder import BaseSeeder
from app.models import BodyPart, ExerciseType, Muscle


class AnatomySeeder(BaseSeeder):
    def __init__(self, session: Session, data_dir: Path):
        super().__init__(session, data_dir)
        self.muscles_map = {}

    def seed(self) -> None:
        self.seed_body_parts()
        self.seed_exercise_types()
        self.seed_muscles()

    def seed_body_parts(self):
        print("Seeding body parts from TSV...")
        file_path = self.data_dir / "body_parts.tsv"
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str or line_str.startswith("code\t"):
                    continue
                cols = [c.strip() for c in line_str.split("\t")]
                code = cols[0]
                name_en = cols[1]
                name_es = cols[2] if len(cols) > 2 else name_en
                image_url = cols[3] if len(cols) > 3 else None

                bp = BodyPart(code=code, name_en=name_en, name_es=name_es, image_url=image_url)
                self.session.add(bp)
        self.session.commit()
        print("Seeded body parts successfully from TSV.")

    def seed_exercise_types(self):
        print("Seeding exercise types from TSV...")
        file_path = self.data_dir / "exercise_types.tsv"
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str or line_str.startswith("code\t"):
                    continue
                cols = [c.strip() for c in line_str.split("\t")]
                code = cols[0]
                name_en = cols[1]
                name_es = cols[2] if len(cols) > 2 else name_en
                image_url = cols[3] if len(cols) > 3 else None

                et = ExerciseType(code=code, name_en=name_en, name_es=name_es, image_url=image_url)
                self.session.add(et)
        self.session.commit()
        print("Seeded exercise types successfully from TSV.")

    def seed_muscles(self):
        print("Seeding anatomical muscles from TSV...")
        file_path = self.data_dir / "muscles.tsv"
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str or line_str.startswith("code\t"):
                    continue
                cols = [c.strip() for c in line_str.split("\t")]
                code = cols[0]
                name = cols[1]
                common_name = cols[2] if len(cols) > 2 else None
                body_part = cols[3] if len(cols) > 3 else "Other"

                muscle = Muscle(code=code, name=name, common_name=common_name, body_part=body_part)
                self.session.add(muscle)
                self.muscles_map[name] = muscle
        self.session.commit()
        print(f"Seeded {len(self.muscles_map)} anatomical muscles from TSV.")
