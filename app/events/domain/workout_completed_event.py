from dataclasses import dataclass

from app.events.domain.base_event import BaseEvent


@dataclass(frozen=True, kw_only=True)
class WorkoutCompletedEvent(BaseEvent):
    user_id: int
    week: int
    day: int
    exercise_count: int
