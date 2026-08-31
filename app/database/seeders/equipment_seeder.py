from pathlib import Path

from sqlalchemy.orm import Session

from app.database.seeders.base_seeder import BaseSeeder
from app.models import Equipment


class EquipmentSeeder(BaseSeeder):
    def __init__(self, session: Session, data_dir: Path):
        super().__init__(session, data_dir)
        self.equip_map = {}

    def seed(self) -> None:
        print("Seeding equipment with CDN images and bilingual names from TSV...")
        file_path = self.data_dir / "equipments.tsv"
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "\t" not in line_str or line_str.startswith("code\t"):
                    continue
                cols = [c.strip() for c in line_str.split("\t")]
                name_en = cols[1]
                name_es = cols[2] if len(cols) > 2 else name_en
                image_url = cols[3] if len(cols) > 3 else None

                eq = Equipment(name=name_en, name_es=name_es, image_url=image_url)
                self.session.add(eq)
                self.equip_map[name_en] = eq
                if name_es:
                    self.equip_map[name_es] = eq

        ex_file = self.data_dir / "exercises.tsv"
        unique_names = self._extract_unique_equipment_names(ex_file)
        for name in sorted(list(unique_names)):
            if name not in self.equip_map:
                eq = Equipment(name=name, name_es=name, image_url=None)
                self.session.add(eq)
                self.equip_map[name] = eq

        self.session.commit()
        for name, eq in self.equip_map.items():
            self.session.refresh(eq)
        print(f"Seeded {len(self.equip_map)} equipment mappings from TSV.")

    def _extract_unique_equipment_names(self, file_path: Path) -> set:
        unique_names = set()
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or "	" not in line_str:
                    continue
                cols = [col.strip() for col in line_str.split("	")]
                if len(cols) > 4 and cols[4]:
                    name = cols[4].strip()
                    if name not in ["Ninguna", "Ninguno", "Ningún", ""]:
                        unique_names.add(name)
                if len(cols) > 5 and cols[5]:
                    name = cols[5].strip()
                    if name not in ["Ninguna", "Ninguno", "Ningún", ""]:
                        unique_names.add(name)
        return unique_names
