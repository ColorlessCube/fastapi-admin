"""
角色数据模型
"""
from sqlalchemy import Column, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


# 角色权限关联表
role_permission_association = Table(
    'role_permissions',
    BaseModel.metadata,
    Column('role_id', ForeignKey('role.id'), primary_key=True),
    Column('permission_id', ForeignKey('permission.id'), primary_key=True)
)


class Role(BaseModel):
    """
    角色模型
    """
    __tablename__ = "role"
    
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # 关联用户
    users = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )
    
    # 关联权限
    permissions = relationship(
        "Permission",
        secondary=role_permission_association,
        back_populates="roles"
    )
    
    def __repr__(self):
        return f"<Role(name='{self.name}')>"
