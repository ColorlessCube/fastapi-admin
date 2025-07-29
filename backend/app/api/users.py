"""
用户管理 API
"""
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.core.database import get_db
from app.crud.user import user as crud_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate, UserWithRoles, UserPreferences, PasswordChange

router = APIRouter()


@router.get("/")
def read_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词（用户名、邮箱、姓名）"),
    role_id: Optional[int] = Query(None, description="角色ID筛选"),
    is_active: Optional[bool] = Query(None, description="状态筛选"),
    current_user: User = Depends(deps.require_permission("user:read")),
) -> Any:
    """
    获取用户列表（支持搜索和筛选）
    """
    users, total = crud_user.get_multi_with_search(
        db,
        skip=skip,
        limit=limit,
        keyword=keyword,
        role_id=role_id,
        is_active=is_active
    )

    # 转换为字典格式以便序列化
    users_data = []
    for user in users:
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "roles": [{"id": role.id, "name": role.name} for role in user.roles] if user.roles else []
        }
        users_data.append(user_dict)

    return {
        "data": users_data,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/", response_model=UserWithRoles)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(deps.require_permission("user:create")),
) -> Any:
    """
    创建新用户
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud_user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud_user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=UserWithRoles)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新当前用户信息
    """
    # 不允许用户修改自己的角色和超级用户状态
    update_data = user_in.dict(exclude_unset=True, exclude={'role_ids', 'is_superuser'})
    user = crud_user.update(db, db_obj=current_user, obj_in=update_data)
    return user


@router.get("/me", response_model=UserSchema)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取当前用户信息
    """
    return current_user


@router.get("/statistics")
def get_user_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.require_permission("user:read")),
) -> Any:
    """
    获取用户统计信息
    """
    stats = crud_user.get_statistics(db)
    return stats


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.require_permission("user:read")),
    db: Session = Depends(get_db),
) -> Any:
    """
    根据 ID 获取用户
    """
    user = crud_user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(deps.require_permission("user:update")),
) -> Any:
    """
    更新用户
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}")
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: User = Depends(deps.require_permission("user:delete")),
) -> Any:
    """
    删除用户
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )

    # 防止删除自己
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete yourself",
        )

    user = crud_user.remove(db, id=user_id)
    return {"message": "User deleted successfully"}


@router.put("/me/preferences", response_model=UserSchema)
def update_my_preferences(
    *,
    db: Session = Depends(get_db),
    preferences: UserPreferences,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    更新当前用户的偏好设置
    """
    user = crud_user.update_preferences(db, user=current_user, preferences=preferences)
    return user


@router.get("/me/preferences", response_model=UserPreferences)
def get_my_preferences(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    获取当前用户的偏好设置
    """
    return UserPreferences(
        preferred_language=current_user.preferred_language,
        timezone=current_user.timezone
    )


@router.put("/me", response_model=UserSchema)
def update_my_profile(
    *,
    db: Session = Depends(get_db),
    user_update: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    更新当前用户的基本信息
    """
    # 不允许修改用户名
    user_update.username = None
    user_update.role_ids = None
    user_update.is_active = None

    user = crud_user.update(db, db_obj=current_user, obj_in=user_update)
    return user


@router.put("/me/password")
def change_my_password(
    *,
    db: Session = Depends(get_db),
    password_change: PasswordChange,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    修改当前用户的密码
    """
    from app.core.security import verify_password, get_password_hash

    # 验证当前密码
    if not verify_password(password_change.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    # 更新密码
    current_user.hashed_password = get_password_hash(password_change.new_password)
    db.commit()

    return {"message": "Password changed successfully"}


