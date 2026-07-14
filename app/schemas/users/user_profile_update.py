from pydantic import BaseModel
from typing import List, Optional

class UserProfileUpdate(BaseModel):
    goal_code: str
    level_code: str
    equipment_ids: List[int] = []
    pathology_ids: List[int] = []
    disease_ids: List[int] = []
