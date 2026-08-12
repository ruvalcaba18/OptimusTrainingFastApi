from pydantic import BaseModel, ConfigDict
from typing import final, Optional
    
@final 
class WorkoutPlacementSchema(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True,extra='forbid', str_strip_whitespace=True)