from app.controllers.users.user_controller import user_controller, UserController
from app.controllers.auth.auth_controller import auth_controller, AuthController
from app.controllers.enterprise.enterprise_controller import enterprise_controller, EnterpriseController
from app.controllers.coaches.coach_controller import coach_controller, CoachController
from app.controllers.events.event_controller import event_controller, EventController
from app.controllers.competitions.competition_controller import competition_controller, CompetitionController

__all__ = [
    "user_controller",
    "UserController",
    "auth_controller",
    "AuthController",
    "enterprise_controller",
    "EnterpriseController",
    "coach_controller",
    "CoachController",
    "event_controller",
    "EventController",
    "competition_controller",
    "CompetitionController",
]
