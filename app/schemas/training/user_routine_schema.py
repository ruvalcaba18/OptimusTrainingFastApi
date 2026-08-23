from pydantic import BaseModel
from typing import List, Dict, Any, Optional, final

@final
class UserRoutineUpdateSchema(BaseModel):
    goal: Optional[str] = None
    level: Optional[str] = None
    volume: Optional[str] = None
    sets: Optional[int] = None
    reps: Optional[str] = None
    rest: Optional[str] = None
    method_name: Optional[str] = None
    exercises: Optional[List[Dict[str, Any]]] = None

@final
class UserRoutineResponseSchema(BaseModel):
    id: int
    user_id: int
    week: int
    day: int
    goal: str
    level: str
    volume: str
    sets: int
    reps: str
    rest: str
    method_name: str
    exercises: List[Dict[str, Any]]

    model_config = {"from_attributes": True}
