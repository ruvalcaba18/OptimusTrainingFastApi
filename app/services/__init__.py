from app.services.coach.coach_service import coach_service
from app.services.enterprise.enterprise_service import enterprise_service
from app.services.excersice.condition_service import condition_service
from app.services.excersice.equipment_service import equipment_service
from app.services.excersice.excersice_service import excersice_service
from app.services.excersice.goal_service import goal_service
from app.services.excersice.gym_equipment_service import gym_equipment_service
from app.services.excersice.health_question_service import health_question_service
from app.services.excersice.home_equipment_service import home_equipment_service
from app.services.excersice.leisure_activity_service import leisure_activity_service
from app.services.excersice.level_service import level_service
from app.services.excersice.method_service import method_service
from app.services.excersice.outdoor_equipment_service import outdoor_equipment_service
from app.services.excersice.session_duration_service import session_duration_service
from app.services.excersice.workout_hybird_places_service import (
    workout_hybrid_places_service,
)
from app.services.excersice.workout_place_service import workout_place_service
from app.services.social.competition_service import competition_service
from app.services.social.event_service import event_service
from app.services.training.exercise_selector import exercise_selector
from app.services.training.routine_generator import routine_generator
from app.services.training.training_service import training_service
from app.services.user.email_service import email_service
from app.services.user.social_auth import (
    AppleProvider,
    FacebookProvider,
    GoogleProvider,
)
from app.services.user.upload_service import (
    delete_profile_picture,
    save_profile_picture,
)
from app.services.user.user_service import user_service

__all__ = [
    "user_service",
    "save_profile_picture",
    "delete_profile_picture",
    "email_service",
    "AppleProvider",
    "GoogleProvider",
    "FacebookProvider",
    "excersice_service",
    "condition_service",
    "goal_service",
    "level_service",
    "method_service",
    "equipment_service",
    "training_service",
    "routine_generator",
    "exercise_selector",
    "session_duration_service",
    "workout_place_service",
    "workout_hybrid_places_service",
    "gym_equipment_service",
    "home_equipment_service",
    "outdoor_equipment_service",
    "leisure_activity_service",
    "health_question_service",
    "coach_service",
    "competition_service",
    "event_service",
    "enterprise_service",
]
