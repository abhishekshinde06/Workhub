from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from workhub.search import service

router = APIRouter(tags=["Search"])


@router.get("/search")
def global_search(
    keyword: str,
    limit_per_type: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """
    'Search' feature from SRS Module 8 -- searches projects, tasks, users
    and documents in one call. Example: GET /search?keyword=login
    """
    return service.service_global_search(db, keyword, limit_per_type)
