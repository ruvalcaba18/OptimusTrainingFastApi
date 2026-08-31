from typing import List, final

from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.models.excersice.everyday_item import EverydayItem
from app.services.excersice.everyday_item_service import everyday_item_service


@final 
class EveryDayItemController:
    
    def list_everyday_item_controller(db: Session) -> List[EverydayItem]:
        return everyday_item_service.list_everyday_item(db=db)


everyday_item_controller = EveryDayItemController()    