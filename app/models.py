from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)

    posts = relationship("Post", back_populates="author", cascade="all, delete")
    comments = relationship("Comment", back_populates="author", cascade="all, delete")
    friendships = relationship("Friendship", foreign_keys="Friendship.user_id", cascade="all, delete")
    friend_of = relationship("Friendship", foreign_keys="Friendship.friend_id", cascade="all, delete")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_like_user_post"),
    )

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

class Friendship(Base):
    __tablename__ = "friendships"
    __table_args__ = (
        UniqueConstraint("user_id", "friend_id", name="unique_friendship"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    friend_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)

# Tabela de sessões (para invalidar tokens de forma real)
class SessionToken(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True)       # ID único do token
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)           # Se false => token inválido
