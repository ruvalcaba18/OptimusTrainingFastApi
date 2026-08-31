from typing import Optional, final

from pydantic import BaseModel


@final
class HealthQuestionSchema(BaseModel):
    id: int
    code: str
    title: str
    subtitle: Optional[str] = None
    type: str
    category: str

    model_config = {"from_attributes": True}
