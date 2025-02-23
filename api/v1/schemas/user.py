from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Schema base para User
class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    birthdate: Optional[datetime] = None
    country: Optional[str] = None
    description: Optional[str] = None
    profile_picture: Optional[str] = None

# Schema para criação de User
class UserCreate(UserBase):
    password: str  # Adicione um campo para senha

# Schema para atualização de User
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    birthdate: Optional[datetime] = None
    country: Optional[str] = None
    description: Optional[str] = None
    profile_picture: Optional[str] = None

# Schema para leitura de User (resposta da API)
class User(UserBase):
    id: int
    friends: List["User"] = []  # Lista de amigos (relacionamento recursivo)

    class Config:
        from_attributes = True  # Habilita a compatibilidade com ORM (antigo `orm_mode`)

# Schema para relacionamento de amigos
class UserFriend(BaseModel):
    id: int
    name: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

# Atualiza o schema User para incluir amigos
User.update_forward_refs()