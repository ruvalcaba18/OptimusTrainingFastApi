from typing import final

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


@final
class ProgrammingMatrix(Base):
    __tablename__ = "programming_matrix"

    id = Column(Integer, primary_key=True, index=True)
    goal_code = Column(String(50), nullable=False)
    level_code = Column(String(50), nullable=False)
    volume = Column(String(50), nullable=False)   
    sets = Column(Integer, nullable=False)
    reps = Column(String(50), nullable=False)   
    rest = Column(String(50), nullable=False)  
    method_id = Column(Integer, ForeignKey("methods.id", ondelete="SET NULL"), nullable=True)

    method = relationship("Method")
