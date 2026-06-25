from sqlalchemy import Column, Integer, ForeignKey
from typing import final
from app.database import Base

@final
class ExcersiceGoal(Base):
    __tablename__ = "excersice_goal"

    excersice_id = Column(Integer, ForeignKey("excersices.id", ondelete="CASCADE"), primary_key=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), primary_key=True)
