from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50),unique=True)
    password = Column(String)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer) 
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, default="todo")
    created_at = Column(DateTime, default=datetime.utcnow)
