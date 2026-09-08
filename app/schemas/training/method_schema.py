
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
    intensity: str | None = None
    tempo: str | None = None
    goals: list[GoalSchema] = []

    model_config = {"from_attributes": True}
