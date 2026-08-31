from typing import final

from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


@final
class UserDisease(Base):
    __tablename__ = "user_disease"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    disease_id = Column(Integer, ForeignKey("conditions.id", ondelete="CASCADE"), primary_key=True)
