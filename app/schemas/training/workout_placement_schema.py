from typing import final

from pydantic import BaseModel, ConfigDict


@final
class WorkoutPlacementSchema(BaseModel):
    code: str
    name: str
    description: str | None = None

    model_config = ConfigDict(
        from_attributes=True, extra="forbid", str_strip_whitespace=True
    )
