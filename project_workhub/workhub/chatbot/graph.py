from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.runtime import Runtime
from workhub.chatbot.schema import ChatState,ChatContext
from workhub.chatbot.service import service_start_conversation,call_llm,tool_pass_data,save_conversation,create_title

def route_conversation(
    state: ChatState,
    runtime: Runtime[ChatContext],
):
    request = runtime.context["request"]

    if request.conversation_id:
        return "new_conversation"

    return "create title"

def make_graph(db,current_user) :
    print("YOU ENTERED IN GRAPH")
    tools = tool_pass_data(db,current_user)

    noded_tool = ToolNode(tools)

    graph_builder = StateGraph(ChatState)

    graph_builder.add_node("create title",create_title)
    graph_builder.add_node("new_conversation",service_start_conversation)
    graph_builder.add_node("tool node",noded_tool)
    graph_builder.add_node("call llm",call_llm)
    graph_builder.add_node("save conversation",save_conversation)



    graph_builder.add_conditional_edges(START,route_conversation,{
        "create title" : "create title",
        "new_conversation" : "new_conversation"
    })

    graph_builder.add_edge("new_conversation","call llm")
    graph_builder.add_edge("call llm","save conversation")

    graph_builder.add_conditional_edges("call llm",tools_condition,{
        "tools": "tool node",
        "__end__": END
    })

    graph_builder.add_edge("tool node","call llm")
    compiled_graph = graph_builder.compile()
    
    png_data = compiled_graph.get_graph().draw_mermaid_png()

    with open("graph.png", "wb") as f:
        f.write(png_data)

    print("Graph image saved as graph.png")
    return compiled_graph


