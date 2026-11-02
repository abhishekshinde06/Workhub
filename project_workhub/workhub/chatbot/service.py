import os
from sqlalchemy import select
from langgraph.runtime import Runtime
from langchain_groq import ChatGroq
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from workhub.chatbot.schema import ChatState,ChatContext,ContinueConversation
from langchain.messages import HumanMessage,AIMessage
from workhub.chatbot.models import Conversation, Message
from workhub.chatbot.tools import tool_pass_data

#! NOTE => IT HAVE MY AI MODEL INFO 
GROK_API_KEY = os.getenv("GROK_API_KEY")
chat_model = ChatGroq(model="openai/gpt-oss-20b",api_key=GROK_API_KEY)

#!======================================================================!#
async def call_llm(state: dict,runtime : Runtime[ChatContext]) -> dict:
    """
        Call LLM => This funtion that help to get answer from an llm .
        Working=> according to user propmt it check whether LLM Model needs the tool or not.
        Tool=> If LLm decide to choose tool then by the help on conditonal edge it goes for tools and run then whatever the output comes it again check the output and see whether we needed tool or not.
    """
    current_user = runtime.context["current_user"]
    db= runtime.context["db"]
    
    tools = tool_pass_data(db,current_user)
    llm_with_tool = chat_model.bind_tools(tools, parallel_tool_calls=True)
    print("||| AI IS CALLING NOW |||")

    try:
        
        result = llm_with_tool.invoke(state["messages"])
       
        user_conversation = Message(role= "user",conversation_id = state["conversation_id"],content =result.content,model="GROQ")
        db.add(user_conversation)
        await db.commit()
        await db.refresh(user_conversation)

        return {"messages" : [result]}
    
    except Exception as e: 
        print(e)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Chatbot provider request failed: {str(e)}",
        )

async def get_chat_history(db,conversation_id) :
    try : 
        result = await db.execute(select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()))
        history = result.scalars().all()
        message_history = [{"role": msg.role, "content": msg.content} for msg in history]
        return message_history
    except Exception as e :
        print("History fetching in fail",e)

def convert_history(message_history) :
    messages = []
    print(message_history)
    for msg in message_history :
        if msg["role"].lower() == "user" :
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"].lower() == "ai" :
            messages.append(AIMessage(content = msg["content"]))
    if not messages:
             raise ValueError("No valid messages found in conversation history")
    return messages
    
async def get_conversation(state : ContinueConversation,runtime : Runtime[ChatContext]) :
    current_user = runtime.context["current_user"]
    db= runtime.context["db"]
    request = runtime.context["request"]
    result = await db.execute(select(Conversation).where(Conversation.conversation_id == state["conversation_id"]))
    conversation = result.scalars().first()
    if not conversation or (
        conversation.user_id != current_user["user_id"] and current_user["role"] != "admin"
    ):
        raise HTTPException(detail="Conversation not found", status_code=status.HTTP_404_NOT_FOUND)
    return {}
    
# =================================================================================
async def save_conversation(state : ContinueConversation,runtime  : Runtime[ChatContext]) : 

    db= runtime.context["db"]
    request = runtime.context["request"]
    try :
        new_message = Message(conversation_id = request.conversation_id,role= "user",content = request.prompt)
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        chat_history = await get_chat_history(db,state["conversation_id"])
        history = convert_history(chat_history)
        return {"messages" : history,"conversation_id": state["conversation_id"]}
        
        
    except Exception as e :
        print("This is the error when we are working on conitnue chat api",e)



async def create_title(state: ChatState) :
   
    result =  await chat_model.ainvoke( f"""
        You are a title generator.
        Generate a short and meaningful title for the following user prompt.

        User prompt:
       {state["messages"][-1].content}
    
        Return only the title, without quotes.
        """)
    print(f"title now created {result.content}")
    return {"messages" : [result]}


async def service_start_conversation(state: ChatState,runtime : Runtime[ChatContext]):

    current_user = runtime.context["current_user"]
    db= runtime.context["db"]
    request = runtime.context["request"]
  
    if not request.conversation_id :

        Session_circle = Conversation(user_id = current_user["user_id"],title = state["messages"][-1].content)
        db.add(Session_circle)
        await db.commit()
        await db.refresh(Session_circle)
        
    else :
        Session_circle = get_conversation(request.conversation_id,db,current_user)
    
    user_conversation = Message(role= "user",conversation_id = Session_circle.conversation_id,content = state["messages"][-1].content,model="GROQ")
    db.add(user_conversation)
    await db.commit()
    await db.refresh(user_conversation)
    chat_history = await get_chat_history(db,Session_circle.conversation_id)
    history = convert_history(chat_history)
 
    return {"messages" : history,"conversation_id": Session_circle.conversation_id}

#!======================================================================!#



async def service_list_conversations(db: Session, current_user: dict, page : int, page_size :int):
    """'View previous conversations' (SRS Module 11) -- list, not the messages themselves.
    Sorted by updated_at (most recently active conversation first), not created_at."""
    skip = (page-1)*page_size
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == current_user["user_id"])
        .order_by(Conversation.updated_at.desc()))
    data = result.scalars().all()

    paginated_tasks = data[skip:skip + page_size]

    print("Paginated data:", paginated_tasks)
    return {
    "page": page,
    "page_size": page_size,
    "tasks": paginated_tasks
    }


async def service_view_conversation_messages(conversation_id: int, db: Session, current_user: dict):
    """'View previous conversations' (SRS Module 11) -- the messages inside one conversation."""
    conversation = get_conversation(conversation_id, db, current_user)
    result = await db.execute(select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()))
    data = result.scalars().all()
    return (
            data
        )

async def service_delete_conversation(conversation_id: int, db: Session, current_user: dict):
    """'Delete conversation history' (SRS Module 11)."""
    conversation = get_conversation(conversation_id, db, current_user)
    await db.delete(conversation) 
    await db.commit()
    return {"message": "Conversation deleted successfully"}

