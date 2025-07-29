from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.models.user import User
from app.services.config_manager import config_manager

router = APIRouter()


@router.get("/")
def read_system_configs(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词（配置键、配置值）"),
    data_type: Optional[str] = Query(None, description="数据类型筛选"),
    is_active: Optional[bool] = Query(None, description="状态筛选"),
    current_user: User = Depends(deps.require_permission("system:config_read")),
) -> Any:
    """
    获取系统配置列表（支持搜索和筛选）
    """
    configs, total = crud.crud_system_config.get_multi_with_search(
        db,
        skip=skip,
        limit=limit,
        keyword=keyword,
        data_type=data_type,
        is_active=is_active
    )

    # 转换为字典格式以便序列化
    configs_data = []
    for config in configs:
        config_dict = {
            "id": config.id,
            "key": config.key,
            "value": config.value,
            "description": config.description,
            "data_type": config.data_type,
            "is_active": config.is_active,
            "is_system": config.is_system,
            "created_at": config.created_at,
            "updated_at": config.updated_at
        }
        configs_data.append(config_dict)

    return {
        "data": configs_data,
        "total": total,
        "skip": skip,
        "limit": limit
    }


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


@router.get("/statistics")
def get_system_config_statistics(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_permission("system:config_read")),
) -> Any:
    """
    获取系统配置统计信息
    """
    stats = crud.crud_system_config.get_statistics(db)
    return stats


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



