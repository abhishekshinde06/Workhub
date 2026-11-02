import logging

from sqlalchemy.orm import Session

from workhub.audit.models import AuditLog

logger = logging.getLogger("workhub.audit")


async def record_audit_log(
    db: Session,
    action: str,
    user_id: int | None = None,
    username: str | None = None,
    detail: str | None = None,
) -> None:
    """
    Write one row to the audit_log table (SRS Module 10).

    This is intentionally "fire and forget": if writing the audit row fails
    for any reason, we log it and move on instead of raising, because an
    audit-log failure should never block the real action (e.g. a user login
    must still succeed even if the audit insert has a problem).

    Args:
        db: database session (the same session the caller is already using).
        action: short machine-readable event name, e.g. "user_login".
        user_id: id of the user who performed the action, if known.
        username: username of the user who performed the action, if known.
        detail: any extra free-text context worth keeping.
    """
    try:
        log_row = AuditLog(action=action, user_id=user_id, username=username, detail=detail)
        db.add(log_row)
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.warning("Failed to write audit log for action=%s: %s", action, e)


def service_list_audit_logs(db: Session, action: str | None = None, skip: int = 0, limit: int = 50):
    """
    'View audit logs' -- lets an admin/superadmin browse the audit trail.

    Args:
        db: database session.
        action: optional exact-match filter on the action name.
        skip: pagination offset.
        limit: pagination page size.

    Returns:
        list of AuditLog rows, newest first.
    """
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action)
    return query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
