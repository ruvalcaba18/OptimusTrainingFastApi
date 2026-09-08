
from sqlalchemy.orm import Session

from app.models import Method


class MethodService:
    def list_methods(self, db: Session, category: str | None = None) -> list[Method]:
        query = db.query(Method)
        if category:
            query = query.filter(Method.category == category)
        return query.order_by(Method.code).all()

method_service = MethodService()
