from app.core.exceptions import (
    NotFoundError,
    ConflictError,
    BadRequestError,
)


class CoachNotFoundError(NotFoundError):
    def __init__(self, message: str = "Coach no encontrado"):
        super().__init__(message=message)


class CoachAlreadyExistsError(ConflictError):
    def __init__(self, message: str = "Ya tienes un perfil de coach registrado."):
        super().__init__(message=message)


class CoachUnavailableError(BadRequestError):
    def __init__(self, message: str = "Este coach no está disponible actualmente"):
        super().__init__(message=message)


class SelfBookingError(BadRequestError):
    def __init__(self, message: str = "No puedes contratarte a ti mismo"):
        super().__init__(message=message)


class BookingNotFoundError(NotFoundError):
    def __init__(self, message: str = "Reservación no encontrada"):
        super().__init__(message=message)


class SessionAlreadyReviewedError(ConflictError):
    def __init__(self, message: str = "Ya calificaste esta sesión"):
        super().__init__(message=message)
