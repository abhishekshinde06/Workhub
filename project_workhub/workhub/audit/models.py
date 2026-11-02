from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from workhub.db_connection import Base


class AuditLog(Base):
    """
    Audit log table for SRS Module 10.

    The SRS asks the system to keep logs for important activities such as
    login/logout, user creation, project creation, task updates, and
    document upload/deletion. Rather than a separate table per feature,
    everything goes into this one generic table:

    - action:   short machine-readable name, e.g. "user_login",
                "project_created", "task_status_changed".
    - user_id:  who performed the action (nullable, e.g. a failed login
                attempt for a username that doesn't exist has no user_id).
    - username: kept alongside user_id so the log still reads clearly even
                if the user account is later deleted.
    - detail:   free-text extra context, e.g. "project_id=3".
    - created_at: when the action happened, set automatically by the DB.
    """

    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    action = Column(String, nullable=False, index=True)
    # ondelete="CASCADE" tells the *database* to auto-delete this row when
    # the referenced user is deleted -- this works even for a raw SQL
    # DELETE FROM users, not just deletes done through SQLAlchemy.
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True)
    username = Column(String, nullable=True)
    detail = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
