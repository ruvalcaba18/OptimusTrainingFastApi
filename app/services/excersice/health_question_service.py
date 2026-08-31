from typing import List

from sqlalchemy.orm import Session

from app.models.excersice.health_question import HealthQuestionModel


class HealthQuestionService:
    def list_health_questions(self, db: Session) -> List[HealthQuestionModel]:
        return db.query(HealthQuestionModel).order_by(HealthQuestionModel.id).all()

health_question_service = HealthQuestionService()
