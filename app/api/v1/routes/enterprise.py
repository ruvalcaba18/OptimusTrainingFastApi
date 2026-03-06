"""
Enterprise routes for API v1.
Thin layer: validates HTTP input, calls controller, returns response.

Diseño RESTful plano — los IDs siempre van al final del path.
Identificadores contextuales van como query params o en el body.
"""
from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.controllers.enterprise.enterprise_controller import enterprise_controller
from app.schemas.enterprise import (
    EnterpriseCreate,
    EnterpriseResponse,
    ValidateCodeRequest,
    ValidateCodeResponse,
    CodeGenerateRequest,
    EnterpriseCodeResponse,
    EnterpriseMemberResponse,
    ActiveBreakCreate,
    ActiveBreakResponse,
    ActiveBreakLogCreate,
    ActiveBreakLogResponse,
    ActiveBreakStatsResponse,
)

router = APIRouter()


# ━━━━━━━━━━━━━━━━━━━━━━━━━  Enterprise  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post(
    "/",
    response_model=EnterpriseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear empresa",
)
def create_enterprise(
    enterprise_in: EnterpriseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Registra una nueva empresa en el sistema. Requiere autenticación."""
    return enterprise_controller.create_enterprise(db, enterprise_in=enterprise_in)


@router.get(
    "/my-enterprise",
    response_model=EnterpriseResponse,
    summary="Mi empresa",
)
def get_my_enterprise(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna la empresa a la que está vinculado el usuario autenticado."""
    return enterprise_controller.get_my_enterprise(db, current_user=current_user)


# ━━━━━━━━━━━━━━━━━━━━━━━  Code Validation  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post(
    "/validate-code",
    response_model=ValidateCodeResponse,
    summary="Validar código de empresa",
)
def validate_code(
    code_in: ValidateCodeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Valida un código proporcionado por la empresa.
    Si el código es válido, no ha sido usado y no ha expirado,
    el usuario se vincula a la empresa automáticamente.
    El código queda marcado como usado y no puede reutilizarse.
    """
    return enterprise_controller.validate_code(
        db, code_in=code_in, current_user=current_user
    )


# ━━━━━━━━━━━━━━━━━━━━━━━  Code Management  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post(
    "/codes",
    response_model=list[EnterpriseCodeResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Generar códigos de empresa",
)
def generate_codes(
    code_req: CodeGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Genera N códigos de un solo uso para una empresa.
    El enterprise_id se envía en el body.
    Cada código tiene formato XXXX-XXXX y expira en los días indicados.
    """
    return enterprise_controller.generate_codes(db, code_req=code_req)


@router.get(
    "/codes",
    response_model=list[EnterpriseCodeResponse],
    summary="Listar códigos de empresa",
)
def list_codes(
    enterprise_id: int = Query(..., description="ID de la empresa"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna los códigos generados para una empresa."""
    return enterprise_controller.list_codes(
        db, enterprise_id=enterprise_id, skip=skip, limit=limit
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━  Members  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.get(
    "/members",
    response_model=list[EnterpriseMemberResponse],
    summary="Listar miembros de empresa",
)
def list_members(
    enterprise_id: int = Query(..., description="ID de la empresa"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna los miembros activos de una empresa."""
    return enterprise_controller.list_members(
        db, enterprise_id=enterprise_id, skip=skip, limit=limit
    )


# ━━━━━━━━━━━━━━━━━━━━━━  Active Breaks  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post(
    "/active-breaks",
    response_model=ActiveBreakResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear pausa activa",
)
def create_active_break(
    break_in: ActiveBreakCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Crea una nueva plantilla de pausa activa (10, 20 o 30 minutos)."""
    return enterprise_controller.create_active_break(db, break_in=break_in)


@router.get(
    "/active-breaks",
    response_model=list[ActiveBreakResponse],
    summary="Listar pausas activas",
)
def list_active_breaks(
    duration: Optional[int] = Query(None, description="Filtrar por duración: 10, 20 o 30"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Lista las pausas activas disponibles.
    Se puede filtrar por duración (10/20/30 min) y categoría.
    """
    return enterprise_controller.list_active_breaks(
        db, duration=duration, category=category, skip=skip, limit=limit
    )


@router.get(
    "/active-breaks/{break_id}",
    response_model=ActiveBreakResponse,
    summary="Detalle de pausa activa",
)
def get_active_break(
    break_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna el detalle de una pausa activa específica."""
    return enterprise_controller.get_active_break(db, break_id=break_id)


# ━━━━━━━━━━━━━━━━━━━━━━  Break Logs  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post(
    "/break-logs",
    response_model=ActiveBreakLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Iniciar pausa activa",
)
def start_break(
    log_in: ActiveBreakLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Registra que el usuario comenzó una pausa activa. El session_id va en el body."""
    return enterprise_controller.start_break(
        db, log_in=log_in, current_user=current_user
    )


@router.put(
    "/break-logs/{log_id}",
    response_model=ActiveBreakLogResponse,
    summary="Completar pausa activa",
)
def complete_break(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Marca una pausa activa como completada. El ID del log va al final del path."""
    return enterprise_controller.complete_break(
        db, log_id=log_id, current_user=current_user
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━  Stats  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.get(
    "/my-stats",
    response_model=ActiveBreakStatsResponse,
    summary="Mis estadísticas de pausas activas",
)
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Devuelve estadísticas personales del usuario:
    total de sesiones iniciadas, completadas, minutos acumulados
    y desglose por categoría.
    """
    return enterprise_controller.get_my_stats(
        db, current_user=current_user
    )
