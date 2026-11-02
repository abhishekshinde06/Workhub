from fastapi import HTTPException, status
from workhub.projects.models import Project
from sqlalchemy.orm import Session
from workhub.audit.service import record_audit_log


def get_project(project_id: int, db: Session) -> Project:
    """
    Look up a single project by id, or raise 404.

    Kept as its own helper (mirroring get_user in the admin/auth modules)
    so update/delete/view-single can all reuse the same not-found check
    instead of repeating the query + HTTPException everywhere.
    """
    project_data = db.query(Project).filter(Project.project_id == project_id).first()
    if not project_data :
        raise HTTPException(detail="Project not found", status_code=status.HTTP_404_NOT_FOUND)
    return project_data


def service_create_project(request, db: Session, current_user: dict):
    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(
            detail="Only admin and manager can add new projects", status_code=400
        )

    project_data = Project(
        project_name=request.project_name,
        description=request.description,
        manager_id=current_user["user_id"],
    )
    try:
        db.add(project_data)
        db.commit()
        db.refresh(project_data)
        record_audit_log(
            db,
            "project_created",
            user_id=current_user["user_id"],
            username=current_user.get("username"),
            detail=f"project_id={project_data.project_id}",
        )
        return {"message": "Project was successfully added"}
    except Exception as e:
        print(e)
        raise HTTPException(
            detail="project was not added", status_code=status.HTTP_400_BAD_REQUEST
        )


def service_show_project(db: Session):
    project_data = db.query(Project).all()
    if project_data:
        return project_data
    return {"message": "project not found"}


def service_get_project(project_id: int, db: Session):
    """'View Project' feature from SRS Module 4."""
    return get_project(project_id, db)


def service_list_projects(db: Session, skip: int = 0, limit: int = 20):
    """'List Projects' feature from SRS Module 4, with basic pagination."""
    return db.query(Project).offset(skip).limit(limit).all()


def service_search_projects(db: Session, keyword: str, skip: int = 0, limit: int = 20):
    """
    'Search Projects' feature from SRS Module 4 / Module 8.

    Does a case-insensitive match on project_name and description, since
    those are the two fields a user is realistically searching by.
    """
    like_pattern = f"%{keyword}%"
    return (
        db.query(Project)
        .filter(
            (Project.project_name.ilike(like_pattern))
            | (Project.description.ilike(like_pattern))
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def service_update_project(project_id: int, request, db: Session, current_user: dict):
    """
    'Update Project' feature from SRS Module 4.

    Only the project's manager or an admin may update it, mirroring the
    "only admin and manager can add new projects" rule already used in
    service_create_project.
    """
    project_data = get_project(project_id, db)
    if current_user["role"] != "admin" and project_data.manager_id != current_user["user_id"]:
        raise HTTPException(
            detail="Only the project's manager or an admin can update this project",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    update_data = request.model_dump(exclude_unset=True)
    try:
        for field, value in update_data.items():
            setattr(project_data, field, value)
        db.commit()
        db.refresh(project_data)
        return {"message": "Project updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(detail=f"Project was not updated: {str(e)}", status_code=400)


def service_delete_project(project_id: int, db: Session, current_user: dict):
    """
    'Delete Project' feature from SRS Module 4.

    Same manager-or-admin rule as update, so a random logged-in user can't
    delete someone else's project.
    """
    project_data = get_project(project_id, db)
    if current_user["role"] != "admin" and project_data.manager_id != current_user["user_id"]:
        raise HTTPException(
            detail="Only the project's manager or an admin can delete this project",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    db.delete(project_data)
    db.commit()
    return {"message": "Project deleted successfully"}
