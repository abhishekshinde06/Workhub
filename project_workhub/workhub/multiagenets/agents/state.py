import os
from pydantic import BaseModel
from typing import Literal,Optional,TypedDict
from langgraph.graph import MessagesState
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


GROK_API_KEY = os.getenv("GROK_API_KEY")
chat_model = ChatGroq(model="openai/gpt-oss-20b",api_key=GROK_API_KEY)


class AgentState(MessagesState) :
    next_agent : Literal[
        "project",
        "task",
        "user",
        "end" 
    ]
print(chat_model.invoke("hi i am abhiske"))