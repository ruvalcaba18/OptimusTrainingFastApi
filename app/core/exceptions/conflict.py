from typing import Any, Optional
from fastapi import status
from app.core.exceptions.base import AppException


class ConflictError(AppException):
    def __init__(self, message: str = "Conflicto con el estado actual del recurso", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT",
            details=details,
        )
