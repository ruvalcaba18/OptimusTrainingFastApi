from datetime import timedelta
from typing import final

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.controllers.auth.exceptions import (
    InactiveAccountError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    InvalidResetTokenError,
)
from app.controllers.users.exceptions import UserNotFoundError
from app.core import security
from app.core.config import settings
from app.core.error_handlers import handle_controller_errors
from app.schemas.users import Token, UserLogin, UserUpdate
from app.services import user_service


@final
class AuthController:

    @staticmethod
    @handle_controller_errors
    def login(db: Session, user_in: UserLogin) -> Token:
        user = user_service.get_by_email(db, email=user_in.email)

        if not user or not security.verify_password(user_in.password, user.hashed_password):
            raise InvalidCredentialsError()
        if not user.is_active:
            raise InactiveAccountError()

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        return Token(
            access_token=security.create_access_token(
                user.email, expires_delta=access_token_expires
            ),
            refresh_token=security.create_refresh_token(
                user.email, expires_delta=refresh_token_expires
            ),
            token_type="bearer",
        )

    @staticmethod
    @handle_controller_errors
    def refresh_access_token(db: Session, refresh_token: str) -> Token:
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") != "refresh":
                raise JWTError("Invalid token type")

            email = payload.get("sub")
            if not email:
                raise JWTError("Missing subject")
        except JWTError:
            raise InvalidRefreshTokenError()

        user = user_service.get_by_email(db, email=email)
        if not user:
            raise UserNotFoundError()

        if not user.is_active:
            raise InactiveAccountError()

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        return Token(
            access_token=security.create_access_token(user.email, access_token_expires),
            refresh_token=security.create_refresh_token(user.email, refresh_token_expires),
            token_type="bearer",
        )

    @staticmethod
    @handle_controller_errors
    def recover_password(db: Session, email: str) -> dict:
        from app.services import email_service
        user = user_service.get_by_email(db, email=email)
        if user:
            token = security.create_password_reset_token(email)
            email_service.send_password_reset_email(email, token)

        return {"message": "Si el correo está registrado, se ha enviado un enlace de recuperación."}

    @staticmethod
    @handle_controller_errors
    def reset_password(db: Session, token: str, new_password: str) -> dict:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            if payload.get("type") != "reset_password":
                raise JWTError("Invalid token type")
            email = payload.get("sub")
            if not email:
                raise JWTError("Missing subject")
        except JWTError:
            raise InvalidResetTokenError()

        user = user_service.get_by_email(db, email=email)
        if not user:
            raise UserNotFoundError()

        user_service.update(db, db_obj=user, user_in=UserUpdate(password=new_password))
        db.commit()
        return {"message": "Contraseña actualizada correctamente."}


auth_controller = AuthController()
