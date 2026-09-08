from app.controllers.auth.auth_controller import AuthController, auth_controller
from app.controllers.coaches.coach_controller import CoachController, coach_controller
from app.controllers.competitions.competition_controller import (
    CompetitionController,
    competition_controller,
)
from app.controllers.enterprise.enterprise_controller import (
    EnterpriseController,
    enterprise_controller,
)
from app.controllers.events.event_controller import EventController, event_controller
from app.controllers.excersices.health_question_controller import (
    health_question_controller,
)
from app.controllers.excersices.leisure_activity_controller import (
    leisure_activity_controller,
)
from app.controllers.users.user_controller import UserController, user_controller

__all__ = [
    "AuthController",
    "CoachController",
    "CompetitionController",
    "EnterpriseController",
    "EventController",
    "UserController",
    "auth_controller",
    "coach_controller",
    "competition_controller",
    "enterprise_controller",
    "event_controller",
    "health_question_controller",
    "leisure_activity_controller",
    "user_controller",
]
