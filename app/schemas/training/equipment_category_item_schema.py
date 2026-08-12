from pydantic import BaseModel
from typing import List, final

@final
class EquipmentCategoryItem(BaseModel):
    code: str
    name: str
    mapping: List[str]
