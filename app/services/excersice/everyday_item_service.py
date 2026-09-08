from typing import final

from sqlalchemy.orm import Session

from app.models.excersice.everyday_item import EverydayItem


@final 
class EverydayItemService:
    
    def list_everyday_item(self,db: Session) -> list[EverydayItem]:
        return db.query(EverydayItem).order_by(EverydayItem.id).all()

everyday_item_service = EverydayItemService()    