"""
Auth routes for API v1.
"""
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.auth.auth_controller import auth_controller
from app.schemas.users import Token, UserLogin

router = APIRouter()


@router.post("/login", response_model=Token, summary="Iniciar sesión")
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db),
) -> Any:
    """
    Autentica al usuario con email y contraseña.
    Devuelve un JWT Bearer token.
    """
    return auth_controller.login(db, user_in=user_in)
