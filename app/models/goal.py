from sqlalchemy import Table, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from typing import final
from app.database import Base

excersice_goal = Table(
    "excersice_goal",
    Base.metadata,
    Column("excersice_id", Integer, ForeignKey("excersices.id", ondelete="CASCADE"), primary_key=True),
    Column("goal_id", Integer, ForeignKey("goals.id", ondelete="CASCADE"), primary_key=True),
)

@final
class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationship to excersices
    excersices = relationship("Excersice", secondary=excersice_goal, back_populates="goals")
