from typing import Any

from fastapi import status

from app.core.exceptions.base import AppException


class ForbiddenError(AppException):
    def __init__(self, message: str = "Acceso denegado", details: Any | None = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            details=details,
        )
