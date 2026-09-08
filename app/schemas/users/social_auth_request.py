
from pydantic import BaseModel


class SocialAuthRequest(BaseModel):
    token: str
    first_name: str | None = None
    last_name: str | None = None
