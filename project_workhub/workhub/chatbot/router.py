from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from workhub.chatbot.graph import make_graph
from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from workhub.chatbot import schema, service,continue_talk_graph

router = APIRouter(tags=["Chatbot"])

@router.post('/talk_with_assistant')
async def start_converstation(request : schema.StartConversation,db : Session = Depends(get_db),current_user :str = Depends(verify_token)) :

    # ? IT is the the data then is going into the graph when we invoke graph for state.
    initial_state = {
        "messages" : [{
            "role" : "user","content" :request.prompt
        }]
    }
    
    # ? IT makes graph and return compiled graph object 
    graph_object = make_graph(db,current_user)

    #? BY graph object we invoke the graph 
    result = await graph_object.ainvoke(initial_state,context={
            "db": db,
            "current_user": current_user,
            "request" : request,
        })
    
    return result["messages"][-1].content


@router.post('/go_on_with_ai')
async def continue_conversation(request : schema.StartConversation,db : Session = Depends(get_db),current_user = Depends(verify_token)) :

    initial_state = {
            "messages" : [{
                "role" : "user","content" :request.prompt
            }],
            "conversation_id": request.conversation_id,
        }
        
        # ? IT makes graph and return compiled graph object 
    graph_object = continue_talk_graph.graph_building(db,current_user)

    #? BY graph object we invoke the graph 
    result = await graph_object.ainvoke(initial_state,context={
            "db": db,
            "current_user": current_user,
            "request" : request,
            })
        
    return result["messages"][-1].content
    

@router.get('/talk_with_assistant')
async def see_history_user(page:int ,page_size : int ,db : Session = Depends(get_db),current_user = Depends(verify_token)):
    return await service.service_list_conversations(db=db,current_user=current_user,page=page,page_size=page_size)