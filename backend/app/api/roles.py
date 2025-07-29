"""
角色管理 API
"""
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.core.database import get_db
from app.crud.role import role as crud_role
from app.crud.permission import permission as crud_permission
from app.models.user import User
from app.schemas.role import Role as RoleSchema, RoleCreate, RoleUpdate, RoleWithPermissions

router = APIRouter()


@router.get("/")
def read_roles(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词（角色名称、描述）"),
    current_user: User = Depends(deps.require_permission("role:read")),
) -> Any:
    """
    获取角色列表（支持搜索）
    """
    roles, total = crud_role.get_multi_with_search(
        db,
        skip=skip,
        limit=limit,
        keyword=keyword
    )

    # 转换为字典格式以便序列化
    roles_data = []
    for role in roles:
        role_dict = {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "is_active": role.is_active,
            "created_at": role.created_at,
            "updated_at": role.updated_at,
            "permissions": [{"id": perm.id, "name": perm.name, "code": perm.code} for perm in role.permissions] if role.permissions else []
        }
        roles_data.append(role_dict)

    return {
        "data": roles_data,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/", response_model=RoleSchema)
def create_role(
    *,
    db: Session = Depends(get_db),
    role_in: RoleCreate,
    current_user: User = Depends(deps.require_permission("role:create")),
) -> Any:
    """
    创建新角色
    """
    role = crud_role.get_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=400,
            detail="The role with this name already exists in the system.",
        )
    role = crud_role.create(db, obj_in=role_in)
    return role


@router.get("/statistics")
def get_role_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.require_permission("role:read")),
) -> Any:
    """
    获取角色统计信息
    """
    stats = crud_role.get_statistics(db)
    return stats


@router.get("/{role_id}", response_model=RoleWithPermissions)
def read_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.require_permission("role:read")),
) -> Any:
    """
    根据 ID 获取角色
    """
    role = crud_role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=404,
            detail="The role with this id does not exist in the system",
        )
    return role


@router.put("/{role_id}", response_model=RoleSchema)
def update_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    role_in: RoleUpdate,
    current_user: User = Depends(deps.require_permission("role:update")),
) -> Any:
    """
    更新角色
    """
    role = crud_role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=404,
            detail="The role with this id does not exist in the system",
        )
    role = crud_role.update(db, db_obj=role, obj_in=role_in)
    return role


@router.delete("/{role_id}")
def delete_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    current_user: User = Depends(deps.require_permission("role:delete")),
) -> Any:
    """
    删除角色
    """
    role = crud_role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=404,
            detail="The role with this id does not exist in the system",
        )
    
    # 检查是否有用户使用此角色
    if role.users:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete role that is assigned to users",
        )
    
    role = crud_role.remove(db, id=role_id)
    return {"message": "Role deleted successfully"}


@router.get("/{role_id}/permissions")
def get_role_permissions(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    current_user: User = Depends(deps.require_permission("role:read")),
) -> Any:
    """
    获取角色的权限列表
    """
    role = crud_role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    permissions = [
        {
            "id": perm.id,
            "name": perm.name,
            "code": perm.code,
            "description": perm.description
        }
        for perm in role.permissions
    ]

    return permissions


@router.post("/{role_id}/permissions/{permission_id}")
def assign_permission_to_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    permission_id: int,
    current_user: User = Depends(deps.require_permission("role:assign_permission")),
) -> Any:
    """
    为角色分配权限
    """
    role = crud_role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    permission = crud_permission.get(db, id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    if permission not in role.permissions:
        role.permissions.append(permission)
        db.commit()

    return {"message": "Permission assigned to role successfully"}


@router.delete("/{role_id}/permissions/{permission_id}")
def remove_permission_from_role(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    permission_id: int,
    current_user: User = Depends(deps.require_permission("role:assign_permission")),
) -> Any:
    """
    从角色中移除权限
    """
    role = crud_role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )
    
    permission = crud_permission.get(db, id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )
    
    if permission in role.permissions:
        role.permissions.remove(permission)
        db.commit()
    
    return {"message": "Permission removed from role successfully"}


from pydantic import BaseModel

class PermissionAssignment(BaseModel):
    permission_ids: List[int]

@router.put("/{role_id}/permissions")
def update_role_permissions(
    *,
    db: Session = Depends(get_db),
    role_id: int,
    assignment: PermissionAssignment,
    current_user: User = Depends(deps.require_permission("role:assign_permission")),
) -> Any:
    """
    更新角色的权限列表
    """
    role = crud_role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )
    
    # 获取所有指定的权限
    permissions = []
    for permission_id in assignment.permission_ids:
        permission = crud_permission.get(db, id=permission_id)
        if permission:
            permissions.append(permission)
    
    # 更新角色的权限列表
    role.permissions = permissions
    db.commit()
    
    return {"message": "Role permissions updated successfully"}



