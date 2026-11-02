from typing import Optional
from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from workhub.task.models import Task
from workhub.db_connection import get_db
from workhub.auth.setting.auth_setting import verify_token
from workhub.task import schema, service
router = APIRouter(tags=["Tasks"])
@router.post("/task")
def create_task(request : schema.CreateTask, db : Session = Depends(get_db),current_user = Depends(verify_token)) : 
    return service.service_create_task(request,db,current_user)
@router.patch("/task/{task_id}")
def assigned_task(task_id : int, id : int, db : Session = Depends(get_db)) :
    return service.service_assign_developer(task_id,id,db)
@router.patch('/task_update/{task_id}') 
def update_task_detail(task_id : int,request :schema.UpdateTask,db :Session = Depends(get_db)) : 
    return service.service_update_task(task_id,request,db)

@router.get('/see_task/{task_id}')
def get_task_data(task_id : int,db :Session = Depends(get_db)) :
    return service.check_task(task_id,db)


@router.delete("/task/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Delete Task' feature from SRS Module 5."""
    return service.service_delete_task(task_id, db)


@router.patch("/task/{task_id}/status")
def change_task_status(
    task_id: int,
    request: schema.UpdateTaskStatus,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Change Status' feature from SRS Module 5."""
    return service.service_change_status(task_id, request, db, current_user)


@router.get("/tasks")
def list_tasks(
    project_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'List Task' / 'View Task' feature from SRS Module 5, with pagination."""
    return service.service_list_tasks(db, project_id, skip, limit)


@router.get("/tasks/search")
def search_tasks(
    keyword: Optional[str] = None,
    status: Optional[schema.TaskStatus] = None,
    priority: Optional[schema.TaskPriority] = None,
    assigned_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Search Tasks' feature from SRS Module 5 / Module 8."""
    return service.service_search_tasks(
        db, keyword, status, priority, assigned_id, skip, limit
    )
