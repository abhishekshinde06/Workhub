from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from workhub.comments.models import Comment
from workhub.comments.schema import CreateComment, UpdateComment
from workhub.projects.models import Project
from workhub.task.models import Task


def _check_entity_exists(entity_type: str, entity_id: int, db: Session) -> None:
    """
    Make sure the project/task a comment points to actually exists, so we
    don't end up with comments attached to nothing.
    """
    if entity_type == "project":
        exists = db.query(Project).filter(Project.project_id == entity_id).first()
    else:
        exists = db.query(Task).filter(Task.task_id == entity_id).first()
    if not exists:
        raise HTTPException(
            detail=f"{entity_type} with id {entity_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )


def get_comment(comment_id: int, db: Session) -> Comment:
    """Look up a single comment by id, or raise 404."""
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(detail="Comment not found", status_code=status.HTTP_404_NOT_FOUND)
    return comment


def service_add_comment(request: CreateComment, db: Session, current_user: dict):
    """'Add Comment' feature from SRS Module 6."""
    _check_entity_exists(request.entity_type, request.entity_id, db)
    comment = Comment(
        entity_type=request.entity_type,
        entity_id=request.entity_id,
        author_id=current_user["user_id"],
        content=request.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {"message": "Comment added successfully", "comment_id": comment.comment_id}


def service_view_comments(entity_type: str, entity_id: int, db: Session, skip: int = 0, limit: int = 50):
    """'View Comments' feature from SRS Module 6, with basic pagination."""
    return (
        db.query(Comment)
        .filter(Comment.entity_type == entity_type, Comment.entity_id == entity_id)
        .order_by(Comment.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def service_update_comment(comment_id: int, request: UpdateComment, db: Session, current_user: dict):
    """
    'Update Comment' feature from SRS Module 6.

    Only the comment's own author (or an admin) may edit it.
    """
    comment = get_comment(comment_id, db)
    if current_user["role"] != "admin" and comment.author_id != current_user["user_id"]:
        raise HTTPException(
            detail="Only the comment's author or an admin can edit this comment",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    comment.content = request.content
    db.commit()
    db.refresh(comment)
    return {"message": "Comment updated successfully"}


def service_delete_comment(comment_id: int, db: Session, current_user: dict):
    """
    'Delete Comment' feature from SRS Module 6.

    Same author-or-admin rule as update.
    """
    comment = get_comment(comment_id, db)
    if current_user["role"] != "admin" and comment.author_id != current_user["user_id"]:
        raise HTTPException(
            detail="Only the comment's author or an admin can delete this comment",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}
