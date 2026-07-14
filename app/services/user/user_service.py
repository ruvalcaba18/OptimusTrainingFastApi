from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import User
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
            gender=user_in.gender.value if user_in.gender else None,
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

        if "gender" in update_data and update_data["gender"] is not None:
            update_data["gender"] = update_data["gender"].value

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

    @staticmethod
    def update_training_profile(db: Session, db_obj: User, profile_in) -> User:
        from app.models import UserProfile, Goal, Level, Equipment, Condition
        
        # 1. Asegurar que el perfil exista
        if not db_obj.profile:
            db_obj.profile = UserProfile(id=db_obj.id)
            db.add(db_obj.profile)

        # 2. Buscar y asignar Goal
        goal = db.query(Goal).filter(Goal.code == profile_in.goal_code).first()
        if goal:
            db_obj.profile.goal_id = goal.id

        # 3. Buscar y asignar Level
        level = db.query(Level).filter(Level.code == profile_in.level_code).first()
        if level:
            db_obj.profile.level_id = level.id

        # 4. Asignar Equipamiento
        if profile_in.equipment_ids is not None:
            equipments = db.query(Equipment).filter(Equipment.id.in_(profile_in.equipment_ids)).all()
            db_obj.equipments = equipments

        # 5. Asignar Patologías
        if profile_in.pathology_ids is not None:
            pathologies = db.query(Condition).filter(
                Condition.id.in_(profile_in.pathology_ids),
                Condition.type == "PATHOLOGY"
            ).all()
            db_obj.pathologies = pathologies

        # 6. Asignar Enfermedades
        if profile_in.disease_ids is not None:
            diseases = db.query(Condition).filter(
                Condition.id.in_(profile_in.disease_ids),
                Condition.type == "DISEASE"
            ).all()
            db_obj.diseases = diseases

        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj



user_service = UserService()
