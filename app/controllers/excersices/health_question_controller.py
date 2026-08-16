from sqlalchemy.orm import Session
from typing import List
from app.services.excersice.health_question_service import health_question_service
from app.models.excersice.health_question import HealthQuestionModel

class HealthQuestionController:
    def list_health_questions(self, db: Session) -> List[HealthQuestionModel]:
        return health_question_service.list_health_questions(db)

health_question_controller = HealthQuestionController()
