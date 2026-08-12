from pydantic import BaseModel, field_validator
from typing import List, final

@final
class HomeEquipmentSchema(BaseModel):
    id: int
    code: str
    name: str
    mapping: List[str]

    @field_validator('mapping', mode='before')
    @classmethod
    def split_mapping(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        if v is None:
            return []
        return v

    model_config = {"from_attributes": True}
