from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from typing import final
from app.database import Base

@final
class ExcersiceEquipment(Base):
    __tablename__ = "excersice_equipment"

    excersice_id = Column(Integer, ForeignKey("excersices.id", ondelete="CASCADE"), primary_key=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id", ondelete="CASCADE"), primary_key=True)
    is_primary = Column(Boolean, default=True, nullable=False)

    excersice = relationship("Excersice", back_populates="equipment_association")
    equipment = relationship("Equipment", back_populates="excersices_association")
