from typing import final

from sqlalchemy import Column, Integer, String, Text

from app.database import Base


@final
class HomeEquipmentModel(Base):
    __tablename__ = "home_equipment"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    mapping = Column(String(200), nullable=False)
