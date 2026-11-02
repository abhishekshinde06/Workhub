from sqlalchemy.orm import Session

from workhub.auth.models import User
from workhub.documents.models import Document
from workhub.projects.models import Project
from workhub.task.models import Task


def service_get_dashboard_stats(db: Session):
    """
    'Dashboard statistics' feature from SRS Module 9.

    The SRS lists these exact numbers as the "possible information" to
    show, so that list is used directly here rather than inventing extra
    metrics: Total Users, Total Projects, Total Tasks, Completed Tasks,
    Pending Tasks, Uploaded Documents.

    "Completed" is read as Task.status == "done" and "Pending" as anything
    else, matching the TaskStatus enum in workhub/task/schema.py.

    Args:
        db: database session.

    Returns:
        dict with the six counts described above.
    """
    total_users = db.query(User).count()
    total_projects = db.query(Project).count()
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "done").count()
    pending_tasks = total_tasks - completed_tasks
    uploaded_documents = db.query(Document).count()

    return {
        "total_users": total_users,
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "uploaded_documents": uploaded_documents,
    }
