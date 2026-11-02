from langchain.tools import tool
from workhub.task.models import Task
from workhub.projects.models import Project
from sqlalchemy import select
from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings
embeding_model = HuggingFaceEmbeddings(model = "sentence-transformers/all-MiniLM-L6-v2")


def tool_pass_data(db,current_user) :
    user_id =  current_user["user_id"]

    @tool
    async def get_task_detail():
        """Get the tasks assigned to the currently logged-in user."""
        result = await db.execute(select(Task).where(Task.assigned_id == user_id))
        tasks = result.scalars().all()
       
        if not tasks:
            return {"messages" : "you did not have any task to  do"}
        return [
            {
                "task_id": task.task_id,
                "title": task.title,
                "status": task.status
            }
            for task in tasks
        ]
    @tool
    async def get_project() :
        """Get details of  projects by user ID."""
     
        result = await db.execute(select(Project).where(Project.manager_id == user_id))
        project_data = result.scalars().all()
        
        if not project_data:
            return {
                "message" : "NO project found for this user"
            }
        return [{
            "title" : project_data.project_name,
            "description" : project_data.description,
            "status" : project_data.status
        } for project_data in project_data]
    
    @tool
    async def get_task_by_name(task_name: str) -> dict:
        """Get details of a task assigned to the current user using its task name."""

        user_id = current_user["user_id"]

        
        result = await db.execute(
        select(Task).where(
        Task.assigned_id == user_id,
        Task.title.ilike(f"%{task_name}%")
            )
        )
        task = result.scalars().all()

        if not task:
            return {"error": "No matching task found."}

        return {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        }

    @tool
    async def retrieval_gen(user_question: str):
        
        """Search AeshTech company documents for policies, rules, culture, and other company information."""
        
        

        vector_store = Chroma(
            embedding_function=embeding_model,
            persist_directory="./chroma_db",
        )

        result = vector_store.similarity_search(
            query=user_question,
            k=5
        )
        
        print("DOCUMENTS FOUND:", len(result))

        if not result:
            return "No relevant company information found."

        rag_result = "\n\n".join(
            data.page_content for data in result
        )
        return rag_result
    @tool
    async def task_by_project(project_name : str) :
        """
        It search project detail by the name of project and according the name it gives all tasks that reltes from the project ; 
        """
        project_detail = db.query(Project).filter(
        Project.project_name.ilike(f"%{project_name}%"),
        Project.manager_id == current_user["user_id"]
        ).first()
        print("THIS IS THE PROJECT DETAILS",project_detail)
        if not project_detail:
            return {"message": "Project not found or access denied."}
    
        result = await db.execute(select(Task).where(Task.project_id == project_detail.project_id))
        task_detail = result.scalars().all()
        for a in task_detail :
            print(a.title)
        return {
            "project_name": project_detail.project_name,
            "total_tasks": len(task_detail),
            "tasks": [
                {
                    "task_id": task.task_id,
                    "title": task.title,
                    "status": task.status,
                }
                for task in task_detail
            ]
        }

    @tool
    async def task_assigned():
        """
        it gives all the task that assigned by the project holder(admin\manager) to the developres
        """
        
        result = await db.execute(select(Task).where(Task.manager_id == user_id))
        task_details = result.scalars().all()
        if not task_details :
            return {"messages" : "We have not given any task to any developer"}
        return {
            "tasks" : [
                {
                "task_id" :task.task_id,
                "task_title" : task.title,
                "status" : task.status,
                "description" : task.description
                }
                for task in task_details
            ]
        }

    return [get_task_detail, get_project,retrieval_gen,task_by_project,task_assigned]

    