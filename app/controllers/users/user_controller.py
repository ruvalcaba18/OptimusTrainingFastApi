"""
User controller — handles HTTP-level logic and calls services.
No direct database queries here; that's the service's job.
"""
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.users import UserCreate, UserUpdate, UserResponse
from app.services.user_service import user_service
from app.services.upload_service import save_profile_picture, delete_profile_picture


class UserController:

    # ─── List ─────────────────────────────────────────────────────────────
    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        return user_service.get_multi(db, skip=skip, limit=limit)

    # ─── Get one ──────────────────────────────────────────────────────────
    @staticmethod
    def get_user(db: Session, user_id: int) -> UserResponse:
        user = user_service.get_by_id(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return user

    # ─── Create ───────────────────────────────────────────────────────────
    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> UserResponse:
        existing = user_service.get_by_email(db, email=user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un usuario con este correo.",
            )
        return user_service.create(db, user_in=user_in)

    # ─── Update ───────────────────────────────────────────────────────────
    @staticmethod
    def update_user(db: Session, user_id: int, user_in: UserUpdate, current_user: User) -> UserResponse:
        user = user_service.get_by_id(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        # Only the owner can update their own profile
        if user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
        return user_service.update(db, db_obj=user, user_in=user_in)

    # ─── Upload profile picture ────────────────────────────────────────────
    @staticmethod
    async def upload_profile_picture(
        db: Session, user_id: int, file: UploadFile, current_user: User
    ) -> UserResponse:
        user = user_service.get_by_id(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        if user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")

        url = await save_profile_picture(user_id=user_id, file=file)
        return user_service.update_profile_picture(db, db_obj=user, url=url)

    # ─── Delete ───────────────────────────────────────────────────────────
    @staticmethod
    def delete_user(db: Session, user_id: int, current_user: User) -> UserResponse:
        user = user_service.get_by_id(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        if user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
        delete_profile_picture(user_id=user_id)
        return user_service.delete(db, user_id=user_id)


user_controller = UserController()
