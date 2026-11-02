from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentOut(BaseModel):
    """What we hand back after upload / in list & search results."""
    document_id: int
    original_filename: str
    file_extension: str
    project_id: Optional[int] = None
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
