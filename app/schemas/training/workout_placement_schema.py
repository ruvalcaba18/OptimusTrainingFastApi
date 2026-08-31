from typing import Optional, final

from pydantic import BaseModel, ConfigDict


@final 
class WorkoutPlacementSchema(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True,extra='forbid', str_strip_whitespace=True)