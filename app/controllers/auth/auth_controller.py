from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.services.user_service import user_service
from app.core import security
from app.core.config import settings
from app.schemas.users import Token, UserLogin
from app.models.user import User


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

    @staticmethod
    def refresh_access_token(db: Session, user: User) -> Token:
        """
        Genera un nuevo access token para un usuario que ya tiene un token válido.
        Esto permite la rotación de tokens sin un refresh_token por separado.
        """
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=security.create_access_token(
                user.email, expires_delta=access_token_expires
            ),
            token_type="bearer",
        )

    @staticmethod
    def recover_password(db: Session, email: str) -> dict:
        from app.services.email_service import email_service
        user = user_service.get_by_email(db, email=email)
        if user:
            token = security.create_password_reset_token(email)
            email_service.send_password_reset_email(email, token)
        
        return {"message": "Si el correo está registrado, se ha enviado un enlace de recuperación."}

    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> dict:
        from jose import jwt, JWTError
        from app.schemas.users import UserUpdate
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            if payload.get("type") != "reset_password":
                raise JWTError("Invalid token type")
            email = payload.get("sub")
            if not email:
                raise JWTError("Missing subject")
        except (JWTError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token de recuperación inválido o expirado",
            )
        
        user = user_service.get_by_email(db, email=email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        try:
            user_service.update(db, db_obj=user, user_in=UserUpdate(password=new_password))
            db.commit()
            return {"message": "Contraseña actualizada correctamente."}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


auth_controller = AuthController()
