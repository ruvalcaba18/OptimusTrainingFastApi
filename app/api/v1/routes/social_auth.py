from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.users import Token
from app.schemas.users.social_auth_request import SocialAuthRequest
from app.controllers.auth.social_auth_controller import social_auth_controller

router = APIRouter()


@router.post("/apple", response_model=Token, summary="Sign In with Apple")
async def login_with_apple(
    body: SocialAuthRequest,
    db: Session = Depends(get_db),
) -> Any:
    return await social_auth_controller.login_with_apple(db=db, body=body)


@router.post("/google", response_model=Token, summary="Sign In with Google")
async def login_with_google(
    body: SocialAuthRequest,
    db: Session = Depends(get_db),
) -> Any:
    return await social_auth_controller.login_with_google(db=db, body=body)


@router.post("/facebook", response_model=Token, summary="Login with Facebook")
async def login_with_facebook(
    body: SocialAuthRequest,
    db: Session = Depends(get_db),
) -> Any:
    return await social_auth_controller.login_with_facebook(db=db, body=body)
