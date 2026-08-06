from sqlalchemy import Column, Integer, String, Text
from typing import final
from app.database import Base

@final
class WorkoutPlace(Base):
    __tablename__ = "workout_places"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)