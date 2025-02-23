from app.db.session import engine, Base

from app.api.v1.models import post_likes, Comment, Post, User

# Cria as tabelas no banco de dados
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()