from pydantic import BaseModel
from typing import Optional

class CreateProjectSchema(BaseModel) : 
  
    project_name : str
    description : str


class UpdateProjectSchema(BaseModel):
    """All fields optional, so a caller can send just the field(s) they
    want to change (mirrors how UpdateUserDetail/UpdateTask work already)."""
    project_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
