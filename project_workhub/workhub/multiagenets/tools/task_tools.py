from sqlalchemy import select
from workhub.task.models import Task
from workhub.task.schema import CreateTask,UpdateTask
from langchain.tools import tool
from workhub.task.service import service_create_task,service_assign_developer,service_update_task,service_delete_task

def task_tools(db,current_user) :
    @tool(args_schema=CreateTask)
    async  def create_new_task(title,description,assigned_id,project_id) :
        request = CreateTask(title=title,description=description,assigned_id=assigned_id,project_id = project_id)
        return await service_create_task(request,db,current_user)
    
    @tool(args_schema=UpdateTask)
    async def update_detail_task(title,description) :
        result = await db.execute(select(Task).where(Task.task_id.like(f"%{title}%"))).scalar_one_or_none()
        task_id = result.task_id
        request = UpdateTask(title= title,description=description)
        return await service_update_task(task_id=task_id,request=request,db=db)

    @tool
    async def give_task(title,user_id,db) :
        result = await db.execute(select(Task).where(Task.task_id.like(f"%{title}%"))).scalar_one_or_none()
        task_id = result.task_id
        return await service_assign_developer(task_id=task_id,user_id=user_id,db=db)  
    @tool  
    async def delect_task(title : str):
        '''It delete task using the title of the task '''
        result = await db.execute(select(Task).where(Task.task_id.like(f"%{title}%"))).scalar_one_or_none()
        task_id = result.task_id
        return await service_delete_task(task_id=task_id,db=db)





