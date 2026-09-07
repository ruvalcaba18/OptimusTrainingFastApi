import logging

from app.events.dispatcher import EventDispatcher, event_bus
from app.events.domain import (
    RoutineGeneratedEvent,
    UserRegisteredEvent,
    UserTierChangedEvent,
    WorkoutCompletedEvent,
)
from app.events.handlers import (
    handle_routine_generated,
    handle_user_registered,
    handle_user_tier_changed,
    handle_workout_completed,
    log_event_to_audit_trail,
)

logger = logging.getLogger("optimus.events.setup")


def register_event_handlers(dispatcher: EventDispatcher = event_bus) -> None:
    logger.info("Initializing Event-Driven Architecture subscriptions...")

    dispatcher.subscribe(UserRegisteredEvent, handle_user_registered)
    dispatcher.subscribe(UserRegisteredEvent, log_event_to_audit_trail)
    dispatcher.subscribe(UserTierChangedEvent, handle_user_tier_changed)
    dispatcher.subscribe(UserTierChangedEvent, log_event_to_audit_trail)

    dispatcher.subscribe(RoutineGeneratedEvent, handle_routine_generated)
    dispatcher.subscribe(RoutineGeneratedEvent, log_event_to_audit_trail)
    dispatcher.subscribe(WorkoutCompletedEvent, handle_workout_completed)
    dispatcher.subscribe(WorkoutCompletedEvent, log_event_to_audit_trail)

    logger.info("Event subscriptions configured successfully.")
