from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post, Comment, Like, User
from app.schemas import CommentCreate, CommentOut, LikeOut, PostOut
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/{post_id}/comments", response_model=List[CommentOut])
def get_comments(post_id: int, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id)\
                 .order_by(Comment.id.desc()).offset(skip).limit(limit).all()
    return comments

@router.post("/{post_id}/comments", response_model=CommentOut)
def create_comment(
    post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado.")

    new_comment = Comment(
        content=data.content,
        post_id=post.id,
        author_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/{post_id}/likes")
def get_likes(post_id: int, db: Session = Depends(get_db)):
    """Retorna a quantidade de likes de um post."""
    likes_count = db.query(Like).filter(Like.post_id == post_id).count()
    return {"post_id": post_id, "likes": likes_count}

@router.post("/{post_id}/likes", response_model=LikeOut)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado.")

    # Verifica se usuário já deu like
    like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == current_user.id).first()
    if like:
        raise HTTPException(status_code=400, detail="Você já deu like neste post.")

    new_like = Like(post_id=post_id, user_id=current_user.id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return {"post_id": new_like.post_id, "user_id": new_like.user_id}

@router.get("/", response_model=List[PostOut])
def get_feed(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = (
        db.query(Post)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts