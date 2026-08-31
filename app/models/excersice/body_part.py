from typing import final

from sqlalchemy import Column, Integer, String

from app.database import Base


@final
class BodyPart(Base):
    __tablename__ = "body_parts"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_en = Column(String(100), unique=True, nullable=False, index=True)
    name_es = Column(String(100), nullable=False)
    image_url = Column(String(500), nullable=True)
