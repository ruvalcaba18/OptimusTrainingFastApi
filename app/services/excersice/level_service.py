from typing import List
from sqlalchemy.orm import Session
from app.models import Level

class LevelService:
    def list_levels(self, db: Session) -> List[Level]:
        return db.query(Level).order_by(Level.code).all()

level_service = LevelService()
