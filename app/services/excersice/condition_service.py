from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Condition

class ConditionService:
    def list_conditions(self, db: Session, type: Optional[str] = None) -> List[Condition]:
        query = db.query(Condition)
        
        if type:
            query = query.filter(Condition.type == type)
            
        return query.order_by(Condition.code).all()

condition_service = ConditionService()
