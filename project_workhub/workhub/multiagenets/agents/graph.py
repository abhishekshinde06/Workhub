from langgraph.graph import StateGraph,START,END
from .state import AgentState
from .project_agent import create_project_agent
from .task_agent import create_agent_task
from .user_agent import create_user_agent
from .supervisor import create_supervisor

def build_graph(supervisor,project_agent,task_agent,user_agent) :
    builder = StateGraph(AgentState)
    
# supervisor node 
    def supervisor_node(state) :
        decision = supervisor.invoke(
            state['messages']
        )
        return {
            'next_agent' : decision.next_agent
            }
# project nodes 
    def project_node(state) :
        result =  project_agent.invoke({"messages":state["messages"]})
        return {
            'messages' : result["messages"][-1:]
        }
# task nodes 
    def task_node(state) :
        result = task_agent.invoke({"messages": state["messages"]})
        return {
            "messages" : result["messages"][-1 :]
        }
#user Detail node
    def user_node(state) :
        result =  user_agent.invoke({"messages" : state["messages"]})
        return {"messages" : result["messages"][-1:]}
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("project", project_node)
    builder.add_node("task", task_node)
    builder.add_node("user", user_node)

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
    "supervisor",
    lambda state: state["next_agent"],
        {
            "project": "project",
            "task": "task",
            "user": "user",
            "end": END
        }
    )

    for agent in ["project", "task", "user"]:
        builder.add_edge(agent, END)

    return builder.compile()