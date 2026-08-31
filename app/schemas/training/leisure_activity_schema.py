from typing import Optional, final

from pydantic import BaseModel


@final
class LeisureActivitySchema(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}
