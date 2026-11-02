from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from workhub.projects.schema import CreateProjectSchema, UpdateProjectSchema
from workhub.projects import service

router = APIRouter(tags = ['Projects'])

@router.post('/project')
def create_project(request : CreateProjectSchema, db : Session = Depends(get_db),current_user : dict = Depends(verify_token)) :
   return service.service_create_project(request, db,current_user)

@router.get('/project')
def show_project(db : Session = Depends(get_db)):
   return service.service_show_project(db)


@router.get('/project/search')
def search_project(keyword: str, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """'Search Projects' feature from SRS Module 4."""
    return service.service_search_projects(db, keyword, skip, limit)


@router.get('/project/{project_id}')
def get_project(project_id: int, db: Session = Depends(get_db)):
    """'View Project' feature from SRS Module 4."""
    return service.service_get_project(project_id, db)


@router.put('/project/{project_id}')
def update_project(
    project_id: int,
    request: UpdateProjectSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Update Project' feature from SRS Module 4."""
    return service.service_update_project(project_id, request, db, current_user)


@router.delete('/project/{project_id}')
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Delete Project' feature from SRS Module 4."""
    return service.service_delete_project(project_id, db, current_user)
