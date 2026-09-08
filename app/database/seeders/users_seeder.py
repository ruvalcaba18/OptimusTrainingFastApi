import os
import secrets

from app.core.security import get_password_hash
from app.database.seeders.base_seeder import BaseSeeder
from app.models import Goal, Level
from app.models.Enums.UserTier import UserTier
from app.models.user.user import User

_ADMIN_PASSWORD: str = os.getenv("SEED_ADMIN_PASSWORD") or secrets.token_urlsafe(16)
_APPLE_PASSWORD: str = os.getenv("SEED_APPLE_PASSWORD") or secrets.token_urlsafe(16)

_USERS: list[dict] = [
    {
        "email": "jael.ruvalcaba@uabc.edu.mx",
        "first_name": "Jael",
        "last_name": "Ruvalcaba",
        "phone": "6641000001",
        "age": 25,
        "weight": 75.0,
        "height": 175.0,
        "exercise_frequency": "5-6",
        "training_type": "strength",
        "gender": "M",
        "tier": UserTier.PREMIUM,
        "goal_code": "GMM",
        "level_code": "NIV3",
        "password_key": "admin",
    },
    {
        "email": "andres.geraldo@uabc.edu.mx",
        "first_name": "Andrés",
        "last_name": "Geraldo",
        "phone": "6641000002",
        "age": 25,
        "weight": 72.0,
        "height": 178.0,
        "exercise_frequency": "3-4",
        "training_type": "general_fitness",
        "gender": "M",
        "tier": UserTier.PREMIUM,
        "goal_code": "SB",
        "level_code": "NIV2",
        "password_key": "admin",
    },
    {
        "email": "apple.review@optimustraining.app",
        "first_name": "Apple",
        "last_name": "Reviewer",
        "phone": "4081000001",
        "age": 30,
        "weight": 70.0,
        "height": 170.0,
        "exercise_frequency": "3-4",
        "training_type": "general_fitness",
        "gender": "M",
        "tier": UserTier.PREMIUM,
        "goal_code": "SB",
        "level_code": "NIV1",
        "password_key": "apple",
    },
]


class UsersSeeder(BaseSeeder):
    def seed(self) -> None:
        goals_map = {g.code: g for g in self.session.query(Goal).all()}
        levels_map = {l.code: l for l in self.session.query(Level).all()}

        for data in _USERS:
            self._upsert_user(data, goals_map, levels_map)

        self.session.commit()

    def _upsert_user(
        self,
        data: dict,
        goals_map: dict,
        levels_map: dict,
    ) -> None:
        already_exists = self.session.query(User).filter_by(email=data["email"]).first()
        if already_exists:
            return

        password = (
            _ADMIN_PASSWORD if data["password_key"] == "admin" else _APPLE_PASSWORD
        )

        user = User(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            age=data["age"],
            weight=data["weight"],
            height=data["height"],
            exercise_frequency=data["exercise_frequency"],
            training_type=data["training_type"],
            gender=data["gender"],
            tier=data["tier"],
            hashed_password=get_password_hash(password),
            is_active=True,
            goal=goals_map.get(data["goal_code"]),
            level=levels_map.get(data["level_code"]),
        )
        self.session.add(user)
