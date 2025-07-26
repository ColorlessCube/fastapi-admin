"""
角色 CRUD 操作
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    """角色 CRUD 操作类"""

    def get(self, db: Session, id: int) -> Optional[Role]:
        """根据 ID 获取角色（包含权限）"""
        return db.query(Role).options(joinedload(Role.permissions)).filter(Role.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Role]:
        """获取多个角色（包含权限）"""
        return db.query(Role).options(joinedload(Role.permissions)).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        """根据名称获取角色"""
        return db.query(Role).filter(Role.name == name).first()


role = CRUDRole(Role)
