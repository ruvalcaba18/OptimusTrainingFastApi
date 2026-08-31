from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .token import Token
from .user_base import UserBase


class UserResponse(UserBase):
    id: int
    is_active: bool
    profile_picture_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserRegistrationResponse(BaseModel):
    user: UserResponse
    token: Token
