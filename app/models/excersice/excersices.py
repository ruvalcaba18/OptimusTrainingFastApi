from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from typing import final, Optional
from app.models.Enums.ExcersicePattern import ExcersicePattern
from app.database import Base

@final
class Excersice(Base):
    __tablename__ = "excersices"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    muscle_group = Column(String(100), nullable=False)
    pattern = Column(Enum(ExcersicePattern, name="excersice_pattern"), nullable=False)
    location = Column(String(100), nullable=False)
    complexity = Column(String(50), nullable=False)
    level = Column(String(100), nullable=False)
    fatigue = Column(String(50), nullable=False)
    category = Column(String(100), nullable=False)
    
    conditions_association = relationship("ExcersiceCondition", back_populates="excersice", cascade="all, delete-orphan")
    equipment_association = relationship("ExcersiceEquipment", back_populates="excersice", cascade="all, delete-orphan")
    
    goals = relationship("Goal", secondary="excersice_goal", back_populates="excersices")

    @property
    def primary_tool(self) -> str:
        for assoc in self.equipment_association:
            if assoc.is_primary:
                return assoc.equipment.name
        return "Propio Peso"

    @property
    def secondary_tool(self) -> Optional[str]:
        for assoc in self.equipment_association:
            if not assoc.is_primary:
                return assoc.equipment.name
        return None