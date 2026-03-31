from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.users import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserService:
                                                                               

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

                                                                               
    @staticmethod
    def create(db: Session, user_in: UserCreate) -> User:
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            phone=user_in.phone,
            age=user_in.age,
            weight=user_in.weight,
            height=user_in.height,
            exercise_frequency=user_in.exercise_frequency,
            training_type=user_in.training_type.value,
            is_active=True,
        )
        db.add(db_user)
        db.flush()                                                                   
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update(db: Session, db_obj: User, user_in: UserUpdate) -> User:
        update_data = user_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        if "training_type" in update_data and update_data["training_type"] is not None:
            update_data["training_type"] = update_data["training_type"].value

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_profile_picture(db: Session, db_obj: User, url: str) -> User:
        db_obj.profile_picture_url = url
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, user_id: int) -> Optional[User]:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.flush()
        return db_user


user_service = UserService()
