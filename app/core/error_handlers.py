import functools
import inspect
import logging
import traceback
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import (
    AppException,
    BadRequestError,
    ForbiddenError,
    InternalServerError,
)

logger = logging.getLogger("optimus.errors")


def _error_response(status_code: int, code: str, message: str, details=None) -> JSONResponse:
    body = {"error": {"code": code, "message": message}}
    if details:
        body["error"]["details"] = details
    return JSONResponse(status_code=status_code, content=body)


def _extract_db_session(*args, **kwargs) -> Session | None:
    for arg in args:
        if isinstance(arg, Session):
            return arg
    for v in kwargs.values():
        if isinstance(v, Session):
            return v
    return None


def handle_controller_errors(func):
    """
    Decorator for controller methods that:
    1. Automatic DB rollback on exception if Session is present.
    2. Lets AppException and StarletteHTTPException pass through to FastAPI handlers.
    3. Translates standard Python exceptions (ValueError, PermissionError) into domain exceptions.
    4. Catches unexpected exceptions, logs traceback, calls rollback, and raises InternalServerError safely.
    """
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except (AppException, StarletteHTTPException):
                db = _extract_db_session(*args, **kwargs)
                if db:
                    db.rollback()
                raise
            except ValueError as e:
                db = _extract_db_session(*args, **kwargs)
                if db:
                    db.rollback()
                raise BadRequestError(str(e))
            except PermissionError as e:
                db = _extract_db_session(*args, **kwargs)
                if db:
                    db.rollback()
                raise ForbiddenError(str(e))
            except Exception as e:
                db = _extract_db_session(*args, **kwargs)
                if db:
                    db.rollback()
                logger.error("Unhandled error in controller function '%s':\n%s", func.__name__, traceback.format_exc())
                raise InternalServerError("Ocurrió un error interno al procesar la solicitud.")
        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (AppException, StarletteHTTPException):
                db = _extract_db_session(*args, **kwargs)
                if db:
                    db.rollback()
                raise
            except ValueError as e:
                db = _extract_db_session(*args, **kwargs)
                if db:
                    db.rollback()
                raise BadRequestError(str(e))
            except PermissionError as e:
                db = _extract_db_session(*args, **kwargs)
                if db:
                    db.rollback()
                raise ForbiddenError(str(e))
            except Exception as e:
                db = _extract_db_session(*args, **kwargs)
                if db:
                    db.rollback()
                logger.error("Unhandled error in controller function '%s':\n%s", func.__name__, traceback.format_exc())
                raise InternalServerError("Ocurrió un error interno al procesar la solicitud.")
        return sync_wrapper


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning("AppException %s %s → %s: %s", exc.status_code, request.url.path, exc.code, exc.message)
        return _error_response(exc.status_code, exc.code, exc.message, exc.details)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        code_map = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
            408: "REQUEST_TIMEOUT",
            409: "CONFLICT",
            410: "GONE",
            413: "PAYLOAD_TOO_LARGE",
            415: "UNSUPPORTED_MEDIA_TYPE",
            422: "UNPROCESSABLE_ENTITY",
            429: "RATE_LIMIT_EXCEEDED",
            500: "INTERNAL_SERVER_ERROR",
            502: "BAD_GATEWAY",
            503: "SERVICE_UNAVAILABLE",
        }
        code = code_map.get(exc.status_code, "HTTP_ERROR")
        logger.warning("HTTP %s %s → %s: %s", exc.status_code, request.url.path, code, exc.detail)
        return _error_response(exc.status_code, code, str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        field_errors = []
        for error in exc.errors():
            loc = " → ".join(str(l) for l in error["loc"] if l != "body")
            field_errors.append({"field": loc, "message": error["msg"], "type": error["type"]})
        logger.info("Validation error on %s: %s", request.url.path, field_errors)
        return _error_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "VALIDATION_ERROR",
            "Los datos enviados no son válidos.",
            field_errors,
        )

    @app.exception_handler(ResponseValidationError)
    async def response_validation_handler(request: Request, exc: ResponseValidationError):
        logger.error("Response validation error on %s: %s", request.url.path, exc)
        return _error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "RESPONSE_VALIDATION_ERROR",
            "Error interno de serialización de respuesta.",
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        logger.error("DB IntegrityError on %s: %s", request.url.path, exc.orig)
        return _error_response(
            status.HTTP_409_CONFLICT,
            "DATABASE_CONFLICT",
            "El recurso ya existe o viola una restricción de integridad.",
        )

    @app.exception_handler(OperationalError)
    async def operational_error_handler(request: Request, exc: OperationalError):
        logger.critical("DB OperationalError on %s: %s", request.url.path, exc)
        return _error_response(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "DATABASE_UNAVAILABLE",
            "La base de datos no está disponible temporalmente.",
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        logger.warning("ValueError on %s: %s", request.url.path, exc)
        return _error_response(
            status.HTTP_400_BAD_REQUEST,
            "INVALID_VALUE",
            str(exc),
        )

    @app.exception_handler(PermissionError)
    async def permission_error_handler(request: Request, exc: PermissionError):
        logger.warning("PermissionError on %s", request.url.path)
        return _error_response(
            status.HTTP_403_FORBIDDEN,
            "FORBIDDEN",
            "No tienes permiso para realizar esta acción.",
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.critical(
            "Unhandled exception on %s %s:\n%s",
            request.method,
            request.url.path,
            traceback.format_exc(),
        )
        return _error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "INTERNAL_SERVER_ERROR",
            "Ocurrió un error inesperado. Por favor intenta de nuevo.",
        )
