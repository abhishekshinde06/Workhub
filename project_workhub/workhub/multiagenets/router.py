from fastapi import APIRouter
from project_workhub.workhub.multiagenets.tools import user_tools
from workhub.db_connection import get_db
from sqlalchemy.orm import Session
from tools import project_tools,task_tools
from .agents import user_agent,task_agent,project_agent,supervisor
from fastapi import Depends
from workhub.auth.setting.auth_setting import verify_token
router = APIRouter()

@router.post("/tiny_my")
async def my_tiny(db : Session = Depends(get_db),current_user = Depends(verify_token)) :
    project_tools = project_tools.get_project_tools(db, current_user)
    task_tools = task_tools.get_task_tools(db, current_user)
    user_tools = user_tools.get_user_tools(db, current_user)
    supervisor.create_supervisor()
    
