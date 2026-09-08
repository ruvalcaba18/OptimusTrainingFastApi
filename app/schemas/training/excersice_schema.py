from pydantic import BaseModel, Field

from app.models.Enums.ExcersicePattern import ExcersicePattern
from app.schemas.training.condition_schema import ConditionSchema
from app.schemas.training.goal_schema import GoalSchema


class ExcersiceConditionResponse(BaseModel):
    condition: ConditionSchema
    relationship: str

    model_config = {"from_attributes": True}


class ExcersiceResponse(BaseModel):
    id: int
    code: str
    exercise_id: str | None = None
    name: str
    image_url: str | None = None
    muscle_group: str
    pattern: ExcersicePattern
    primary_tool: str
    secondary_tool: str | None = None
    location: str
    complexity: str
    level: str
    fatigue: str
    category: str
    goals: list[GoalSchema] = []
    conditions_association: list[ExcersiceConditionResponse] = Field(
        default=[], alias="conditions_association"
    )

    model_config = {"from_attributes": True, "populate_by_name": True}
