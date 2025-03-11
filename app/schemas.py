from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ------------------ USER ------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    full_name: Optional[str] = None
    profile_image: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True

# ------------------ POST ------------------
class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    content: str
    image_urls: Optional[List[str]] = []

class PostImageOut(BaseModel):
    id: int
    image_url: str

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: UserOut
    images: List[PostImageOut] = []

    class Config:
        from_attributes = True

# ------------------ COMMENT ------------------
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    post_id: int
    author: UserOut

    class Config:
        from_attributes = True

# ------------------ LIKE ------------------
class LikeOut(BaseModel):
    post_id: int
    user_id: int

    class Config:
        from_attributes = True

# ------------------ FRIENDSHIP ------------------
class FriendOut(BaseModel):
    id: int
    user_id: int
    friend_id: int

    class Config:
        from_attributes = True

# ------------------ TOKEN ------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    jti: Optional[str] = None
    username: Optional[str] = None

# ------------------ LOGOUT ------------------
class LogoutOut(BaseModel):
    detail: str
