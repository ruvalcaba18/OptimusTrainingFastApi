from .user_base import UserBase

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
