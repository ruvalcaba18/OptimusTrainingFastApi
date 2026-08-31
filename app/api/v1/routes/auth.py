import logging
from typing import Dict

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.controllers.auth.auth_controller import auth_controller
from app.database import get_db
from app.models import User
from app.schemas.users import PasswordReset, Token, TokenRefreshRequest, UserLogin

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/login", 
    response_model=Token, 
    summary="Iniciar sesión (JSON)"
             )
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db),
) -> Token:
    logger.info(f"Login attempt for user: {user_in.email}")
    
    return auth_controller.login(db, user_in=user_in)


@router.post("/login/access-token", 
             response_model=Token, 
             summary="Iniciar sesión (Form/Swagger)")
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user_in = UserLogin(email=form_data.username, password=form_data.password)
    return auth_controller.login(db, user_in=user_in)


@router.post("/refresh-token", 
             response_model=Token, 
             summary="Renovar Access Token"
)
def refresh_token(
    body: TokenRefreshRequest,
    db: Session = Depends(get_db)
) -> Token:
    logger.info("Refreshing access token using refresh token")
    
    return auth_controller.refresh_access_token(db, refresh_token=body.refresh_token)


@router.post("/password-recovery/{email}", 
             summary="Recuperar contraseña")
def recover_password(
    email: str,
    db: Session = Depends(get_db),
) -> dict:
    return auth_controller.recover_password(db, email=email)


@router.post("/reset-password", 
             summary="Restablecer contraseña")
def reset_password(
    data: PasswordReset,
    db: Session = Depends(get_db),
) -> dict:
    return auth_controller.reset_password(
        db, token=data.token, new_password=data.new_password
    )
