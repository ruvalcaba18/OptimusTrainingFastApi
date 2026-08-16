from sqlalchemy import Column, Integer, String, Text
from typing import final
from app.database import Base

@final
class HealthQuestionModel(Base):
    __tablename__ = "health_questions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(250), nullable=False)
    subtitle = Column(String(250), nullable=True)
    type = Column(String(50), nullable=False) # e.g., multiple, single
    category = Column(String(50), nullable=False) # e.g., PATHOLOGY, DISEASE
