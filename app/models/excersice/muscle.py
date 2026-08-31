from typing import final

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


@final
class Muscle(Base):
    __tablename__ = "muscles"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    common_name = Column(String(100), nullable=True)
    body_part = Column(String(50), nullable=False)  # Upper Body, Lower Body, Core

    excersice_associations = relationship("ExcersiceMuscle", back_populates="muscle", cascade="all, delete-orphan")
