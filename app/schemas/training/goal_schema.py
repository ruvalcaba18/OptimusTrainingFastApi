from typing import Optional

from pydantic import BaseModel


class GoalSchema(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}
