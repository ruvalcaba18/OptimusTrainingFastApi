from typing import List, final

from sqlalchemy.orm import Session

from app.models.excersice.workout_hybrid_places import WorkoutHybridPlaces


@final 
class WorkoutHybridPlacesService:
    
    def list_workout_hybrid_places(self, db: Session) ->List[WorkoutHybridPlaces]:
        return db.query(WorkoutHybridPlaces).order_by(WorkoutHybridPlaces.id).all()

workout_hybrid_places_service = WorkoutHybridPlacesService()