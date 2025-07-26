"""
权限 CRUD 操作
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    """权限 CRUD 操作类"""
    
    def get_by_code(self, db: Session, *, code: str) -> Optional[Permission]:
        """根据代码获取权限"""
        return db.query(Permission).filter(Permission.code == code).first()
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Permission]:
        """根据名称获取权限"""
        return db.query(Permission).filter(Permission.name == name).first()


permission = CRUDPermission(Permission)
