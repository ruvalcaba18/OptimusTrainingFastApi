from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.Enums.UserTier import UserTier


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    auth_provider = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    exercise_frequency = Column(String, nullable=False)
    training_type = Column(String, nullable=False)
    gender = Column(String, nullable=True) 
    profile_picture_url = Column(String, nullable=True)
    custom_equipment = Column(String, nullable=True)
    session_duration_code = Column(String, nullable=True)
    specific_days = Column(String, nullable=True)
    tier = Column(Enum(UserTier), default=UserTier.BASIC, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="SET NULL"), nullable=True)
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="SET NULL"), nullable=True)

    goal = relationship("Goal")
    level = relationship("Level")
    pathologies = relationship("Condition", secondary="user_pathology", backref="users_with_pathology")
    diseases = relationship("Condition", secondary="user_disease", backref="users_with_disease")
    equipments = relationship("Equipment", secondary="user_equipment", backref="users")
    leisure_activities = relationship("LeisureActivityModel", secondary="user_leisure_activity", backref="users")
    user_routines = relationship("UserRoutine", back_populates="user", cascade="all, delete-orphan")

