
from pydantic import BaseModel


class UserTrainingProfileUpdate(BaseModel):
    goal_code: str
    level_code: str
    equipment_ids: list[int] | None = None
    pathology_ids: list[int] | None = None
    disease_ids: list[int] | None = None
    custom_equipment: str | None = None
    session_duration_code: str | None = None
    specific_days: list[int] | None = None
    leisure_activity_ids: list[int] | None = None
