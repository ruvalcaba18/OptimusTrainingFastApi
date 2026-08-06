from pydantic import BaseModel, ConfigDict
from typing import final, Optional
    
@final 
class WorkoutPlacementSchema(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)