from pydantic import BaseModel
from typing import Optional

class ConditionSchema(BaseModel):
    id: int
    code: str
    name: str
    type: str  
    category: Optional[str] = None

    model_config = {"from_attributes": True}
