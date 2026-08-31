from typing import List

from sqlalchemy.orm import Session

from app.models.excersice.health_question import HealthQuestionModel
from app.services.excersice.health_question_service import health_question_service


class HealthQuestionController:
    def list_health_questions(self, db: Session) -> List[HealthQuestionModel]:
        return health_question_service.list_health_questions(db)

health_question_controller = HealthQuestionController()
