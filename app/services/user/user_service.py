from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import Goal, Level, User
from app.schemas.users import UserCreate, UserUpdate


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

        if user_in.goal_code:
            goal = db.query(Goal).filter(Goal.code == user_in.goal_code).first()
            if goal:
                db_user.goal_id = goal.id

        if user_in.level_code:
            level = db.query(Level).filter(Level.code == user_in.level_code).first()
            if level:
                db_user.level_id = level.id

        db.add(db_user)
        db.flush()

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
        from app.models import Condition, Equipment, Goal, Level
        
        goal = db.query(Goal).filter(Goal.code == profile_in.goal_code).first()
        if goal:
            db_obj.goal_id = goal.id

        level = db.query(Level).filter(Level.code == profile_in.level_code).first()
        if level:
            db_obj.level_id = level.id

        if profile_in.equipment_ids is not None:
            equipments = db.query(Equipment).filter(Equipment.id.in_(profile_in.equipment_ids)).all()
            db_obj.equipments = equipments

        if profile_in.pathology_ids is not None:
            pathologies = db.query(Condition).filter(
                Condition.id.in_(profile_in.pathology_ids),
                Condition.type == "PATHOLOGY"
            ).all()
            db_obj.pathologies = pathologies

        if profile_in.disease_ids is not None:
            diseases = db.query(Condition).filter(
                Condition.id.in_(profile_in.disease_ids),
                Condition.type == "DISEASE"
            ).all()
            db_obj.diseases = diseases

        if hasattr(profile_in, "custom_equipment") and profile_in.custom_equipment is not None:
            db_obj.custom_equipment = profile_in.custom_equipment

        if hasattr(profile_in, "session_duration_code") and profile_in.session_duration_code is not None:
            db_obj.session_duration_code = profile_in.session_duration_code

        if hasattr(profile_in, "specific_days") and profile_in.specific_days is not None:
            db_obj.specific_days = ",".join(str(d) for d in profile_in.specific_days)

        if hasattr(profile_in, "leisure_activity_ids") and profile_in.leisure_activity_ids is not None:
            from app.models import LeisureActivityModel
            leisure_activities = db.query(LeisureActivityModel).filter(LeisureActivityModel.id.in_(profile_in.leisure_activity_ids)).all()
            db_obj.leisure_activities = leisure_activities

        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        
        return db_obj



user_service = UserService()
