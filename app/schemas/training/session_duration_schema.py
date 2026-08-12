from pydantic import BaseModel, ConfigDict
from typing import final

@final
class SessionDurationSchema(BaseModel):
    code: str
    name: str
    description: str
    
    model_config = ConfigDict(from_attributes=True,extra='forbid', str_strip_whitespace=True)