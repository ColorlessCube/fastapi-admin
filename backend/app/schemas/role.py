"""
角色相关的 Pydantic 模式
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class RoleBase(BaseModel):
    """角色基础模式"""
    name: str
    description: Optional[str] = None
    is_active: bool = True


class RoleCreate(RoleBase):
    """创建角色模式"""
    pass


class RoleUpdate(BaseModel):
    """更新角色模式"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RoleInDBBase(RoleBase):
    """数据库中的角色基础模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Role(RoleInDBBase):
    """角色响应模式"""
    pass


class RoleWithPermissions(Role):
    """包含权限信息的角色模式"""
    permissions: List["Permission"] = []


# 避免循环导入
from .permission import Permission
RoleWithPermissions.model_rebuild()
