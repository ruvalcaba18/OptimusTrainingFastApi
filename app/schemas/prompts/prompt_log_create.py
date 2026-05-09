from pydantic import BaseModel
from typing import final

@final
class PromptLogCreate(BaseModel):
    system_prompt: str
    user_prompt: str
    ai_response: str
