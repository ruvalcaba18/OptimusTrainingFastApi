from typing import final

from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


@final
class UserEquipment(Base):
    __tablename__ = "user_equipment"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id", ondelete="CASCADE"), primary_key=True)
