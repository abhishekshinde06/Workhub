from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from workhub.dashboard import service

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Dashboard statistics' feature from SRS Module 9."""
    return service.service_get_dashboard_stats(db)
