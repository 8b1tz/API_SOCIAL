from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from .friendship import user_friends

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    birthdate = Column(DateTime, nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    country = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    profile_picture = Column(String(255), nullable=True)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    liked_posts = relationship("Post", secondary="post_likes", back_populates="likes")

    friends = relationship(
        "User",
        secondary=user_friends,
        primaryjoin=(id == user_friends.c.user_id),
        secondaryjoin=(id == user_friends.c.friend_id),
        backref="added_by",
    )