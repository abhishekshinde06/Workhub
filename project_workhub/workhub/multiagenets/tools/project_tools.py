from workhub.projects.schema import CreateProjectSchema,UpdateProjectSchema
from langchain.tools import tool
from sqlalchemy import select
from workhub.projects.service import service_create_project,service_update_project,service_show_project,service_delete_project
from workhub.projects.models import Project

def get_project_tools(db,current_user) :
    @tool
    async def list_projects (db):
        """It Shows all projects"""
        return service_show_project(db)
    
    @tool(args_schema=CreateProjectSchema)
    async def create_project(project_name : str,description : str) :
        """It Create the project through arguments that will provide by the user"""
        request = CreateProjectSchema(project_name=project_name,description=description)
        return await service_create_project(request,db,current_user)
        
    @tool(args_schema = UpdateProjectSchema)
    async def update_project(project_name,description) :
        """Update Project detail through user provided fileds"""
        request = UpdateProjectSchema(project_name= project_name,description=description)
        result = db.execute(select(Project.project_id).where(
        Project.project_name.like(f"%{project_name}%")
            )
            ).scalar_one_or_none()
        project_id = result.project_id
        return await service_update_project(project_id,request,db,current_user)

    @tool
    async def delete_project(project_name) :
        """It delete the project using detail of the projects"""
        result = db.execute(select(Project.project_id).where(
            Project.project_name.like(f"%{project_name}%")
                )
                ).scalar_one_or_none()
        project_id = result.project_id
        return await service_delete_project(project_id,db,current_user)
        
