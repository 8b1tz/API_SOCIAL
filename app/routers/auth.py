from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.utils import hash_password, verify_password, create_access_token, decode_token, invalidate_token
from app.schemas import LogoutOut
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Decodifica o token e checa se a sessão está ativa."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_token(token)
    if not token_data.jti or not token_data.username:
        raise credentials_exception

    # Busca a sessão no DB
    session_record = db.query(models.SessionToken).filter_by(jti=token_data.jti).first()
    if not session_record or not session_record.is_active:
        # Sessão não existe ou está inativa => token inválido
        raise credentials_exception

    # Checa se expirou
    if session_record.expires_at < models.datetime.utcnow():
        # Expirou => inativa
        session_record.is_active = False
        db.commit()
        raise credentials_exception

    # Busca o usuário
    user = db.query(models.User).filter_by(username=token_data.username).first()
    if not user:
        raise credentials_exception

    return user

@router.post("/register", response_model=schemas.UserOut)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se username já existe
    user_in_db = db.query(models.User).filter(models.User.username == user_data.username).first()
    if user_in_db:
        raise HTTPException(status_code=400, detail="Username já cadastrado.")

    # Verifica se email já existe
    email_in_db = db.query(models.User).filter(models.User.email == user_data.email).first()
    if email_in_db:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    hashed = hash_password(user_data.password)
    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed,
        profile_image=user_data.profile_image
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Faz login com OAuth2PasswordRequestForm (username e password).
    Retorna token JWT + token_type.
    """
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha incorreta.")

    # Gera JWT e salva a sessão
    token_str, _ = create_access_token(db, user.id, user.username)
    return {"access_token": token_str, "token_type": "bearer"}

@router.post("/logout", response_model=LogoutOut)
def logout(
    raw_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Invalida o token no servidor, fazendo logout real.
    Após este endpoint, o token atual deixa de ser aceito.
    """
    token_data = decode_token(raw_token)
    if token_data.jti:
            invalidate_token(db, token_data.jti)

    return {"detail": "Logout realizado com sucesso"}