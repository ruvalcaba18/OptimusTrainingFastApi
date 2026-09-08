from dataclasses import dataclass

from app.events.domain.base_event import BaseEvent


@dataclass(frozen=True, kw_only=True)
class UserRegisteredEvent(BaseEvent):
    user_id: int
    email: str
    first_name: str
    last_name: str
    auth_provider: str | None = "email"
