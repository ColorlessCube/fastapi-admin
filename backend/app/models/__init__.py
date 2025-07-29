"""
数据模型模块
"""
from app.core.database import Base
from .base import BaseModel
from .user import User
from .role import Role
from .permission import Permission
from .system_config import SystemConfig
from .notification_client import NotificationClient

__all__ = ["Base", "BaseModel", "User", "Role", "Permission", "SystemConfig", "NotificationClient"]
