import secrets
from typing import Callable, Awaitable

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.user_service import user_service
from app.schemas.users import Token
from app.schemas.users.social_auth_request import SocialAuthRequest
from app.core import security
from app.services.social_auth import AppleProvider, GoogleProvider, FacebookProvider


class SocialAuthController:

    @staticmethod
    async def login_with_apple(db: Session, body: SocialAuthRequest) -> Token:
        return await SocialAuthController._handle(
            db=db,
            body=body,
            provider="apple",
            verify_fn=AppleProvider.verify_token,
        )

    @staticmethod
    async def login_with_google(db: Session, body: SocialAuthRequest) -> Token:
        return await SocialAuthController._handle(
            db=db,
            body=body,
            provider="google",
            verify_fn=GoogleProvider.verify_token,
        )

    @staticmethod
    async def login_with_facebook(db: Session, body: SocialAuthRequest) -> Token:
        return await SocialAuthController._handle(
            db=db,
            body=body,
            provider="facebook",
            verify_fn=FacebookProvider.verify_token,
        )

    # ── Private

    @staticmethod
    async def _handle(
        db: Session,
        body: SocialAuthRequest,
        provider: str,
        verify_fn: Callable[[str], Awaitable[dict]],
    ) -> Token:
        social_user = await verify_fn(body.token)

        user = await SocialAuthController._find_or_create_user(
            db=db,
            social_user=social_user,
            provider=provider,
            first_name=body.first_name,
            last_name=body.last_name,
        )

        return Token(
            access_token=security.create_access_token(user.email),
            refresh_token=security.create_refresh_token(user.email),
            token_type="bearer",
        )

    @staticmethod
    async def _find_or_create_user(
        db: Session,
        social_user: dict,
        provider: str,
        first_name: str | None,
        last_name: str | None,
    ) -> User:
        email = social_user["email"]
        existing_user = user_service.get_by_email(db, email=email)

        if existing_user:
            if not existing_user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Cuenta desactivada. Contacta al soporte.",
                )
            return existing_user

        return SocialAuthController._create_social_user(
            db=db,
            email=email,
            social_user=social_user,
            provider=provider,
            first_name=first_name,
            last_name=last_name,
        )

    @staticmethod
    def _create_social_user(
        db: Session,
        email: str,
        social_user: dict,
        provider: str,
        first_name: str | None,
        last_name: str | None,
    ) -> User:
        provider_name = social_user.get("name") or ""
        name_parts = provider_name.split(" ", 1)

        resolved_first_name = (
            first_name
            or (name_parts[0] if name_parts else None)
            or email.split("@")[0]
        )
        resolved_last_name = (
            last_name
            or (name_parts[1] if len(name_parts) > 1 else None)
            or f"{provider.capitalize()} User"
        )

        random_password = secrets.token_hex(32)

        db_user = User(
            email=email,
            hashed_password=security.get_password_hash(random_password),
            first_name=resolved_first_name,
            last_name=resolved_last_name,
            phone="",
            age=0,
            weight=0.0,
            height=0.0,
            exercise_frequency="",
            training_type="",
            is_active=True,
            auth_provider=provider,
        )

        db.add(db_user)
        db.flush()
        db.refresh(db_user)
        return db_user


social_auth_controller = SocialAuthController()
