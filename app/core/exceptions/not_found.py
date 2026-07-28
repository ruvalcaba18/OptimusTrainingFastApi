from typing import Any, Optional
from fastapi import status
from app.core.exceptions.base import AppException


class NotFoundError(AppException):
    def __init__(self, message: str = "Recurso no encontrado", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
            details=details,
        )
