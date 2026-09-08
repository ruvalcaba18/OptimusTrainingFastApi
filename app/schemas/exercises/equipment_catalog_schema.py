
from pydantic import BaseModel, ConfigDict


class EquipmentCatalogResponse(BaseModel):
    id: int
    name: str
    name_es: str | None = None
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
