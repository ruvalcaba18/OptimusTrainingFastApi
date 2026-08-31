from typing import List, Optional

from pydantic import BaseModel

from app.schemas.training.goal_schema import GoalSchema


class MethodSchema(BaseModel):
    id: int
    code: str
    name: str
    category: str  # 'FORCE' or 'RESISTANCE'
    type: str
    level: str
    complexity: str
    intensity: Optional[str] = None
    tempo: Optional[str] = None
    goals: List[GoalSchema] = []

    model_config = {"from_attributes": True}
