from pydantic import BaseModel
from typing import Optional, final

@final
class LeisureActivitySchema(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}
