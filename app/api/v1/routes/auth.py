from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.auth.auth_controller import auth_controller
from app.schemas.users import Token, UserLogin, PasswordRecoveryRequest, PasswordReset

router = APIRouter()


@router.post("/login", response_model=Token, summary="Iniciar sesión (JSON)")
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db),
) -> Any:
    """
    Autentica al usuario con email y contraseña via JSON body.
    Devuelve un JWT Bearer token (access + refresh).
    """
    return auth_controller.login(db, user_in=user_in)


@router.post("/login/access-token", response_model=Token, summary="Iniciar sesión (Form/Swagger)")
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    Autentica al usuario con username (email) y contraseña via Form data.
    Especialmente útil para la documentación Swagger (botón Authorize).
    """
    user_in = UserLogin(email=form_data.username, password=form_data.password)
    return auth_controller.login(db, user_in=user_in)


@router.post("/refresh-token", response_model=Token, summary="Refrescar Access Token")
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Genera un nuevo access_token usando un refresh_token válido.
    """
    return auth_controller.refresh_token(db, refresh_token=refresh_token)


@router.post("/password-recovery/{email}", summary="Recuperar contraseña")
def recover_password(
    email: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Envía un correo electrónico de recuperación de contraseña.
    """
    return auth_controller.recover_password(db, email=email)


@router.post("/reset-password", summary="Restablecer contraseña")
def reset_password(
    data: PasswordReset,
    db: Session = Depends(get_db),
) -> Any:
    """
    Restablece la contraseña usando un token de recuperación válido.
    """
    return auth_controller.reset_password(
        db, token=data.token, new_password=data.new_password
    )
