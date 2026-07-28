from app.core.exceptions import (
    NotFoundError,
    ConflictError,
    BadRequestError,
)


class EnterpriseNotFoundError(NotFoundError):
    def __init__(self, message: str = "Empresa no encontrada"):
        super().__init__(message=message)


class InvalidEnterpriseCodeError(BadRequestError):
    def __init__(self, message: str = "Código inválido."):
        super().__init__(message=message)


class EnterpriseCodeExpiredError(BadRequestError):
    def __init__(self, message: str = "Este código ha expirado."):
        super().__init__(message=message)


class EnterpriseCodeAlreadyUsedError(BadRequestError):
    def __init__(self, message: str = "Este código ya fue utilizado."):
        super().__init__(message=message)


class AlreadyLinkedEnterpriseError(ConflictError):
    def __init__(self, message: str = "Ya estás vinculado a esta empresa."):
        super().__init__(message=message)


class ActiveBreakNotFoundError(NotFoundError):
    def __init__(self, message: str = "Pausa activa no encontrada"):
        super().__init__(message=message)


class BreakAlreadyCompletedError(BadRequestError):
    def __init__(self, message: str = "Esta pausa ya fue completada"):
        super().__init__(message=message)
