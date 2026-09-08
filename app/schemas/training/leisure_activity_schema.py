from typing import final

from pydantic import BaseModel


@final
class LeisureActivitySchema(BaseModel):
    id: int
    code: str
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}
