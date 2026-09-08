from typing import final

from pydantic import BaseModel


@final
class HealthQuestionSchema(BaseModel):
    id: int
    code: str
    title: str
    subtitle: str | None = None
    type: str
    category: str

    model_config = {"from_attributes": True}
