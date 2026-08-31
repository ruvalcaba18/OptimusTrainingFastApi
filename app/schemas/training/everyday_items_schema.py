from typing import List, Optional, final

from pydantic import BaseModel, ConfigDict, field_validator


@final 
class EveryDayItemSchema(BaseModel):
    id: int
    code: Optional[str] = None
    name: str
    description: Optional[str] = None
    mapping: Optional[List[str]] = None

    @field_validator('mapping', mode='before')
    @classmethod
    def split_mapping(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        if v is None:
            return []
        return v
    
    model_config = ConfigDict(from_attributes=True, extra="ignore", str_strip_whitespace=True)
    