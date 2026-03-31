from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.cache import cache_get, cache_set, cache_delete_pattern, make_key
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
    return enterprise_controller.get_my_enterprise(db, current_user=current_user)


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
    return enterprise_controller.validate_code(
        db, code_in=code_in, current_user=current_user
    )


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
    return enterprise_controller.list_codes(
        db, enterprise_id=enterprise_id, skip=skip, limit=limit
    )


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
    return enterprise_controller.list_members(
        db, enterprise_id=enterprise_id, skip=skip, limit=limit
    )


@router.post(
    "/active-breaks",
    response_model=ActiveBreakResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear pausa activa",
)
async def create_active_break(
    break_in: ActiveBreakCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    result = enterprise_controller.create_active_break(db, break_in=break_in)
    await cache_delete_pattern("active_breaks:*")
    return result


@router.get(
    "/active-breaks",
    response_model=list[ActiveBreakResponse],
    summary="Listar pausas activas",
)
async def list_active_breaks(
    duration: Optional[int] = Query(None, description="Filtrar por duración: 10, 20 o 30"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    cache_key = make_key("active_breaks", duration, category, skip, limit)
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached
    result = enterprise_controller.list_active_breaks(
        db, duration=duration, category=category, skip=skip, limit=limit
    )
    serialized = [r.model_dump() for r in result]
    await cache_set(cache_key, serialized, ttl=600)
    return result


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
    return enterprise_controller.get_active_break(db, break_id=break_id)


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
    return enterprise_controller.complete_break(
        db, log_id=log_id, current_user=current_user
    )


@router.get(
    "/my-stats",
    response_model=ActiveBreakStatsResponse,
    summary="Mis estadísticas de pausas activas",
)
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return enterprise_controller.get_my_stats(
        db, current_user=current_user
    )
