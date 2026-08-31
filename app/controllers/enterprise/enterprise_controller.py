from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.controllers.enterprise.exceptions import (
    ActiveBreakNotFoundError,
    AlreadyLinkedEnterpriseError,
    BreakAlreadyCompletedError,
    EnterpriseCodeAlreadyUsedError,
    EnterpriseCodeExpiredError,
    EnterpriseNotFoundError,
    InvalidEnterpriseCodeError,
)
from app.core.error_handlers import handle_controller_errors
from app.models import User
from app.schemas.enterprise import (
    ActiveBreakCreate,
    ActiveBreakLogCreate,
    ActiveBreakLogResponse,
    ActiveBreakResponse,
    ActiveBreakStatsResponse,
    CodeGenerateRequest,
    EnterpriseCodeResponse,
    EnterpriseCreate,
    EnterpriseMemberResponse,
    EnterpriseResponse,
    ValidateCodeRequest,
    ValidateCodeResponse,
)
from app.services import enterprise_service


class EnterpriseController:

    @staticmethod
    @handle_controller_errors
    def create_enterprise(
        db: Session, enterprise_in: EnterpriseCreate
    ) -> EnterpriseResponse:
        enterprise = enterprise_service.create_enterprise(db, enterprise_in)
        db.commit()
        return enterprise

    @staticmethod
    @handle_controller_errors
    def get_enterprise(db: Session, enterprise_id: int) -> EnterpriseResponse:
        enterprise = enterprise_service.get_enterprise_by_id(db, enterprise_id)
        if not enterprise:
            raise EnterpriseNotFoundError()
        return enterprise

    @staticmethod
    @handle_controller_errors
    def validate_code(
        db: Session, code_in: ValidateCodeRequest, current_user: User
    ) -> ValidateCodeResponse:
        db_code = enterprise_service.get_code_by_value(db, code_in.code)

        if not db_code:
            raise InvalidEnterpriseCodeError()

        if db_code.is_used:
            raise EnterpriseCodeAlreadyUsedError()

        if db_code.expires_at < datetime.now(timezone.utc):
            raise EnterpriseCodeExpiredError()

        existing = enterprise_service.get_membership(
            db, user_id=current_user.id, enterprise_id=db_code.enterprise_id
        )
        if existing:
            raise AlreadyLinkedEnterpriseError()

        enterprise_service.redeem_code(db, db_code, user_id=current_user.id)
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

    @staticmethod
    @handle_controller_errors
    def generate_codes(
        db: Session, code_req: CodeGenerateRequest
    ) -> list[EnterpriseCodeResponse]:
        enterprise = enterprise_service.get_enterprise_by_id(db, code_req.enterprise_id)
        if not enterprise:
            raise EnterpriseNotFoundError()

        codes = enterprise_service.generate_codes(
            db,
            enterprise_id=code_req.enterprise_id,
            quantity=code_req.quantity,
            expire_in_days=code_req.expire_in_days,
        )
        db.commit()
        return codes

    @staticmethod
    @handle_controller_errors
    def list_codes(
        db: Session, enterprise_id: int, skip: int = 0, limit: int = 100
    ) -> list[EnterpriseCodeResponse]:
        enterprise = enterprise_service.get_enterprise_by_id(db, enterprise_id)
        if not enterprise:
            raise EnterpriseNotFoundError()
        return enterprise_service.get_codes_by_enterprise(
            db, enterprise_id=enterprise_id, skip=skip, limit=limit
        )

    @staticmethod
    @handle_controller_errors
    def get_my_enterprise(
        db: Session, current_user: User
    ) -> EnterpriseResponse:
        memberships = enterprise_service.get_user_memberships(db, user_id=current_user.id)
        if not memberships:
            raise EnterpriseNotFoundError("No estás vinculado a ninguna empresa. Valida tu código primero.")
        enterprise = enterprise_service.get_enterprise_by_id(
            db, memberships[0].enterprise_id
        )
        return enterprise

    @staticmethod
    @handle_controller_errors
    def list_members(
        db: Session, enterprise_id: int, skip: int = 0, limit: int = 100
    ) -> list[EnterpriseMemberResponse]:
        enterprise = enterprise_service.get_enterprise_by_id(db, enterprise_id)
        if not enterprise:
            raise EnterpriseNotFoundError()
        return enterprise_service.get_enterprise_members(
            db, enterprise_id=enterprise_id, skip=skip, limit=limit
        )

    @staticmethod
    @handle_controller_errors
    def create_active_break(
        db: Session, break_in: ActiveBreakCreate
    ) -> ActiveBreakResponse:
        active_break = enterprise_service.create_active_break(db, break_in)
        db.commit()
        return active_break

    @staticmethod
    @handle_controller_errors
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
    @handle_controller_errors
    def get_active_break(db: Session, break_id: int) -> ActiveBreakResponse:
        active_break = enterprise_service.get_active_break_by_id(db, break_id)
        if not active_break:
            raise ActiveBreakNotFoundError()
        return active_break

    @staticmethod
    @handle_controller_errors
    def start_break(
        db: Session, log_in: ActiveBreakLogCreate, current_user: User
    ) -> ActiveBreakLogResponse:
        active_break = enterprise_service.get_active_break_by_id(db, log_in.session_id)
        if not active_break:
            raise ActiveBreakNotFoundError()

        memberships = enterprise_service.get_user_memberships(db, user_id=current_user.id)
        enterprise_id = memberships[0].enterprise_id if memberships else None

        log = enterprise_service.start_break_log(
            db,
            session_id=log_in.session_id,
            user_id=current_user.id,
            enterprise_id=enterprise_id,
        )
        db.commit()
        return log

    @staticmethod
    @handle_controller_errors
    def complete_break(
        db: Session, log_id: int, current_user: User
    ) -> ActiveBreakLogResponse:
        log = enterprise_service.get_break_log_by_id(
            db, log_id=log_id, user_id=current_user.id
        )
        if not log:
            raise ActiveBreakNotFoundError("Registro de pausa no encontrado")
        if log.completed:
            raise BreakAlreadyCompletedError()

        completed_log = enterprise_service.complete_break_log(db, log)
        db.commit()
        return completed_log

    @staticmethod
    @handle_controller_errors
    def get_my_stats(
        db: Session, current_user: User
    ) -> ActiveBreakStatsResponse:
        stats = enterprise_service.get_user_break_stats(db, user_id=current_user.id)
        return ActiveBreakStatsResponse(**stats)


enterprise_controller = EnterpriseController()
