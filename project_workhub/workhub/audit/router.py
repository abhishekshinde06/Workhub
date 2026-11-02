from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from workhub.auth.setting.auth_setting import require_role
from workhub.db_connection import get_db
from workhub.audit import service

router = APIRouter(tags=["Audit Logs"])


@router.get("/audit-logs")
def list_audit_logs(
    action: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin", "superadmin")),
):
    """
    'View audit logs' feature from SRS Module 10.

    Restricted to admin/superadmin via the require_role dependency, since an
    audit trail (who did what, and when) is sensitive information that
    regular employees/managers shouldn't be able to browse.
    """
    return service.service_list_audit_logs(db, action, skip, limit)
