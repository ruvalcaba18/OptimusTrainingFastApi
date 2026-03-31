from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    Text, ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ActiveBreakSession(Base):
    __tablename__ = "active_break_sessions"

                                                                            
    id = Column(Integer, primary_key=True, index=True)

                                                                            
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)                                   
    duration_minutes = Column(Integer, nullable=False)                   
    instructions = Column(Text, nullable=True)                             
    video_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

                                                                            
    is_active = Column(Boolean, default=True, nullable=False)

                                                                            
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

                                                                            
    logs = relationship(
        "ActiveBreakLog", back_populates="session", cascade="all, delete-orphan"
    )


class ActiveBreakLog(Base):
    __tablename__ = "active_break_logs"

                                                                            
    id = Column(Integer, primary_key=True, index=True)

                                                                            
    session_id = Column(
        Integer, ForeignKey("active_break_sessions.id"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    enterprise_id = Column(
        Integer, ForeignKey("enterprises.id"), nullable=True
    )

                                                                            
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

                                                                            
    session = relationship("ActiveBreakSession", back_populates="logs")
    user = relationship("User", backref="active_break_logs")
