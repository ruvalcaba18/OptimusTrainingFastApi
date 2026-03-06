"""
Enterprise controller — handles HTTP-level logic and calls the service.
No direct database queries here; that's the service's job.
"""
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.enterprise_service import enterprise_service
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


class EnterpriseController:

    # ━━━━━━━━━━━━━━━━━━━━━  Enterprise CRUD  ━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def create_enterprise(
        db: Session, enterprise_in: EnterpriseCreate
    ) -> EnterpriseResponse:
        try:
            enterprise = enterprise_service.create_enterprise(db, enterprise_in)
            db.commit()
            return enterprise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la empresa: {str(e)}",
            )

    @staticmethod
    def get_enterprise(db: Session, enterprise_id: int) -> EnterpriseResponse:
        enterprise = enterprise_service.get_enterprise_by_id(db, enterprise_id)
        if not enterprise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa no encontrada",
            )
        return enterprise

    # ━━━━━━━━━━━━━━━━━━━━━━  Code validation  ━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def validate_code(
        db: Session, code_in: ValidateCodeRequest, current_user: User
    ) -> ValidateCodeResponse:
        """
        Valida un código de empresa:
        1. Buscar el código
        2. Verificar que no esté usado
        3. Verificar que no esté expirado
        4. Marcar como usado y vincular al usuario
        5. Crear membresía
        """
        db_code = enterprise_service.get_code_by_value(db, code_in.code)

        if not db_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código inválido.",
            )

        if db_code.is_used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este código ya fue utilizado.",
            )

        if db_code.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este código ha expirado.",
            )

        # Verificar si el usuario ya es miembro de esta empresa
        existing = enterprise_service.get_membership(
            db, user_id=current_user.id, enterprise_id=db_code.enterprise_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya estás vinculado a esta empresa.",
            )

        try:
            # Marcar código como usado
            enterprise_service.redeem_code(db, db_code, user_id=current_user.id)

            # Crear membresía
            enterprise_service.create_membership(
                db, enterprise_id=db_code.enterprise_id, user_id=current_user.id
            )

            enterprise = enterprise_service.get_enterprise_by_id(
                db, db_code.enterprise_id
            )

            db.commit()
            return ValidateCodeResponse(
                message=f"Vinculado exitosamente a {enterprise.name}",
                enterprise=EnterpriseResponse.model_validate(enterprise),
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al validar código: {str(e)}",
            )

    # ━━━━━━━━━━━━━━━━━━━━━━  Code generation  ━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def generate_codes(
        db: Session, code_req: CodeGenerateRequest
    ) -> list[EnterpriseCodeResponse]:
        enterprise = enterprise_service.get_enterprise_by_id(db, code_req.enterprise_id)
        if not enterprise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa no encontrada",
            )

        try:
            codes = enterprise_service.generate_codes(
                db,
                enterprise_id=code_req.enterprise_id,
                quantity=code_req.quantity,
                expire_in_days=code_req.expire_in_days,
            )
            db.commit()
            return codes
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al generar códigos: {str(e)}",
            )

    @staticmethod
    def list_codes(
        db: Session, enterprise_id: int, skip: int = 0, limit: int = 100
    ) -> list[EnterpriseCodeResponse]:
        enterprise = enterprise_service.get_enterprise_by_id(db, enterprise_id)
        if not enterprise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa no encontrada",
            )
        return enterprise_service.get_codes_by_enterprise(
            db, enterprise_id=enterprise_id, skip=skip, limit=limit
        )

    # ━━━━━━━━━━━━━━━━━━━━━━━━  My Enterprise  ━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def get_my_enterprise(
        db: Session, current_user: User
    ) -> EnterpriseResponse:
        memberships = enterprise_service.get_user_memberships(db, user_id=current_user.id)
        if not memberships:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No estás vinculado a ninguna empresa. Valida tu código primero.",
            )
        # Retornar la empresa de la primera membresía activa
        enterprise = enterprise_service.get_enterprise_by_id(
            db, memberships[0].enterprise_id
        )
        return enterprise

    @staticmethod
    def list_members(
        db: Session, enterprise_id: int, skip: int = 0, limit: int = 100
    ) -> list[EnterpriseMemberResponse]:
        enterprise = enterprise_service.get_enterprise_by_id(db, enterprise_id)
        if not enterprise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa no encontrada",
            )
        return enterprise_service.get_enterprise_members(
            db, enterprise_id=enterprise_id, skip=skip, limit=limit
        )

    # ━━━━━━━━━━━━━━━━━━━━━  Active Breaks  ━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def create_active_break(
        db: Session, break_in: ActiveBreakCreate
    ) -> ActiveBreakResponse:
        try:
            active_break = enterprise_service.create_active_break(db, break_in)
            db.commit()
            return active_break
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear pausa activa: {str(e)}",
            )

    @staticmethod
    def list_active_breaks(
        db: Session,
        duration: Optional[int] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[ActiveBreakResponse]:
        return enterprise_service.get_active_breaks(
            db, duration=duration, category=category, skip=skip, limit=limit
        )

    @staticmethod
    def get_active_break(db: Session, break_id: int) -> ActiveBreakResponse:
        active_break = enterprise_service.get_active_break_by_id(db, break_id)
        if not active_break:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pausa activa no encontrada",
            )
        return active_break

    @staticmethod
    def start_break(
        db: Session, log_in: ActiveBreakLogCreate, current_user: User
    ) -> ActiveBreakLogResponse:
        active_break = enterprise_service.get_active_break_by_id(db, log_in.session_id)
        if not active_break:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pausa activa no encontrada",
            )

        # Buscar la empresa del usuario (si tiene)
        memberships = enterprise_service.get_user_memberships(db, user_id=current_user.id)
        enterprise_id = memberships[0].enterprise_id if memberships else None

        try:
            log = enterprise_service.start_break_log(
                db,
                session_id=log_in.session_id,
                user_id=current_user.id,
                enterprise_id=enterprise_id,
            )
            db.commit()
            return log
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al iniciar pausa: {str(e)}",
            )

    @staticmethod
    def complete_break(
        db: Session, log_id: int, current_user: User
    ) -> ActiveBreakLogResponse:
        log = enterprise_service.get_break_log_by_id(
            db, log_id=log_id, user_id=current_user.id
        )
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de pausa no encontrado",
            )
        if log.completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta pausa ya fue completada",
            )

        try:
            completed_log = enterprise_service.complete_break_log(db, log)
            db.commit()
            return completed_log
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al completar pausa: {str(e)}",
            )

    @staticmethod
    def get_my_stats(
        db: Session, current_user: User
    ) -> ActiveBreakStatsResponse:
        stats = enterprise_service.get_user_break_stats(db, user_id=current_user.id)
        return ActiveBreakStatsResponse(**stats)


enterprise_controller = EnterpriseController()
