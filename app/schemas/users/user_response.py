from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from .user_base import UserBase
from .token import Token


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

