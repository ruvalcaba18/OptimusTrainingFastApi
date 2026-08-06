from typing import List, final
from sqlalchemy.orm import Session
from app.models.excersice.session_duration import SessionDuration

@final
class SessionDurationService:
    
    def list_session_duration(self, db: Session) -> List[SessionDuration]:
        return db.query(SessionDuration).order_by(SessionDuration.code).all() 
    
    
session_duration_service = SessionDurationService()