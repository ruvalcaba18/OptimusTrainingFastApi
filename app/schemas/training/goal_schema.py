from pydantic import BaseModel
from typing import Optional

class GoalSchema(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}
