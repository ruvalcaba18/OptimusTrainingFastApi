from pydantic import BaseModel
from datetime import datetime
from typing import final

@final
class PromptLogResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}