from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco de dados (substitua pela sua URL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./meu_banco.db"  # Exemplo para SQLite
# Para PostgreSQL: "postgresql+psycopg2://user:password@localhost:5432/mydatabase"

# Cria a engine do banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # Apenas para SQLite
)

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()