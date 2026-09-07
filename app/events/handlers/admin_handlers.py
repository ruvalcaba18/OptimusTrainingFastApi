import logging

from app.events.domain.base_event import BaseEvent

logger = logging.getLogger("optimus.events.admin")


def log_event_to_audit_trail(event: BaseEvent) -> None:
    logger.info(
        "[AUDIT TRAIL] Event: %s | Time: %s",
        event.event_name,
        event.occurred_at.isoformat(),
    )
