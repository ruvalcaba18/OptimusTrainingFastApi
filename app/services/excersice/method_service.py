from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Method


class MethodService:
    def list_methods(self, db: Session, category: Optional[str] = None) -> List[Method]:
        query = db.query(Method)
        if category:
            query = query.filter(Method.category == category)
        return query.order_by(Method.code).all()

method_service = MethodService()
