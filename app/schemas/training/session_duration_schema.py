from pydantic import BaseModel, ConfigDict
from typing import final

@final
class SessionDurationSchema(BaseModel):
    code: str
    name: str
    description: str
    
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)