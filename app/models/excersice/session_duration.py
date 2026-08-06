from sqlalchemy import Column, Integer, String, Text
from typing import final
from app.database import Base

@final 
class SessionDuration(Base):
    __tablename__ = "session_durations"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False,index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text,nullable=True)