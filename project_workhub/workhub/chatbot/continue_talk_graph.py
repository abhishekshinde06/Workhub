from langgraph.graph import StateGraph,START,END
from .schema import ContinueConversation
from langgraph.prebuilt import tools_condition,ToolNode
from .service import get_chat_history,get_conversation,call_llm,create_title,tool_pass_data,save_conversation
def graph_building(db,current_user):
    tools = tool_pass_data(db,current_user)
    noded_tool = ToolNode(tools)
    graph = StateGraph(ContinueConversation)

    graph.add_node('get_conversations',get_conversation)
    graph.add_node('save conversations',save_conversation)
    graph.add_node('calling_llm',call_llm)
    graph.add_node('tool node',noded_tool)

    graph.add_edge(START,"get_conversations")
    graph.add_edge('get_conversations','save conversations')
    graph.add_edge('save conversations','calling_llm')
    graph.add_conditional_edges("calling_llm",tools_condition,{
        "tools": "tool node",
        "__end__": END
    })

    graph.add_edge("tool node","calling_llm")
    compiled_graph = graph.compile()
    return compiled_graph
