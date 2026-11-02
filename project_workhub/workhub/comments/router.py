from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from workhub.comments import schema, service

router = APIRouter(tags=["Comments"])


@router.post("/comment")
def add_comment(
    request: schema.CreateComment,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Add Comment' feature from SRS Module 6."""
    return service.service_add_comment(request, db, current_user)


@router.get("/comments/{entity_type}/{entity_id}")
def view_comments(
    entity_type: schema.CommentEntityType,
    entity_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'View Comments' feature from SRS Module 6 -- e.g. GET /comments/task/5"""
    return service.service_view_comments(entity_type, entity_id, db, skip, limit)


@router.put("/comment/{comment_id}")
def update_comment(
    comment_id: int,
    request: schema.UpdateComment,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Update Comment' feature from SRS Module 6."""
    return service.service_update_comment(comment_id, request, db, current_user)


@router.delete("/comment/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Delete Comment' feature from SRS Module 6."""
    return service.service_delete_comment(comment_id, db, current_user)
