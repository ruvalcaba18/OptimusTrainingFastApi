from pydantic import BaseModel, EmailStr, Field, field_validator
from .training_type import TrainingType
from .gender import UserGender
from .phone_validator import PhoneValidator
from typing import Optional, final


@final
class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=8)
    age: int = Field(..., gt=0)
    weight: float = Field(default=None, gt=0)
    height: float = Field(default=None, gt=0)
    exercise_frequency: str
    training_type: TrainingType = Field(default=TrainingType.CASA)
    gender: Optional[UserGender] = None
    goal_code: Optional[str] = None
    level_code: Optional[str] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        return PhoneValidator.validate(v)

    @field_validator("gender", mode="before")
    @classmethod
    def validate_gender(cls, value: str) -> str:
        if value is not None and isinstance(value, str):
            return value.lower()
        return value
