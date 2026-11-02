from pydantic import BaseModel
from typing import Optional
from enum import Enum


class CommentEntityType(str, Enum):
    """Which kind of thing a comment is attached to (SRS Module 6)."""
    project = "project"
    task = "task"


class CreateComment(BaseModel):
    entity_type: CommentEntityType
    entity_id: int
    content: str


class UpdateComment(BaseModel):
    content: str
