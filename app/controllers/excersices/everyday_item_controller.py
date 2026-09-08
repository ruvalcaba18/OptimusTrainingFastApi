from typing import final

from sqlalchemy.orm import Session

from app.models.excersice.everyday_item import EverydayItem
from app.services.excersice.everyday_item_service import everyday_item_service


@final 
class EveryDayItemController:
    
    def list_everyday_item_controller(db: Session) -> list[EverydayItem]:
        return everyday_item_service.list_everyday_item(db=db)


everyday_item_controller = EveryDayItemController()    