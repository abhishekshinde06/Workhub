from pydantic import BaseModel
from datetime import datetime
from typing import Optional,Annotated,TypedDict
from langgraph.graph import add_messages


class StartConversation(BaseModel):
    """'Start a new conversation' -- the first prompt kicks it off."""
    conversation_id : Optional[int] = None
    prompt: str
    title: Optional[str] = None





class MessageOut(BaseModel):
    message_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationOut(BaseModel):
    conversation_id: int
    title: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ChatState(TypedDict) :
    messages : Annotated[list,add_messages]
    conversation_id : int | None

# Runtime context
class ChatContext(TypedDict):
    db: object
    current_user: dict
    
class ContinueConversation(TypedDict):
    """'Continue an existing conversation' -- just the next prompt."""
    messages : Annotated[list,add_messages]
    conversation_id : int