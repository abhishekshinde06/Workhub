from sqlalchemy.orm import Session

from workhub.auth.models import User
from workhub.documents.models import Document
from workhub.projects.models import Project
from workhub.task.models import Task


def service_global_search(db: Session, keyword: str, limit_per_type: int = 10):
    """
    'Search' feature from SRS Module 8: one endpoint that searches across
    Projects, Tasks, Users and Documents at once, the way a top-level search
    bar in the app would use it.

    Each entity already has its own dedicated search endpoint too
    (/project/search, /tasks/search, /documents/search) for when a caller
    wants to search just one kind of thing with more filters -- this one is
    for the "search everything" case.

    Args:
        db: database session.
        keyword: text to search for (case-insensitive).
        limit_per_type: max results to return per entity type, so one very
            common keyword doesn't return an unbounded response.

    Returns:
        dict with one list per entity type: projects, tasks, users, documents.
    """
    like_pattern = f"%{keyword}%"

    projects = (
        db.query(Project)
        .filter(
            (Project.project_name.ilike(like_pattern)) | (Project.description.ilike(like_pattern))
        )
        .limit(limit_per_type)
        .all()
    )

    tasks = (
        db.query(Task)
        .filter((Task.title.ilike(like_pattern)) | (Task.description.ilike(like_pattern)))
        .limit(limit_per_type)
        .all()
    )

    users = (
        db.query(User)
        .filter((User.name.ilike(like_pattern)) | (User.username.ilike(like_pattern)))
        .limit(limit_per_type)
        .all()
    )

    documents = (
        db.query(Document)
        .filter(Document.original_filename.ilike(like_pattern))
        .limit(limit_per_type)
        .all()
    )

    return {
        "projects": projects,
        "tasks": tasks,
        "users": users,
        "documents": documents,
    }
