import logging

logger = logging.getLogger("optimus.events")


class EventDispatcher:
    def __init__(self):
        self._subscribers: dict[type, list] = {}

    def subscribe(self, event_type: type, handler) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        if handler not in self._subscribers[event_type]:
            self._subscribers[event_type].append(handler)
            logger.info(
                "Subscribed handler '%s' to event '%s'",
                handler.__name__,
                event_type.__name__,
            )

    def dispatch(self, event: object, db_session=None) -> None:
        event_type = type(event)
        handlers = self._subscribers.get(event_type, [])

        if not handlers:
            logger.debug("No handlers registered for event: %s", event_type.__name__)
            return

        logger.info(
            "Dispatching event: %s to %d handler(s)", event_type.__name__, len(handlers)
        )

        for handler in handlers:
            try:
                if db_session is not None:
                    handler(event, db_session)
                else:
                    handler(event)
            except Exception as exc:
                logger.error(
                    "Error executing handler '%s' for event '%s': %s",
                    getattr(handler, "__name__", str(handler)),
                    event_type.__name__,
                    exc,
                    exc_info=True,
                )

    def clear(self) -> None:
        self._subscribers.clear()


event_bus = EventDispatcher()
