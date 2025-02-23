from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Schema base para Comment
class CommentBase(BaseModel):
    content: str

# Schema para criação de Comment
class CommentCreate(CommentBase):
    pass

# Schema para leitura de Comment (resposta da API)
class Comment(CommentBase):
    id: int
    created_at: datetime
    user_id: int
    post_id: int

    class Config:
        from_attributes = True  # Habilita a compatibilidade com ORM