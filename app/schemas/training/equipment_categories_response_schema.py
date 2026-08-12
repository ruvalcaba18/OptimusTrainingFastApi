from pydantic import BaseModel
from typing import List, final
from .equipment_category_item_schema import EquipmentCategoryItem

@final
class EquipmentCategoriesResponse(BaseModel):
    gym: List[EquipmentCategoryItem]
    home: List[EquipmentCategoryItem]
    outdoor: List[EquipmentCategoryItem]
    everyday: List[EquipmentCategoryItem]

    model_config = {"from_attributes": True}
