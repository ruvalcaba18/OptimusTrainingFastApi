from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func 
from app.database import Base

class PromptLog(Base):
    __tablename__ = "prompt_logs"
    
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False, index = True)
    system_prompt = Column(Text, nullable = False)
    user_prompt = Column(Text, nullable = False)
    ai_response = Column(Text, nullable = False)
    created_at = Column(DateTime(timezone = True), server_default = func.now(), nullable = False)