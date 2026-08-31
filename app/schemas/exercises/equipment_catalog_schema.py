from typing import Optional

from pydantic import BaseModel, ConfigDict


class EquipmentCatalogResponse(BaseModel):
    id: int
    name: str
    name_es: Optional[str] = None
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
