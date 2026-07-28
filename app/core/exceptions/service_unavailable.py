from typing import Any, Optional
from fastapi import status
from app.core.exceptions.base import AppException


class ServiceUnavailableError(AppException):
    def __init__(self, message: str = "Servicio no disponible temporalmente", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="SERVICE_UNAVAILABLE",
            details=details,
        )
