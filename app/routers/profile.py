from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import User
from app.schemas import UserOut, LogoutOut
from app.routers.auth import get_current_user, decode_token
from app.utils import invalidate_token
from app.schemas import TokenData

router = APIRouter()

@router.get("/", response_model=UserOut)
def get_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/", response_model=UserOut)
def update_profile(
    full_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza dados do perfil do usuário logado."""
    if full_name is not None:
        current_user.full_name = full_name
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/")
def delete_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Deleta a conta do usuário."""
    db.delete(current_user)
    db.commit()
    return {"detail": "Conta removida com sucesso"}
