from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, feed, posts, profile, friends

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Social")

app.add_middleware(
    CORSMiddleware, # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(feed.router, prefix="/feed", tags=["feed"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(friends.router, prefix="/friends", tags=["friends"])

@app.get("/")
async def root():
    return {"message": "API Social pronta, com sessão JWT real e logout no servidor!"}
