from app.core.exceptions import (
    BadRequestError,
    ForbiddenError,
    UnauthorizedError,
)


class InvalidCredentialsError(UnauthorizedError):
    def __init__(self, message: str = "Correo o contraseña incorrectos"):
        super().__init__(message=message)


class InactiveAccountError(ForbiddenError):
    def __init__(self, message: str = "Cuenta inactiva"):
        super().__init__(message=message)


class InvalidRefreshTokenError(UnauthorizedError):
    def __init__(self, message: str = "Token de renovación inválido o expirado"):
        super().__init__(message=message)


class InvalidResetTokenError(BadRequestError):
    def __init__(self, message: str = "Token de recuperación inválido o expirado"):
        super().__init__(message=message)
