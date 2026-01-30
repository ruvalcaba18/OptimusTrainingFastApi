from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from enum import Enum
import re

class TrainingType(str, Enum):
    CASA = "casa"
    AFUERA = "afuera"
    GIMNASIO = "gimnasio"
    MIXTO = "mixto"

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

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r"^\+?[\d\s-]{7,15}$", v):
            raise ValueError("Número de teléfono inválido")
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

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

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
