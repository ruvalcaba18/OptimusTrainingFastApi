from dataclasses import dataclass

from app.events.domain.base_event import BaseEvent


@dataclass(frozen=True, kw_only=True)
class UserTierChangedEvent(BaseEvent):
    user_id: int
    old_tier: str
    new_tier: str
