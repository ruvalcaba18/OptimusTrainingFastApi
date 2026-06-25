from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship as sqla_relationship
from typing import final
from app.database import Base

@final
class ExcersiceCondition(Base):
    __tablename__ = "excersice_condition"
    
    excersice_id = Column(Integer, ForeignKey("excersices.id", ondelete="CASCADE"), primary_key=True)
    condition_id = Column(Integer, ForeignKey("conditions.id", ondelete="CASCADE"), primary_key=True)
    relationship = Column(String(50), nullable=False)  # 'COMPATIBLE', 'CAUTION', 'FORBIDDEN'
    
    excersice = sqla_relationship("Excersice", back_populates="conditions_association")
    condition = sqla_relationship("Condition", back_populates="excersices_association")

@final
class Condition(Base):
    __tablename__ = "conditions"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)  
    category = Column(String(100), nullable=True) 
    
    excersices_association = sqla_relationship("ExcersiceCondition", back_populates="condition", cascade="all, delete-orphan")
