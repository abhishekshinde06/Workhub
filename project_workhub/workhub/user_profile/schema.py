from pydantic import BaseModel
from typing import Optional

class UpdateUserDetail(BaseModel) : 
    name : Optional[str] = None
    email_id : Optional[str] = None
    mobile_no :Optional[str] = None
    gender : Optional[str] = None
    
