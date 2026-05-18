from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY

from models import get_session
from models.user import User

async def require_auth(token: str = None) -> int:
    """从请求头获取当前用户（简化版，demo 用）"""
    # Demo 模式：直接返回 1
    return 1

def create_token(user_id: int, username: str) -> str:
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    username: str
    password: str
    display_name: str = ""

class LoginRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str
    username: str
    display_name: str

@router.post("/register")
async def register(req: RegisterRequest):
    session = next(get_session())
    try:
        result = session.execute(select(User).where(User.username == req.username))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        user = User(
            username=req.username,
            password_hash=bcrypt.hash(req.password),
            display_name=req.display_name or req.username
        )
        session.add(user)
        session.commit()
        
        token = create_token(user.id, user.username)
        return AuthResponse(token=token, username=user.username, display_name=user.display_name)
    finally:
        session.close()

@router.post("/login")
async def login(req: LoginRequest):
    session = next(get_session())
    try:
        result = session.execute(select(User).where(User.username == req.username))
        user = result.scalar_one_or_none()
        if not user or not bcrypt.verify(req.password, user.password_hash):
            raise HTTPException(status_code=401, detail="用户名或密码错误")
        
        token = create_token(user.id, user.username)
        return AuthResponse(token=token, username=user.username, display_name=user.display_name)
    finally:
        session.close()

@router.get("/me")
async def get_me(user_id: int = Depends(require_auth)):
    session = next(get_session())
    try:
        result = session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return {"username": user.username, "display_name": user.display_name}
    finally:
        session.close()