from typing import Any

from fastapi import status

from app.core.exceptions.base import AppException


class InternalServerError(AppException):
    def __init__(self, message: str = "Ocurrió un error interno al procesar la solicitud.", details: Any | None = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR",
            details=details,
        )
