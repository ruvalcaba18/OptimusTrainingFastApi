from pydantic import BaseModel
from typing import List, Optional

class UserTrainingProfileUpdate(BaseModel):
    goal_code: str
    level_code: str
    equipment_ids: Optional[List[int]] = None
    pathology_ids: Optional[List[int]] = None
    disease_ids: Optional[List[int]] = None
    custom_equipment: Optional[str] = None
    session_duration_code: Optional[str] = None
    specific_days: Optional[List[int]] = None
    leisure_activity_ids: Optional[List[int]] = None
