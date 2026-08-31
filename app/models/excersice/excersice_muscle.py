from typing import final

from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


@final
class ExcersiceMuscle(Base):
    __tablename__ = "excersice_muscles"

    id = Column(Integer, primary_key=True, index=True)
    excersice_id = Column(Integer, ForeignKey("excersices.id", ondelete="CASCADE"), nullable=False)
    muscle_id = Column(Integer, ForeignKey("muscles.id", ondelete="CASCADE"), nullable=False)
    is_primary = Column(Boolean, default=True, nullable=False)

    excersice = relationship("Excersice", back_populates="muscle_associations")
    muscle = relationship("Muscle", back_populates="excersice_associations")
