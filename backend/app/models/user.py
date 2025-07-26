"""
用户数据模型
"""
from sqlalchemy import Column, String, Boolean, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import BaseModel


# 用户角色关联表
user_role_association = Table(
    'user_roles',
    BaseModel.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('role_id', ForeignKey('role.id'), primary_key=True)
)


class User(BaseModel):
    """
    用户模型
    """
    __tablename__ = "user"
    
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)

    # 用户偏好设置
    preferred_language = Column(String(10), default='zh-CN', nullable=False)  # 首选语言
    timezone = Column(String(50), nullable=True)  # 用户时区
    last_login_at = Column(DateTime, nullable=True)  # 上次登录时间
    last_login_ip = Column(String(45), nullable=True)  # 上次登录IP
    login_count = Column(String(10), default='0', nullable=False)  # 登录次数

    # 关联角色
    roles = relationship(
        "Role",
        secondary=user_role_association,
        back_populates="users"
    )
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
