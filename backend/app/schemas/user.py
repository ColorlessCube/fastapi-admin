"""
用户相关的 Pydantic 模式
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """用户基础模式"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    preferred_language: Optional[str] = 'zh-CN'
    timezone: Optional[str] = None


class UserCreate(UserBase):
    """创建用户模式"""
    password: str
    role_ids: Optional[List[int]] = []


class UserUpdate(BaseModel):
    """更新用户模式"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    preferred_language: Optional[str] = None
    timezone: Optional[str] = None
    role_ids: Optional[List[int]] = None


class UserInDBBase(UserBase):
    """数据库中的用户基础模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    last_login_ip: Optional[str] = None
    login_count: Optional[str] = '0'

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """用户响应模式"""
    pass


class UserInDB(UserInDBBase):
    """数据库中的用户模式（包含密码哈希）"""
    hashed_password: str


class UserWithRoles(User):
    """包含角色信息的用户模式"""
    roles: List["Role"] = []


class UserPreferences(BaseModel):
    """用户偏好设置模式"""
    preferred_language: Optional[str] = None
    timezone: Optional[str] = None


class LoginInfo(BaseModel):
    """登录信息模式"""
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class PasswordChange(BaseModel):
    """密码修改模式"""
    current_password: str
    new_password: str


# 避免循环导入
from .role import Role
UserWithRoles.model_rebuild()
