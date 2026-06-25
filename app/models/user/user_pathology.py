from sqlalchemy import Column, Integer, ForeignKey
from typing import final
from app.database import Base

@final
class UserPathology(Base):
    __tablename__ = "user_pathology"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    pathology_id = Column(Integer, ForeignKey("conditions.id", ondelete="CASCADE"), primary_key=True)
