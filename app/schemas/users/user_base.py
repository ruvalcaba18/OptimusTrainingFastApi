from typing import Any, final

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.Enums.UserTier import UserTier
from app.schemas.training.leisure_activity_schema import LeisureActivitySchema

from .gender import UserGender
from .phone_validator import PhoneValidator
from .training_type import TrainingType


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
    gender: UserGender | None = None
    goal_code: str | None = None
    level_code: str | None = None
    custom_equipment: str | None = None
    session_duration_code: str | None = None
    specific_days: list[int] | None = None
    leisure_activities: list[LeisureActivitySchema] | None = None
    tier: UserTier | None = UserTier.BASIC

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

    @field_validator("specific_days", mode="before")
    @classmethod
    def parse_specific_days(cls, v: Any) -> list[int] | None:
        if isinstance(v, str):
            if not v.strip():
                return []
            return [int(x.strip()) for x in v.split(",") if x.strip().isdigit()]
        return v
