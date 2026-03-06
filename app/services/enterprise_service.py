"""
Enterprise service — data-access layer.
No HTTP logic here; that belongs in the controller.
"""
import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from app.models.enterprise import Enterprise, EnterpriseCode, EnterpriseMember
from app.models.active_break import ActiveBreakSession, ActiveBreakLog
from app.schemas.enterprise import (
    EnterpriseCreate,
    ActiveBreakCreate,
    ActiveBreakUpdate,
)


class EnterpriseService:

    # ━━━━━━━━━━━━━━━━━━━━━━  Enterprise CRUD  ━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def create_enterprise(db: Session, enterprise_in: EnterpriseCreate) -> Enterprise:
        db_enterprise = Enterprise(
            name=enterprise_in.name,
            description=enterprise_in.description,
            contact_email=enterprise_in.contact_email,
        )
        db.add(db_enterprise)
        db.flush()
        db.refresh(db_enterprise)
        return db_enterprise

    @staticmethod
    def get_enterprise_by_id(db: Session, enterprise_id: int) -> Optional[Enterprise]:
        return db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()

    @staticmethod
    def get_all_enterprises(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[Enterprise]:
        return db.query(Enterprise).offset(skip).limit(limit).all()

    # ━━━━━━━━━━━━━━━━━━━━━━  Code generation  ━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def _generate_unique_code(length: int = 8) -> str:
        """Genera un código alfanumérico en mayúsculas (ej: A3K9-M2X7)."""
        chars = string.ascii_uppercase + string.digits
        raw = "".join(secrets.choice(chars) for _ in range(length))
        # Formato XXXX-XXXX para legibilidad
        return f"{raw[:4]}-{raw[4:]}"

    @staticmethod
    def generate_codes(
        db: Session,
        enterprise_id: int,
        quantity: int,
        expire_in_days: int = 7,
    ) -> List[EnterpriseCode]:
        """Genera N códigos únicos para una empresa con fecha de expiración."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=expire_in_days)
        codes: List[EnterpriseCode] = []

        for _ in range(quantity):
            # Reintentar si hay colisión (muy improbable)
            for _attempt in range(5):
                code_str = EnterpriseService._generate_unique_code()
                exists = (
                    db.query(EnterpriseCode)
                    .filter(EnterpriseCode.code == code_str)
                    .first()
                )
                if not exists:
                    break
            else:
                # Si tras 5 intentos no se pudo, usar uno más largo
                code_str = EnterpriseService._generate_unique_code(length=12)

            db_code = EnterpriseCode(
                enterprise_id=enterprise_id,
                code=code_str,
                expires_at=expires_at,
            )
            db.add(db_code)
            codes.append(db_code)

        db.flush()
        for c in codes:
            db.refresh(c)
        return codes

    @staticmethod
    def get_code_by_value(db: Session, code: str) -> Optional[EnterpriseCode]:
        """ACID: row-level lock para evitar redención concurrente del mismo código."""
        return (
            db.query(EnterpriseCode)
            .filter(EnterpriseCode.code == code.upper().strip())
            .with_for_update()
            .first()
        )

    @staticmethod
    def get_codes_by_enterprise(
        db: Session, enterprise_id: int, skip: int = 0, limit: int = 100
    ) -> List[EnterpriseCode]:
        return (
            db.query(EnterpriseCode)
            .filter(EnterpriseCode.enterprise_id == enterprise_id)
            .order_by(EnterpriseCode.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def redeem_code(
        db: Session, db_code: EnterpriseCode, user_id: int
    ) -> EnterpriseCode:
        """Marca el código como usado y registra quién lo canjeó."""
        db_code.is_used = True
        db_code.used_by_user_id = user_id
        db_code.used_at = datetime.now(timezone.utc)
        db.add(db_code)
        db.flush()
        db.refresh(db_code)
        return db_code

    # ━━━━━━━━━━━━━━━━━━━━━━━━  Membership  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def get_membership(
        db: Session, user_id: int, enterprise_id: int
    ) -> Optional[EnterpriseMember]:
        return (
            db.query(EnterpriseMember)
            .filter(
                EnterpriseMember.user_id == user_id,
                EnterpriseMember.enterprise_id == enterprise_id,
            )
            .first()
        )

    @staticmethod
    def get_user_memberships(
        db: Session, user_id: int
    ) -> List[EnterpriseMember]:
        return (
            db.query(EnterpriseMember)
            .filter(EnterpriseMember.user_id == user_id, EnterpriseMember.is_active == True)
            .all()
        )

    @staticmethod
    def create_membership(
        db: Session, enterprise_id: int, user_id: int
    ) -> EnterpriseMember:
        member = EnterpriseMember(
            enterprise_id=enterprise_id,
            user_id=user_id,
        )
        db.add(member)
        db.flush()
        db.refresh(member)
        return member

    @staticmethod
    def get_enterprise_members(
        db: Session, enterprise_id: int, skip: int = 0, limit: int = 100
    ) -> List[EnterpriseMember]:
        return (
            db.query(EnterpriseMember)
            .filter(
                EnterpriseMember.enterprise_id == enterprise_id,
                EnterpriseMember.is_active == True,
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ━━━━━━━━━━━━━━━━━━━━━  Active Break Sessions  ━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def create_active_break(
        db: Session, break_in: ActiveBreakCreate
    ) -> ActiveBreakSession:
        db_break = ActiveBreakSession(
            title=break_in.title,
            description=break_in.description,
            category=break_in.category.value,
            duration_minutes=break_in.duration_minutes.value,
            instructions=break_in.instructions,
            video_url=break_in.video_url,
            image_url=break_in.image_url,
        )
        db.add(db_break)
        db.flush()
        db.refresh(db_break)
        return db_break

    @staticmethod
    def get_active_break_by_id(
        db: Session, break_id: int
    ) -> Optional[ActiveBreakSession]:
        return (
            db.query(ActiveBreakSession)
            .filter(ActiveBreakSession.id == break_id, ActiveBreakSession.is_active == True)
            .first()
        )

    @staticmethod
    def get_active_breaks(
        db: Session,
        duration: Optional[int] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[ActiveBreakSession]:
        query = db.query(ActiveBreakSession).filter(ActiveBreakSession.is_active == True)
        if duration:
            query = query.filter(ActiveBreakSession.duration_minutes == duration)
        if category:
            query = query.filter(ActiveBreakSession.category == category)
        return query.order_by(ActiveBreakSession.created_at.desc()).offset(skip).limit(limit).all()

    # ━━━━━━━━━━━━━━━━━━━━━━  Active Break Logs  ━━━━━━━━━━━━━━━━━━━━━━━

    @staticmethod
    def start_break_log(
        db: Session,
        session_id: int,
        user_id: int,
        enterprise_id: Optional[int] = None,
    ) -> ActiveBreakLog:
        log = ActiveBreakLog(
            session_id=session_id,
            user_id=user_id,
            enterprise_id=enterprise_id,
        )
        db.add(log)
        db.flush()
        db.refresh(log)
        return log

    @staticmethod
    def complete_break_log(db: Session, log: ActiveBreakLog) -> ActiveBreakLog:
        log.completed = True
        log.completed_at = datetime.now(timezone.utc)
        db.add(log)
        db.flush()
        db.refresh(log)
        return log

    @staticmethod
    def get_break_log_by_id(
        db: Session, log_id: int, user_id: int
    ) -> Optional[ActiveBreakLog]:
        return (
            db.query(ActiveBreakLog)
            .filter(ActiveBreakLog.id == log_id, ActiveBreakLog.user_id == user_id)
            .first()
        )

    @staticmethod
    def get_user_break_stats(db: Session, user_id: int) -> dict:
        """Calcula estadísticas de pausas activas para un usuario."""
        logs = (
            db.query(ActiveBreakLog)
            .filter(ActiveBreakLog.user_id == user_id)
            .all()
        )

        total_started = len(logs)
        total_completed = sum(1 for l in logs if l.completed)

        # Calcular minutos totales (solo completadas)
        total_minutes = 0
        by_category: dict[str, int] = {}

        for log in logs:
            if log.completed:
                session = log.session
                if session:
                    total_minutes += session.duration_minutes
                    cat = session.category
                    by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_sessions_started": total_started,
            "total_sessions_completed": total_completed,
            "total_minutes": total_minutes,
            "sessions_by_category": by_category,
        }


enterprise_service = EnterpriseService()
