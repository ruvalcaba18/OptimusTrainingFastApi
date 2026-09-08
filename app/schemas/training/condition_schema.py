
from pydantic import BaseModel


class ConditionSchema(BaseModel):
    id: int
    code: str
    name: str
    type: str  
    category: str | None = None
    warning_message: str | None = None

    model_config = {"from_attributes": True}
