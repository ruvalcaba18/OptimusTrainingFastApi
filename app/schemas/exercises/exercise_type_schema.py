
from pydantic import BaseModel, ConfigDict


class ExerciseTypeResponse(BaseModel):
    id: int
    code: str
    name_en: str
    name_es: str
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
