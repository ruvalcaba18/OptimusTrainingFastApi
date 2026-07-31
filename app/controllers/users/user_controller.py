from datetime import timedelta
from typing import final
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.users import (
    UserCreate, 
    UserUpdate, 
    UserResponse, 
    UserRegistrationResponse, 
    Token,
)
from app.services import user_service
from app.services import save_profile_picture, delete_profile_picture
from app.core import security
from app.core.config import settings
from app.controllers.users.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
)
from app.core.exceptions import ForbiddenError
from app.core.error_handlers import handle_controller_errors


@final
class UserController:

    @staticmethod
    @handle_controller_errors
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        return user_service.get_multi(db, skip=skip, limit=limit)

    @staticmethod
    @handle_controller_errors
    def get_user(db: Session, user_id: int) -> UserResponse:
        user = user_service.get_by_id(db, user_id=user_id)
        if not user:
            raise UserNotFoundError()
        return user

    @staticmethod
    @handle_controller_errors
    def create_user(db: Session, user_in: UserCreate) -> UserRegistrationResponse:
        existing = user_service.get_by_email(db, email=user_in.email)
        if existing:
            raise UserAlreadyExistsError()

        user = user_service.create(db, user_in=user_in)

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = Token(
            access_token=security.create_access_token(
                user.email, expires_delta=access_token_expires
            ),
            refresh_token=security.create_refresh_token(user.email),
            token_type="bearer",
        )

        db.commit()
        
        return UserRegistrationResponse(user=UserResponse.model_validate(user), token=token)

    @staticmethod
    @handle_controller_errors
    def update_user(db: Session, user_id: int, user_in: UserUpdate, current_user: User) -> UserResponse:
        user = user_service.get_by_id(db, user_id=user_id)
        if not user:
            raise UserNotFoundError()

        if user.id != current_user.id:
            raise ForbiddenError("No autorizado")

        updated_user = user_service.update(db, db_obj=user, user_in=user_in)
        db.commit()
        
        return updated_user

    @staticmethod
    @handle_controller_errors
    async def upload_profile_picture(
        db: Session, user_id: int, file: UploadFile, current_user: User
    ) -> UserResponse:
        user = user_service.get_by_id(db, user_id=user_id)
        if not user:
            raise UserNotFoundError()
        if user.id != current_user.id:
            raise ForbiddenError("No autorizado")

        url = await save_profile_picture(user_id=user_id, file=file)
        updated_user = user_service.update_profile_picture(db, db_obj=user, url=url)
        db.commit()
        
        return updated_user

    @staticmethod
    @handle_controller_errors
    def delete_user(db: Session, user_id: int, current_user: User) -> UserResponse:
        user = user_service.get_by_id(db, user_id=user_id)
        if not user:
            raise UserNotFoundError()
        if user.id != current_user.id:
            raise ForbiddenError("No autorizado")

        delete_profile_picture(user_id=user_id)
        deleted_user = user_service.delete(db, user_id=user_id)
        db.commit()
        
        return deleted_user

    @staticmethod
    @handle_controller_errors
    def update_training_profile(db: Session, profile_in, current_user: User):
        updated_user = user_service.update_training_profile(db, db_obj=current_user, profile_in=profile_in)
        db.commit()
        return updated_user


user_controller = UserController()
