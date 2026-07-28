from typing import Any, Optional
from fastapi import status
from app.core.exceptions.base import AppException


class UnprocessableEntityError(AppException):
    def __init__(self, message: str = "Los datos no pudieron ser procesados", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="UNPROCESSABLE_ENTITY",
            details=details,
        )
