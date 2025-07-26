"""
权限数据模型
"""
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class Permission(BaseModel):
    """
    权限模型
    """
    __tablename__ = "permission"
    
    name = Column(String(50), unique=True, index=True, nullable=False)
    code = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    resource = Column(String(50), nullable=False)  # 资源类型，如 user, role, permission
    action = Column(String(20), nullable=False)    # 操作类型，如 create, read, update, delete
    
    # 关联角色
    roles = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions"
    )
    
    def __repr__(self):
        return f"<Permission(name='{self.name}', code='{self.code}')>"
