from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    ForeignKey, Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Enterprise(Base):
    __tablename__ = "enterprises"

                                                                            
    id = Column(Integer, primary_key=True, index=True)

                                                                            
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    logo_url = Column(String, nullable=True)
    contact_email = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

                                                                            
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

                                                                            
    codes = relationship(
        "EnterpriseCode", back_populates="enterprise", cascade="all, delete-orphan"
    )
    members = relationship(
        "EnterpriseMember", back_populates="enterprise", cascade="all, delete-orphan"
    )


class EnterpriseCode(Base):
    __tablename__ = "enterprise_codes"

    id = Column(Integer, primary_key=True, index=True)
    enterprise_id = Column(
        Integer, ForeignKey("enterprises.id", ondelete="CASCADE"), nullable=False
    )

                                                                            
    code = Column(String(20), unique=True, index=True, nullable=False)

                                                                            
    is_used = Column(Boolean, default=False, nullable=False)
    used_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    used_at = Column(DateTime(timezone=True), nullable=True)

                                                                            
    expires_at = Column(DateTime(timezone=True), nullable=False)

                                                                            
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

                                                                            
    enterprise = relationship("Enterprise", back_populates="codes")
    used_by = relationship("User", backref="used_enterprise_codes")


class EnterpriseMember(Base):
    __tablename__ = "enterprise_members"

    id = Column(Integer, primary_key=True, index=True)
    enterprise_id = Column(
        Integer, ForeignKey("enterprises.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

                                                                            
    enterprise = relationship("Enterprise", back_populates="members")
    user = relationship("User", backref="enterprise_memberships")
