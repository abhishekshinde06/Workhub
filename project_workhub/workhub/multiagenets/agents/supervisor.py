from pydantic import BaseModel
from .state import chat_model
from typing import Literal

class RouteDecision(BaseModel) :
    next_agent : Literal[
        "project",
        "user",
        "task",
        "end"
    ]
    

def create_supervisor(chat_model) :
    return chat_model.with_structured_output(
        RouteDecision
    )

