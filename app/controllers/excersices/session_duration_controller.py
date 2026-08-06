from typing import List, final
from sqlalchemy.orm import Session
from app.services.excersice.session_duration_service import session_duration_service
from app.models.excersice.session_duration import SessionDuration
from app.core.error_handlers import handle_controller_errors

@final 
class SessionDurationController:
    
    @staticmethod
    @handle_controller_errors
    def list_session_duration(db: Session) -> List[SessionDuration]:
        return session_duration_service.list_session_duration(db)
    
session_duration_controller = SessionDurationController()