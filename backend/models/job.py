from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Job(BaseModel):
    id: str
    title: str
    company: str    
    url: str 
    posted_at: datetime
    application_deadline_at: datetime
    locations: str
    description: str = ""
    embedding_text: str = ""
    is_deleted: bool = False