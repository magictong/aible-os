from sqlalchemy import Column, Integer, String, DateTime, func
from models import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    display_name = Column(String(64), default="")
    created_at = Column(DateTime, server_default=func.now())
