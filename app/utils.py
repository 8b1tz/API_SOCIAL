from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import uuid  # para gerar jti
from app.schemas import TokenData
from sqlalchemy.orm import Session
from app import models

# Em produção, coloque em variáveis de ambiente
SECRET_KEY = "SUPER_SECRET_KEY_PRODUCAO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(db: Session, user_id: int, username: str):
    """
    Cria um token JWT contendo jti e sub=username,
    salva a sessão no banco, e retorna (jwt_token, session_record).
    """
    jti = str(uuid.uuid4())  # ID único para este token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Payload
    to_encode = {
        "sub": username,
        "jti": jti,
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Salva na tabela SessionToken
    session_record = models.SessionToken(
        jti=jti,
        user_id=user_id,
        created_at=datetime.utcnow(),
        expires_at=expire,
        is_active=True
    )
    db.add(session_record)
    db.commit()
    db.refresh(session_record)

    return encoded_jwt, session_record

def decode_token(token: str) -> TokenData:
    """
    Decodifica o JWT e retorna jti + username.
    Se inválido ou expirado, retorna TokenData vazio.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti: str = payload.get("jti")
        username: str = payload.get("sub")
        if not jti or not username:
            return TokenData()
        return TokenData(jti=jti, username=username)
    except JWTError:
        return TokenData()

def invalidate_token(db: Session, jti: str):
    """
    Marca a sessão como inativa (desativada).
    """
    session_record = db.query(models.SessionToken).filter(models.SessionToken.jti == jti).first()
    if session_record and session_record.is_active:
        session_record.is_active = False
        db.commit()
        db.refresh(session_record)
