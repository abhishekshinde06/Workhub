from langchain.agents import create_agent
from .state import chat_model
from ..tools import project_tools
def create_project_agent() :
    decided_agent = create_agent(
        model = chat_model,
        tools=project_tools.get_project_tools,
        system_prompt="""
        You are the Project Management Agent.

        Your responsibilities:
        1. Create projects.
        2. Update project details.
        3. Find projects.
        4. Get project information.

        Use the available tools to perform operations.
        Do not invent project IDs or claim success
        without tool confirmation.
        """
    )
    print(f"IN project Agent decide agents are here now {decided_agent}")
    return decided_agent