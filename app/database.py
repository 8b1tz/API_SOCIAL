from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão. Ajuste conforme o seu banco (PostgreSQL, MySQL, etc.)
# Exemplo para SQLite local:
SQLALCHEMY_DATABASE_URL = "sqlite:///./social.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency para obter a sessão do DB em cada requisição."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
