from sqlalchemy.orm import Session
from typing import List
from app.models.excersice.leisure_activity import LeisureActivityModel

class LeisureActivityService:
    def list_leisure_activities(self, db: Session) -> List[LeisureActivityModel]:
        return db.query(LeisureActivityModel).order_by(LeisureActivityModel.code).all()

leisure_activity_service = LeisureActivityService()
