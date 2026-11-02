from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from workhub.db_connection import Base


class Comment(Base):
    """
    Comment table for SRS Module 6.

    The SRS leaves "association with appropriate system entities" up to the
    developer. Kept simple here: a comment is attached to one entity, named
    generically by `entity_type` ("project" or "task") + `entity_id`, rather
    than adding a separate comments table per entity type. This keeps the
    Comments module reusable if more commentable entities are added later
    (documents, etc.) without another migration.

    - entity_type: "project" or "task" for now.
    - entity_id:   the project_id or task_id being commented on.
    - author_id:   the user who wrote the comment.
    - content:     the comment text itself.
    """

    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entity_type = Column(String, nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
