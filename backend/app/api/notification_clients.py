"""
通知客户端管理 API
"""
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.core.database import get_db
from app.crud.notification_client import notification_client as crud_notification_client
from app.models.user import User
from app.schemas.notification_client import (
    NotificationClient,
    NotificationClientCreate,
    NotificationClientUpdate,
    NotificationTypeConfig,
    NotificationScenario,
    NotificationTestRequest,
    NotificationTestResponse,
    NotificationSendRequest,
    NotificationSendResponse,
    NotificationConfigValidationResponse
)
from app.utils.notification_configs import (
    get_notification_types,
    get_notification_type_config,
    validate_notification_config,
    get_notification_scenarios
)
from app.services.notification_service import notification_service
# from app.utils.pagination import paginate  # 暂时注释掉，不需要

router = APIRouter()


@router.get("/types", response_model=List[NotificationTypeConfig])
def get_notification_types_api(
    current_user: User = Depends(deps.require_permission("notification:read")),
) -> Any:
    """
    获取所有支持的通知类型配置
    """
    return get_notification_types()


@router.get("/types/{type_key}", response_model=NotificationTypeConfig)
def get_notification_type_config_api(
    type_key: str,
    current_user: User = Depends(deps.require_permission("notification:read")),
) -> Any:
    """
    获取指定通知类型的配置
    """
    try:
        return get_notification_type_config(type_key)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/scenarios", response_model=List[NotificationScenario])
def get_notification_scenarios_api(
    current_user: User = Depends(deps.require_permission("notification:read")),
) -> Any:
    """
    获取所有推送场景配置
    """
    return get_notification_scenarios()


@router.post("/validate-config", response_model=NotificationConfigValidationResponse)
def validate_notification_config_api(
    *,
    type_key: str,
    config_data: dict,
    current_user: User = Depends(deps.require_permission("notification:read")),
) -> Any:
    """
    验证通知配置
    """
    errors = validate_notification_config(type_key, config_data)
    return NotificationConfigValidationResponse(
        valid=len(errors) == 0,
        errors=errors
    )


@router.post("/test", response_model=NotificationTestResponse)
async def test_notification(
    *,
    test_request: NotificationTestRequest,
    current_user: User = Depends(deps.require_permission("notification:test")),
) -> Any:
    """
    测试通知发送
    """
    # 验证配置
    errors = validate_notification_config(test_request.type, test_request.config)
    if errors:
        return NotificationTestResponse(
            success=False,
            message="配置验证失败",
            error="; ".join([f"{k}: {v}" for k, v in errors.items()])
        )
    
    # 执行测试
    success, message, duration = await notification_service.test_notification(
        test_request.type,
        test_request.config,
        test_request.message
    )
    
    return NotificationTestResponse(
        success=success,
        message=message,
        error=None if success else message,
        duration=duration
    )


@router.get("/", response_model=List[NotificationClient])
def read_notification_clients(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    keyword: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    enabled: Optional[bool] = Query(None),
    current_user: User = Depends(deps.require_permission("notification:read")),
) -> Any:
    """
    获取通知客户端列表
    """
    clients = crud_notification_client.search(
        db,
        keyword=keyword,
        type=type,
        enabled=enabled,
        skip=skip,
        limit=limit
    )
    return clients


@router.get("/statistics")
def get_notification_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.require_permission("notification:read")),
) -> Any:
    """
    获取通知客户端统计信息
    """
    return crud_notification_client.get_statistics(db)


@router.post("/", response_model=NotificationClient)
def create_notification_client(
    *,
    db: Session = Depends(get_db),
    client_in: NotificationClientCreate,
    current_user: User = Depends(deps.require_permission("notification:create")),
) -> Any:
    """
    创建通知客户端
    """
    # 检查名称是否已存在
    existing_client = crud_notification_client.get_by_name(db, name=client_in.name)
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="客户端名称已存在"
        )
    
    # 验证配置
    if client_in.config:
        errors = validate_notification_config(client_in.type, client_in.config)
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"配置验证失败: {'; '.join([f'{k}: {v}' for k, v in errors.items()])}"
            )
    
    client = crud_notification_client.create(db, obj_in=client_in)
    return client


@router.get("/{client_id}", response_model=NotificationClient)
def read_notification_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.require_permission("notification:read")),
) -> Any:
    """
    根据 ID 获取通知客户端
    """
    client = crud_notification_client.get(db, id=client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知客户端不存在"
        )
    return client


@router.put("/{client_id}", response_model=NotificationClient)
def update_notification_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    client_in: NotificationClientUpdate,
    current_user: User = Depends(deps.require_permission("notification:update")),
) -> Any:
    """
    更新通知客户端
    """
    client = crud_notification_client.get(db, id=client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知客户端不存在"
        )
    
    # 检查名称冲突
    if client_in.name and client_in.name != client.name:
        existing_client = crud_notification_client.get_by_name(db, name=client_in.name)
        if existing_client:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="客户端名称已存在"
            )
    
    # 验证配置
    if client_in.config:
        notification_type = client_in.type or client.type
        errors = validate_notification_config(notification_type, client_in.config)
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"配置验证失败: {'; '.join([f'{k}: {v}' for k, v in errors.items()])}"
            )
    
    client = crud_notification_client.update(db, db_obj=client, obj_in=client_in)
    return client


@router.delete("/{client_id}")
def delete_notification_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    current_user: User = Depends(deps.require_permission("notification:delete")),
) -> Any:
    """
    删除通知客户端
    """
    client = crud_notification_client.get(db, id=client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知客户端不存在"
        )
    
    crud_notification_client.remove(db, id=client_id)
    return {"message": "通知客户端删除成功"}


@router.post("/{client_id}/toggle")
def toggle_notification_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    current_user: User = Depends(deps.require_permission("notification:update")),
) -> Any:
    """
    切换通知客户端启用状态
    """
    client = crud_notification_client.get(db, id=client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="通知客户端不存在"
        )
    
    client = crud_notification_client.toggle_enabled(db, db_obj=client)
    return {"message": f"通知客户端已{'启用' if client.enabled else '禁用'}"}


@router.post("/send", response_model=NotificationSendResponse)
async def send_notification(
    *,
    db: Session = Depends(get_db),
    send_request: NotificationSendRequest,
    current_user: User = Depends(deps.require_permission("notification:send")),
) -> Any:
    """
    发送通知
    """
    # 获取客户端列表
    clients = []
    for client_id in send_request.client_ids:
        client = crud_notification_client.get(db, id=client_id)
        if client and client.enabled:
            # 检查是否启用了该场景
            if client.switches and client.switches.get(send_request.scenario, False):
                clients.append({
                    "id": client.id,
                    "name": client.name,
                    "type": client.type,
                    "config": client.config
                })
    
    if not clients:
        return NotificationSendResponse(
            total=0,
            success=0,
            failed=0,
            results=[]
        )
    
    # 发送通知
    results = await notification_service.send_to_multiple(
        clients,
        send_request.title,
        send_request.content,
        send_request.extra_data
    )
    
    success_count = sum(1 for r in results if r["success"])
    failed_count = len(results) - success_count
    
    return NotificationSendResponse(
        total=len(results),
        success=success_count,
        failed=failed_count,
        results=results
    )
