import logging

from app.events.domain.user_registered_event import UserRegisteredEvent
from app.events.domain.user_tier_changed_event import UserTierChangedEvent

logger = logging.getLogger("optimus.events.user")


def handle_user_registered(event: UserRegisteredEvent) -> None:
    logger.info(
        "[USER REGISTERED] User #%d (%s %s) registered with email: %s via %s",
        event.user_id,
        event.first_name,
        event.last_name,
        event.email,
        event.auth_provider,
    )


def handle_user_tier_changed(event: UserTierChangedEvent) -> None:
    logger.info(
        "[TIER CHANGED] User #%d tier changed: %s -> %s",
        event.user_id,
        event.old_tier,
        event.new_tier,
    )
