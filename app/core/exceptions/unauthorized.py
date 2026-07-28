from typing import Any, Optional
from fastapi import status
from app.core.exceptions.base import AppException


class UnauthorizedError(AppException):
    def __init__(self, message: str = "No autorizado", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="UNAUTHORIZED",
            details=details,
        )
