from typing import final

from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


@final
class MethodGoal(Base):
    __tablename__ = "method_goal"

    method_id = Column(Integer, ForeignKey("methods.id", ondelete="CASCADE"), primary_key=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), primary_key=True)
