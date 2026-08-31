from typing import List, final

from sqlalchemy.orm import Session

from app.models.excersice.workout_place import WorkoutPlace


@final 
class WorkoutPlaceService: 
    
    def list_workout_place(self, db: Session)-> List[WorkoutPlace]:
        return db.query(WorkoutPlace).order_by(WorkoutPlace.id).all()
 
workout_place_service = WorkoutPlaceService()   