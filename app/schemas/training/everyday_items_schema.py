from typing import final

from pydantic import BaseModel, ConfigDict, field_validator


@final 
class EveryDayItemSchema(BaseModel):
    id: int
    code: str | None = None
    name: str
    description: str | None = None
    mapping: list[str] | None = None

    @field_validator('mapping', mode='before')
    @classmethod
    def split_mapping(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        if v is None:
            return []
        return v
    
    model_config = ConfigDict(from_attributes=True, extra="ignore", str_strip_whitespace=True)
    