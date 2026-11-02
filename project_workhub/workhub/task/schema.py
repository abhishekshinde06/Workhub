from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Allowed values for Task.status (SRS Module 5: 'Status')."""
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, Enum):
    """Allowed values for Task.priority (SRS Module 5: 'Priority')."""
    low = "low"
    medium = "medium"
    high = "high"


class CreateTask(BaseModel) : 
    title : str
    description :str
    assigned_id: int
    project_id : int
  
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[datetime] = None


class UpdateTask(BaseModel) :
    """All fields optional so a caller can update just one field at a time
    (service_update_task only applies whatever fields were actually sent)."""
    title : Optional[str] = None
    description : Optional[str] = None
    due_date: Optional[datetime] = None


class UpdateTaskStatus(BaseModel):
    """Dedicated schema for the 'Change Status' feature (SRS Module 5)."""
    status: TaskStatus