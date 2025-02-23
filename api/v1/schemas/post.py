from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    likes_count: int

    class Config:
        from_attributes = True