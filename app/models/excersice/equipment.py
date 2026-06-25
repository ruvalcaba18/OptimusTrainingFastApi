from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import final
from app.database import Base

@final
class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    excersices_association = relationship("ExcersiceEquipment", back_populates="equipment", cascade="all, delete-orphan")
