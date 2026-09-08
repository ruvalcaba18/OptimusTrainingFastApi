from typing import final

from pydantic import BaseModel, EmailStr, Field

from .gender import UserGender
from .training_type import TrainingType


@final
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    age: int | None = None
    weight: float | None = None
    height: float | None = None
    exercise_frequency: str | None = None
    training_type: TrainingType | None = None
    gender: UserGender | None = None
    password: str | None = Field(None, min_length=8)

