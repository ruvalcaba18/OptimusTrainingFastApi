from pydantic import BaseModel
from typing import Optional

class ConditionSchema(BaseModel):
    id: int
    code: str
    name: str
    type: str  # 'PATHOLOGY' or 'DISEASE'
    category: Optional[str] = None

    model_config = {"from_attributes": True}
