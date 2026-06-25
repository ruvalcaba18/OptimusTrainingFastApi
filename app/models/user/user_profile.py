from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from typing import final
from app.database import Base

@final
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="SET NULL"), nullable=True)
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="SET NULL"), nullable=True)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)

    # Relaciones
    user = relationship("User", back_populates="profile")
    goal = relationship("Goal")
    level = relationship("Level")
