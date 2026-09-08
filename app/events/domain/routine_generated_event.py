from dataclasses import dataclass

from app.events.domain.base_event import BaseEvent


@dataclass(frozen=True, kw_only=True)
class RoutineGeneratedEvent(BaseEvent):
    user_id: int
    weeks_count: int
    trigger_source: str
    week: int | None = None
    day: int | None = None
