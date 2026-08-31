from app.core.exceptions import (
    ConflictError,
    NotFoundError,
)


class UserNotFoundError(NotFoundError):
    def __init__(self, message: str = "Usuario no encontrado"):
        super().__init__(message=message)


class UserAlreadyExistsError(ConflictError):
    def __init__(self, message: str = "Ya existe un usuario con este correo."):
        super().__init__(message=message)
