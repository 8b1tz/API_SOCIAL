from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Post, User
from app.schemas import PostCreate, PostOut
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PostOut])
def get_feed(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retorna posts mais recentes, com paginação."""
    posts = db.query(Post).order_by(Post.id.desc()).offset(skip).limit(limit).all()
    return posts

@router.post("/", response_model=PostOut)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria um novo Post."""
    new_post = Post(content=post_data.content, author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
