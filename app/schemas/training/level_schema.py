
from pydantic import BaseModel


class LevelSchema(BaseModel):
    id: int
    code: str
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}
