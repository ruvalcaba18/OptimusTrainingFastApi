from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from .training_type import TrainingType

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    exercise_frequency: Optional[str] = None
    training_type: Optional[TrainingType] = None
    password: Optional[str] = Field(None, min_length=8)
