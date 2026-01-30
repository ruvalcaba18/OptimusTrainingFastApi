from pydantic import Field
from .user_base import UserBase

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
