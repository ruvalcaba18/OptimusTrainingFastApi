"""
Auth controller — handles login HTTP logic.
"""
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.services.user_service import user_service
from app.core import security
from app.core.config import settings
from app.schemas.users import Token, UserLogin


class AuthController:

    @staticmethod
    def login(db: Session, user_in: UserLogin) -> Token:
        user = user_service.get_by_email(db, email=user_in.email)
        if not user or not security.verify_password(user_in.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cuenta inactiva",
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=security.create_access_token(
                user.email, expires_delta=access_token_expires
            ),
            token_type="bearer",
        )


auth_controller = AuthController()
