from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from typing import final
from app.database import Base

@final
class Level(Base):
    __tablename__ = "levels"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
