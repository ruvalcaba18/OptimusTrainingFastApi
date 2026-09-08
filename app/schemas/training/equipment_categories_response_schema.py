from typing import final

from pydantic import BaseModel

from .equipment_category_item_schema import EquipmentCategoryItem


@final
class EquipmentCategoriesResponse(BaseModel):
    gym: list[EquipmentCategoryItem]
    home: list[EquipmentCategoryItem]
    outdoor: list[EquipmentCategoryItem]
    everyday: list[EquipmentCategoryItem]

    model_config = {"from_attributes": True}
