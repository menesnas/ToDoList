from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

class TodoResponse(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    
    class Config:
        from_attributes = True 