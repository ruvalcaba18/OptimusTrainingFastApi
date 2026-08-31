from typing import List, final

from sqlalchemy.orm import Session

from app.core.error_handlers import handle_controller_errors
from app.models.excersice.workout_hybrid_places import WorkoutHybridPlaces
from app.services.excersice.workout_hybird_places_service import (
   workout_hybrid_places_service,
)


@final
class WorkOutHybridPlacesController:
    
   @staticmethod
   @handle_controller_errors
   def list_workout_hybrid_places(db: Session) -> List[WorkoutHybridPlaces]:
       return workout_hybrid_places_service.list_workout_hybrid_places(db)

workou_hybrid_places_controller = WorkOutHybridPlacesController()   