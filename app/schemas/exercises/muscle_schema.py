from typing import Optional

from pydantic import BaseModel, ConfigDict


class MuscleResponse(BaseModel):
    id: int
    code: str
    name: str
    common_name: Optional[str] = None
    body_part: str

    model_config = ConfigDict(from_attributes=True)
