from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


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
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="SET NULL"), nullable=True)
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="SET NULL"), nullable=True)

    goal = relationship("Goal")
    level = relationship("Level")
    pathologies = relationship("Condition", secondary="user_pathology", backref="users_with_pathology")
    diseases = relationship("Condition", secondary="user_disease", backref="users_with_disease")
    equipments = relationship("Equipment", secondary="user_equipment", backref="users")

