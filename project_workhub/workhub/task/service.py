from sqlalchemy.orm import Session
from fastapi import HTTPException
from workhub.auth.models import User
from workhub.task.models import Task
from workhub.task.schema import CreateTask, UpdateTaskStatus
from workhub.audit.service import record_audit_log


def check_task(task_id : int,db : Session) : 
    task_detail = db.query(Task).filter(Task.task_id == task_id).first()
    if not task_detail :
        raise HTTPException(detail = "Invalid task id ", status_code = 404)
    return task_detail

def service_create_task(request : str,db,current_user):
    task_data = Task(
        title=request.title,
        description=request.description,
        assigned_id=request.assigned_id,
        project_id=request.project_id,
        priority=request.priority,
        due_date=request.due_date,
        manager_id = current_user["user_id"]
    )
    try :
        db.add(task_data)
        db.commit()
        return {"message" : f"task {request.title} was added successfully"}
    except Exception as e :
        print(e)
        return {"message" : "task was not added"}
    
def service_assign_developer(task_id : int,user_id : int, db : Session) : 
    # bug fix: this used to call the local variable `task_detail` as if it
    # were the `check_task` function, which raised an UnboundLocalError.
    task_detail = check_task(task_id,db)
    user_data  = db.query(User).filter(User.user_id == user_id).first()
    if not user_data : 
        raise HTTPException(detail = "developer not exist in company",status_code = 404)
    task_detail.assigned_id = id
    db.commit()
    db.refresh(task_detail)
    return {"message" : "task was aggigned successfully"}




def service_update_task(task_id : int,request : str,db : Session) :
    task_data = check_task(task_id, db)
    try : 
        change_task_data = request.model_dump(exclude_unset = True)
        for field,value in change_task_data.items() : 
            setattr(task_data,field,value)
        db.commit()
        db.refresh(task_data)
        return {"message" : "task detail updated"}  
    except Exception as e : 
        print(e)
        raise HTTPException(status_code=501,detail = "task detail was not updated yet")


def service_delete_task(task_id: int, db: Session):
    """
    'Delete Task' feature from SRS Module 5 (this was listed in the spec
    but had no implementation yet).

    Args:
        task_id: id of the task to remove.
        db: database session.

    Returns:
        dict confirming deletion.
    """
    task_data = check_task(task_id, db)
    db.delete(task_data)
    db.commit()
    return {"message": "task deleted successfully"}


def service_change_status(task_id: int, request: UpdateTaskStatus, db: Session, current_user: dict | None = None):
    """
    'Change Status' feature from SRS Module 5.

    Kept separate from service_update_task so that changing a task's status
    (the thing that happens most often, e.g. moving a task on a board) does
    not need to go through the general update endpoint.

    Args:
        task_id: id of the task to change.
        request: UpdateTaskStatus schema, holding the new status value.
        db: database session.
        current_user: decoded token dict of whoever made the change, used
            only for the audit log entry.

    Returns:
        dict confirming the status change.
    """
    task_data = check_task(task_id, db)
    task_data.status = request.status.value
    db.commit()
    db.refresh(task_data)
    record_audit_log(
        db,
        "task_status_changed",
        user_id=current_user.get("user_id") if current_user else None,
        username=current_user.get("username") if current_user else None,
        detail=f"task_id={task_id} -> {request.status.value}",
    )
    return {"message": f"task status changed to {request.status.value}"}


def service_list_tasks(db: Session, project_id: int | None = None, skip: int = 0, limit: int = 20):
    """
    List Task / Search Task features from SRS Module 5.

    Supports plain pagination (skip/limit) and an optional project_id filter,
    since most of the time a caller wants "tasks of this project" rather
    than every task in the whole system.

    Args:
        db: database session.
        project_id: optional project id to filter tasks by.
        skip: how many rows to skip (pagination offset).
        limit: max rows to return (pagination page size).

    Returns:
        list of Task rows.
    """
    query = db.query(Task)
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)
    return query.offset(skip).limit(limit).all()


def service_search_tasks(
    db: Session,
    keyword: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    assigned_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
):
    """
    'Search Tasks' feature from SRS Module 5 / Module 8 (Search).

    All filters are optional and combine with AND, so a caller can search by
    just a keyword, just a status, or any mix of the four.

    Args:
        db: database session.
        keyword: matched (case-insensitive) against title and description.
        status: exact match on task status ("todo" / "in_progress" / "done").
        priority: exact match on task priority ("low" / "medium" / "high").
        assigned_id: exact match on the assignee's user id.
        skip: pagination offset.
        limit: pagination page size.

    Returns:
        list of matching Task rows.
    """
    query = db.query(Task)
    if keyword:
        like_pattern = f"%{keyword}%"
        query = query.filter(
            (Task.title.ilike(like_pattern)) | (Task.description.ilike(like_pattern))
        )
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assigned_id is not None:
        query = query.filter(Task.assigned_id == assigned_id)
    return query.offset(skip).limit(limit).all()