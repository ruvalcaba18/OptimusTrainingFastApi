from pydantic import BaseModel


class EquipmentSchema(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
