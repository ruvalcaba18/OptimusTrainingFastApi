import logging

from app.events.domain.routine_generated_event import RoutineGeneratedEvent
from app.events.domain.workout_completed_event import WorkoutCompletedEvent

logger = logging.getLogger("optimus.events.routine")


def handle_routine_generated(event: RoutineGeneratedEvent) -> None:
    logger.info(
        "[ROUTINE GENERATED] Routine created for User #%d | Weeks: %d | Source: %s (week=%s, day=%s)",
        event.user_id,
        event.weeks_count,
        event.trigger_source,
        event.week,
        event.day,
    )


def handle_workout_completed(event: WorkoutCompletedEvent) -> None:
    logger.info(
        "[WORKOUT COMPLETED] User #%d completed workout W%d-D%d (%d exercises)",
        event.user_id,
        event.week,
        event.day,
        event.exercise_count,
    )
