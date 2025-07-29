"""
用户 CRUD 操作
"""
from typing import Any, Dict, Optional, Union, List, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate, UserPreferences


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """用户 CRUD 操作类"""
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """创建用户"""
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # 分配角色
        if obj_in.role_ids:
            roles = db.query(Role).filter(Role.id.in_(obj_in.role_ids)).all()
            db_obj.roles = roles
            db.commit()
            db.refresh(db_obj)

        return db_obj
    
    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """更新用户"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # 处理角色分配
        role_ids = update_data.pop("role_ids", None)

        # 如果更新密码，需要加密
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        # 更新基本信息
        updated_user = super().update(db, db_obj=db_obj, obj_in=update_data)

        # 更新角色
        if role_ids is not None:
            roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
            updated_user.roles = roles
            db.commit()
            db.refresh(updated_user)

        return updated_user
    
    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        """用户认证"""
        user = self.get_by_username(db, username=username)
        if not user:
            user = self.get_by_email(db, email=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        """检查用户是否激活"""
        return user.is_active

    def get_with_roles(self, db: Session, *, id: int) -> Optional[User]:
        """获取用户及其角色信息"""
        from sqlalchemy.orm import joinedload
        return db.query(User).options(
            joinedload(User.roles).joinedload(Role.permissions)
        ).filter(User.id == id).first()

    def update_login_info(self, db: Session, *, user: User, ip_address: str = None) -> User:
        """更新用户登录信息"""
        user.last_login_at = datetime.utcnow()
        user.last_login_ip = ip_address
        # 增加登录次数
        try:
            current_count = int(user.login_count or '0')
            user.login_count = str(current_count + 1)
        except ValueError:
            user.login_count = '1'

        db.commit()
        db.refresh(user)
        return user

    def update_preferences(self, db: Session, *, user: User, preferences: UserPreferences) -> User:
        """更新用户偏好设置"""
        if preferences.preferred_language is not None:
            user.preferred_language = preferences.preferred_language
        if preferences.timezone is not None:
            user.timezone = preferences.timezone

        db.commit()
        db.refresh(user)
        return user

    def get_multi_with_search(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        keyword: Optional[str] = None,
        role_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[User], int]:
        """
        获取用户列表（支持搜索和筛选）
        """
        query = db.query(User)

        # 关键词搜索
        if keyword:
            search_filter = or_(
                User.username.ilike(f"%{keyword}%"),
                User.email.ilike(f"%{keyword}%"),
                User.full_name.ilike(f"%{keyword}%")
            )
            query = query.filter(search_filter)

        # 角色筛选
        if role_id is not None:
            query = query.join(User.roles).filter(Role.id == role_id)

        # 状态筛选
        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        # 获取总数
        total = query.count()

        # 分页
        users = query.offset(skip).limit(limit).all()

        return users, total

    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """
        获取用户统计信息
        """
        from app.models.role import Role

        total = db.query(User).count()
        active = db.query(User).filter(User.is_active == True).count()
        inactive = total - active
        roles = db.query(Role).count()

        return {
            "total": total,
            "active": active,
            "inactive": inactive,
            "roles": roles
        }


user = CRUDUser(User)
