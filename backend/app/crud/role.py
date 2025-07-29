"""
角色 CRUD 操作
"""
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func

from app.crud.base import CRUDBase
from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User
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

    def get_multi_with_search(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        keyword: Optional[str] = None
    ) -> Tuple[List[Role], int]:
        """
        获取角色列表（支持搜索）
        """
        query = db.query(Role).options(joinedload(Role.permissions))

        # 关键词搜索
        if keyword:
            search_filter = or_(
                Role.name.ilike(f"%{keyword}%"),
                Role.description.ilike(f"%{keyword}%")
            )
            query = query.filter(search_filter)

        # 获取总数
        total = query.count()

        # 分页
        roles = query.offset(skip).limit(limit).all()

        return roles, total

    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """
        获取角色统计信息
        """
        total = db.query(Role).count()
        total_permissions = db.query(Permission).count()
        total_users = db.query(User).count()

        return {
            "total": total,
            "totalPermissions": total_permissions,
            "totalUsers": total_users
        }


role = CRUDRole(Role)
