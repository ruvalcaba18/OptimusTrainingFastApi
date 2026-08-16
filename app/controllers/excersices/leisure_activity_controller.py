from sqlalchemy.orm import Session
from typing import List
from app.services.excersice.leisure_activity_service import leisure_activity_service
from app.models.excersice.leisure_activity import LeisureActivityModel

class LeisureActivityController:
    def list_leisure_activities(self, db: Session) -> List[LeisureActivityModel]:
        return leisure_activity_service.list_leisure_activities(db)

leisure_activity_controller = LeisureActivityController()
