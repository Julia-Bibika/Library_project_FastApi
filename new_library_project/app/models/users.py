from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean

from app.session import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    nickname = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean)
    actions = Column(String(50), default='None action')

class UserHistories(Base):
    __tablename__ = "user-histories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(50), default='None action')
    timestamp = Column(DateTime, default=datetime.utcnow)