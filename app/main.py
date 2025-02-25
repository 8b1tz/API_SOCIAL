from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, feed, posts, profile, friends

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Social com Logout Real")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(feed.router, prefix="/feed", tags=["feed"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(friends.router, prefix="/friends", tags=["friends"])

@app.get("/")
async def root():
    return {"message": "API Social pronta, com sessão JWT real e logout no servidor!"}
