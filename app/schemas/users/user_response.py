from datetime import datetime

from pydantic import BaseModel

from .token import Token
from .user_base import UserBase


class UserResponse(UserBase):
    id: int
    is_active: bool
    profile_picture_url: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class UserRegistrationResponse(BaseModel):
    user: UserResponse
    token: Token
