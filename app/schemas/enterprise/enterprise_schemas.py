from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


class EnterpriseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    contact_email: EmailStr


class EnterpriseCreate(EnterpriseBase):
    pass


class EnterpriseResponse(EnterpriseBase):
    id: int
    logo_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ValidateCodeRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=20)


class CodeGenerateRequest(BaseModel):
    enterprise_id: int = Field(..., description="ID de la empresa")
    quantity: int = Field(..., ge=1, le=500, description="Cantidad de códigos a generar")
    expire_in_days: int = Field(
        default=7, ge=1, le=365,
        description="Días hasta que los códigos expiren"
    )


class EnterpriseCodeResponse(BaseModel):
    id: int
    code: str
    is_used: bool
    used_by_user_id: Optional[int] = None
    used_at: Optional[datetime] = None
    expires_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class ValidateCodeResponse(BaseModel):
    message: str
    enterprise: EnterpriseResponse


class EnterpriseMemberResponse(BaseModel):
    id: int
    enterprise_id: int
    user_id: int
    joined_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}
