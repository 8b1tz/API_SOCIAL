from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Friendship
from app.schemas import FriendOut
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[FriendOut])
def list_friends(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    friends_1 = db.query(Friendship).filter(Friendship.user_id == current_user.id).all()
    friends_2 = db.query(Friendship).filter(Friendship.friend_id == current_user.id).all()
    return friends_1 + friends_2

@router.post("/{friend_id}", response_model=FriendOut)
def add_friend(friend_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if friend_id == current_user.id:
        raise HTTPException(status_code=400, detail="Você não pode ser amigo de si mesmo.")

    friend_user = db.query(User).filter(User.id == friend_id).first()
    if not friend_user:
        raise HTTPException(status_code=404, detail="Amigo não encontrado.")

    exists = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == friend_id)) |
        ((Friendship.user_id == friend_id) & (Friendship.friend_id == current_user.id))
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Amizade já existe.")

    new_friendship = Friendship(user_id=current_user.id, friend_id=friend_id)
    db.add(new_friendship)
    db.commit()
    db.refresh(new_friendship)
    return new_friendship

@router.delete("/{friendship_id}")
def remove_friend(friendship_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    friendship = db.query(Friendship).filter(Friendship.id == friendship_id).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Amizade não encontrada.")

    if friendship.user_id != current_user.id and friendship.friend_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para excluir essa amizade.")

    db.delete(friendship)
    db.commit()
    return {"detail": "Amizade removida com sucesso"}
