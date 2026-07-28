from app.core.exceptions import (
    NotFoundError,
    ConflictError,
    BadRequestError,
)


class EventNotFoundError(NotFoundError):
    def __init__(self, message: str = "Evento no encontrado"):
        super().__init__(message=message)


class EventCancelledError(BadRequestError):
    def __init__(self, message: str = "No puedes unirte a un evento cancelado"):
        super().__init__(message=message)


class EventFullError(BadRequestError):
    def __init__(self, message: str = "El evento ha alcanzado el máximo de participantes"):
        super().__init__(message=message)


class AlreadyJoinedEventError(ConflictError):
    def __init__(self, message: str = "Ya estás inscrito en este evento"):
        super().__init__(message=message)


class NotJoinedEventError(NotFoundError):
    def __init__(self, message: str = "No estás inscrito en este evento"):
        super().__init__(message=message)
