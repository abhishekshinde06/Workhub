from langchain.agents import create_agent
from .state import AgentState,chat_model
from ..tools import task_tools

def create_agent_task(AgentState) :
    agenet_task = create_agent(model=chat_model,system_prompt="""
        You are the Task Management Agent.

        Your responsibilities:
        1. Create tasks.
        2. Update tasks.
        3. Assign tasks to developers.
        4. Find tasks.
        5. Track task status.

        Use only the available tools.
        """
        )

