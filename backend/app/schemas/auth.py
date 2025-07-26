"""
认证相关的 Pydantic 模式
"""
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """令牌模式"""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """令牌载荷模式"""
    sub: Optional[str] = None


class LoginRequest(BaseModel):
    """登录请求模式"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """登录响应模式"""
    access_token: str
    token_type: str
    user: dict
