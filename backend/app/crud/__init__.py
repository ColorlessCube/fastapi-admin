"""
CRUD 操作模块
"""
from .user import user
from .role import role
from .permission import permission
from .system_config import crud_system_config

__all__ = ["user", "role", "permission"]
