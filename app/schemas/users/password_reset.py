from pydantic import BaseModel, EmailStr, Field

class PasswordRecoveryRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
