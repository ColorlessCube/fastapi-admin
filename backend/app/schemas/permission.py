"""
权限相关的 Pydantic 模式
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PermissionBase(BaseModel):
    """权限基础模式"""
    name: str
    code: str
    description: Optional[str] = None
    resource: str
    action: str
    is_active: bool = True


class PermissionCreate(PermissionBase):
    """创建权限模式"""
    pass


class PermissionUpdate(BaseModel):
    """更新权限模式"""
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None
    is_active: Optional[bool] = None


class PermissionInDBBase(PermissionBase):
    """数据库中的权限基础模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Permission(PermissionInDBBase):
    """权限响应模式"""
    pass
