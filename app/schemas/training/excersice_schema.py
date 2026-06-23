from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.Enums.ExcersicePattern import ExcersicePattern
from app.schemas.training.goal_schema import GoalSchema
from app.schemas.training.condition_schema import ConditionSchema

class ExcersiceConditionResponse(BaseModel):
    condition: ConditionSchema
    relationship: str

    model_config = {"from_attributes": True}

class ExcersiceResponse(BaseModel):
    id: int
    code: str
    name: str
    muscle_group: str
    pattern: ExcersicePattern
    primary_tool: str
    secondary_tool: Optional[str] = None
    location: str
    complexity: str
    level: str
    fatigue: str
    category: str
    goals: List[GoalSchema] = []
    conditions_association: List[ExcersiceConditionResponse] = Field(default=[], alias="conditions_association")

    model_config = {"from_attributes": True, "populate_by_name": True}
