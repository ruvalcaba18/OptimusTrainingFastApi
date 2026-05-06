from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from .training_type import TrainingType
from .gender import UserGender
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    phone: str
    age: int = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    exercise_frequency: str
    training_type: TrainingType
    gender: Optional[UserGender] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r"^\+?[\d\s-]{7,15}$", v):
            raise ValueError("Número de teléfono inválido")
        return v
