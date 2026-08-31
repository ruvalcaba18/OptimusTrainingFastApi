from typing import final

from sqlalchemy import Column, Integer, String, Text

from app.database import Base


@final
class EverydayItem(Base):
    __tablename__ = "everyday_item"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    mapping = Column(String(200), nullable=True)