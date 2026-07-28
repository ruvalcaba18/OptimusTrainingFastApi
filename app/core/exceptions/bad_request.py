from typing import Any, Optional
from fastapi import status
from app.core.exceptions.base import AppException


class BadRequestError(AppException):
    def __init__(self, message: str = "Solicitud inválida", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            code="BAD_REQUEST",
            details=details,
        )
