from typing import final

from sqlalchemy import Column, Integer, String, Text

from app.database import Base


@final
class LeisureActivityModel(Base):
    __tablename__ = "leisure_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
