from typing import final

from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


@final
class ExcersiceGoal(Base):
    __tablename__ = "excersice_goal"

    excersice_id = Column(Integer, ForeignKey("excersices.id", ondelete="CASCADE"), primary_key=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), primary_key=True)
