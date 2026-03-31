from typing import Optional
from pydantic import BaseModel


class SocialAuthRequest(BaseModel):
    token: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
