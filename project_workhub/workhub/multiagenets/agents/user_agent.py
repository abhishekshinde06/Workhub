from langchain.agents import create_agent 
from ..tools import user_tools
from .state import AgentState,chat_model

class create_user_agent(AgentState) :
    agent_user = create_agent(model = chat_model,tools=user_tools.user_tools,system_prompt=
       """
    You are the User Management Agent.
        Your responsibilities:
        1. Get user data.
        2. Update User details.

        Use the available tools to perform operations.

        """
        )

