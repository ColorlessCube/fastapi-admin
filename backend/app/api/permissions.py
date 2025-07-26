"""
权限管理 API
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.database import get_db
from app.crud.permission import permission as crud_permission
from app.models.user import User
from app.schemas.permission import Permission as PermissionSchema, PermissionCreate, PermissionUpdate

router = APIRouter()


@router.get("/", response_model=List[PermissionSchema])
def read_permissions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.require_permission("permission:read")),
) -> Any:
    """
    获取权限列表
    """
    permissions = crud_permission.get_multi(db, skip=skip, limit=limit)
    return permissions


@router.post("/", response_model=PermissionSchema)
def create_permission(
    *,
    db: Session = Depends(get_db),
    permission_in: PermissionCreate,
    current_user: User = Depends(deps.require_permission("permission:create")),
) -> Any:
    """
    创建新权限
    """
    permission = crud_permission.get_by_code(db, code=permission_in.code)
    if permission:
        raise HTTPException(
            status_code=400,
            detail="The permission with this code already exists in the system.",
        )
    permission = crud_permission.create(db, obj_in=permission_in)
    return permission


@router.get("/{permission_id}", response_model=PermissionSchema)
def read_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.require_permission("permission:read")),
) -> Any:
    """
    根据 ID 获取权限
    """
    permission = crud_permission.get(db, id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=404,
            detail="The permission with this id does not exist in the system",
        )
    return permission


@router.put("/{permission_id}", response_model=PermissionSchema)
def update_permission(
    *,
    db: Session = Depends(get_db),
    permission_id: int,
    permission_in: PermissionUpdate,
    current_user: User = Depends(deps.require_permission("permission:update")),
) -> Any:
    """
    更新权限
    """
    permission = crud_permission.get(db, id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=404,
            detail="The permission with this id does not exist in the system",
        )
    permission = crud_permission.update(db, db_obj=permission, obj_in=permission_in)
    return permission


@router.delete("/{permission_id}")
def delete_permission(
    *,
    db: Session = Depends(get_db),
    permission_id: int,
    current_user: User = Depends(deps.require_permission("permission:delete")),
) -> Any:
    """
    删除权限
    """
    permission = crud_permission.get(db, id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=404,
            detail="The permission with this id does not exist in the system",
        )
    
    # 检查是否有角色使用此权限
    if permission.roles:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete permission that is assigned to roles",
        )
    
    permission = crud_permission.remove(db, id=permission_id)
    return {"message": "Permission deleted successfully"}
