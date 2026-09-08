from typing import Any, final

from pydantic import BaseModel


@final
class UserRoutineUpdateSchema(BaseModel):
    goal: str | None = None
    level: str | None = None
    volume: str | None = None
    sets: int | None = None
    reps: str | None = None
    rest: str | None = None
    method_name: str | None = None
    exercises: list[dict[str, Any]] | None = None

@final
class UserRoutineResponseSchema(BaseModel):
    id: int
    week: int
    day: int
    goal: str
    level: str
    volume: str
    sets: int
    reps: str
    rest: str
    method_name: str
    exercises: list[dict[str, Any]]

    model_config = {"from_attributes": True}
