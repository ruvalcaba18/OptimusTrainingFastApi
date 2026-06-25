from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from typing import final
from app.database import Base

@final
class Method(Base):
    __tablename__ = "methods"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)  
    type = Column(String(100), nullable=False)    
    level = Column(String(100), nullable=False)     
    complexity = Column(String(50), nullable=False) 
    intensity = Column(String(50), nullable=True)   
    tempo = Column(String(100), nullable=True)    
    
    goals = relationship("Goal", secondary="method_goal", backref="methods")
