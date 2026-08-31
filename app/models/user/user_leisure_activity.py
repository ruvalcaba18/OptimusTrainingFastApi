from typing import final

from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


@final
class UserLeisureActivity(Base):
    __tablename__ = "user_leisure_activity"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    leisure_activity_id = Column(Integer, ForeignKey("leisure_activities.id", ondelete="CASCADE"), primary_key=True)
