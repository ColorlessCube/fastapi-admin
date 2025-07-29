"""
Pydantic 模式模块
"""
from .user import User, UserCreate, UserUpdate, UserWithRoles
from .role import Role, RoleCreate, RoleUpdate, RoleWithPermissions
from .permission import Permission, PermissionCreate, PermissionUpdate
from .auth import Token, TokenPayload, LoginRequest, LoginResponse
from .system_config import SystemConfig, SystemConfigCreate, SystemConfigUpdate, SystemConfigInDB
from .notification_client import (
    NotificationClient, NotificationClientCreate, NotificationClientUpdate,
    NotificationTypeConfig, NotificationScenario, NotificationTestRequest,
    NotificationTestResponse, NotificationSendRequest, NotificationSendResponse
)

__all__ = [
    "User", "UserCreate", "UserUpdate", "UserWithRoles",
    "Role", "RoleCreate", "RoleUpdate", "RoleWithPermissions",
    "Permission", "PermissionCreate", "PermissionUpdate",
    "Token", "TokenPayload", "LoginRequest", "LoginResponse",
    "SystemConfig", "SystemConfigCreate", "SystemConfigUpdate", "SystemConfigInDB",
    "NotificationClient", "NotificationClientCreate", "NotificationClientUpdate",
    "NotificationTypeConfig", "NotificationScenario", "NotificationTestRequest",
    "NotificationTestResponse", "NotificationSendRequest", "NotificationSendResponse"
]
