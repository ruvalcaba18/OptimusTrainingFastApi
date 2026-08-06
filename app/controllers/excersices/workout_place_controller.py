from typing import List, final
from sqlalchemy import Session 
from app.services.excersice.workout_place_service import workout_place_service
from app.core.error_handlers import handle_controller_errors
from app.models.excersice.workout_place import WorkoutPlace

@final
class WorkoutController: 
    @staticmethod
    @handle_controller_errors
    def list_workout_place(db: Session) -> List[WorkoutPlace]:
        return workout_place_service.list_workout_place(db)

workout_place_controller = WorkoutController()    