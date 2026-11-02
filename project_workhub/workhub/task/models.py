from sqlalchemy import ForeignKey, Integer,Column, String, DateTime

from workhub.db_connection import Base
# from sqlalchemy.orm import 


class Task(Base) : 
    """
    Task table for Module 5 of the SRS.

    Added `status`, `priority` and `due_date` here because the SRS explicitly
    says every task should support at least: Status, Priority, Assignee and
    Due Date. `assigned_id` (Assignee) already existed; the other three are
    new columns added on top of the original table.
    """
    __tablename__ = "project_task"
    manager_id  = Column(Integer,ForeignKey("users.user_id"),nullable=True)
    task_id = Column(Integer,index=True,primary_key = True, autoincrement=True)
    title = Column(String,nullable = False)
    description = Column(String,nullable = False)
    # status: "todo" (default) | "in_progress" | "done" -- see schema.TaskStatus
    status = Column(String, default="todo", nullable=False)
    # priority: "low" | "medium" (default) | "high" -- see schema.TaskPriority
    priority = Column(String, default="medium", nullable=False)
    due_date = Column(DateTime, nullable=True)
    assigned_id =Column(Integer,ForeignKey("users.user_id"))
    project_id = Column(Integer,ForeignKey("projects.project_id"))


