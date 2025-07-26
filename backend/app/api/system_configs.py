from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.models.user import User
from app.services.config_manager import config_manager

router = APIRouter()


@router.get("/", response_model=List[schemas.SystemConfig])
def read_system_configs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.require_permission("system:config_read")),
) -> Any:
    """
    获取系统配置列表
    """
    configs = crud.crud_system_config.get_multi(db, skip=skip, limit=limit)
    return configs


@router.post("/", response_model=schemas.SystemConfig)
def create_system_config(
    *,
    db: Session = Depends(deps.get_db),
    config_in: schemas.SystemConfigCreate,
    current_user: User = Depends(deps.require_permission("system:config_create")),
) -> Any:
    """
    创建系统配置
    """
    # 检查配置键是否已存在
    existing_config = crud.crud_system_config.get_by_key(db, key=config_in.key)
    if existing_config:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="配置键已存在"
        )
    
    config = crud.crud_system_config.create(db, obj_in=config_in)
    return config


@router.put("/{config_id}", response_model=schemas.SystemConfig)
def update_system_config(
    *,
    db: Session = Depends(deps.get_db),
    config_id: int,
    config_in: schemas.SystemConfigUpdate,
    current_user: User = Depends(deps.require_permission("system:config_update")),
) -> Any:
    """
    更新系统配置
    """
    config = crud.crud_system_config.get(db, id=config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置不存在"
        )
    
    config = crud.crud_system_config.update(db, db_obj=config, obj_in=config_in)
    return config


@router.get("/{config_id}", response_model=schemas.SystemConfig)
def read_system_config(
    *,
    db: Session = Depends(deps.get_db),
    config_id: int,
    current_user: User = Depends(deps.require_permission("system:config_read")),
) -> Any:
    """
    获取单个系统配置
    """
    config = crud.crud_system_config.get(db, id=config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置不存在"
        )
    return config


@router.delete("/{config_id}")
def delete_system_config(
    *,
    db: Session = Depends(deps.get_db),
    config_id: int,
    current_user: User = Depends(deps.require_permission("system:config_delete")),
) -> Any:
    """
    删除系统配置
    """
    config = crud.crud_system_config.get(db, id=config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置不存在"
        )
    
    if config.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="系统配置不能删除"
        )
    
    crud.crud_system_config.remove(db, id=config_id)
    return {"message": "配置删除成功"}


@router.get("/key/{config_key}")
def read_config_by_key(
    *,
    db: Session = Depends(deps.get_db),
    config_key: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    根据配置键获取配置值
    """
    value = crud.crud_system_config.get_config_value(db, key=config_key)
    return {"key": config_key, "value": value}


@router.get("/active/all")
def read_active_configs(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取所有启用的配置
    """
    configs_dict = crud.crud_system_config.get_configs_dict(db)
    return configs_dict


@router.get("/manager/status")
def get_config_manager_status(
    current_user: User = Depends(deps.require_permission("system:config_read")),
) -> Any:
    """
    获取配置管理器状态
    """
    return {
        "is_running": config_manager.is_running,
        "last_refresh": config_manager.last_refresh,
        "config_count": len(config_manager.get_all_configs()),
        "maintenance_mode": config_manager.is_maintenance_mode(),
        "session_timeout": config_manager.get_session_timeout(),
        "default_language": config_manager.get_default_language()
    }


@router.post("/manager/refresh")
async def refresh_config_manager(
    current_user: User = Depends(deps.require_permission("system:config_update")),
) -> Any:
    """
    手动刷新配置管理器
    """
    await config_manager.refresh_configs()
    return {"message": "配置刷新成功", "last_refresh": config_manager.last_refresh}
