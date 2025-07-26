"""
认证相关 API
"""
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.crud.user import user as crud_user
from app.schemas.auth import LoginRequest, LoginResponse, Token
from app.schemas.user import User

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login_for_access_token(
    request: Request,
    db: Session = Depends(get_db),
    form_data: LoginRequest = None
) -> Any:
    """
    用户登录获取访问令牌
    """
    user = crud_user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not crud_user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # 获取客户端IP地址
    client_ip = request.client.host if request.client else None
    if hasattr(request, 'headers'):
        # 检查是否有代理转发的真实IP
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            client_ip = forwarded_for.split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            client_ip = request.headers.get('X-Real-IP')

    # 更新登录信息
    crud_user.update_login_info(db, user=user, ip_address=client_ip)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "preferred_language": user.preferred_language,
            "timezone": user.timezone,
            "last_login_at": user.last_login_at,
            "login_count": user.login_count
        }
    )


@router.post("/login/test-token", response_model=User)
def test_token(current_user: User = Depends(deps.get_current_user)) -> Any:
    """
    测试访问令牌
    """
    return current_user


@router.get("/me/permissions")
def read_user_permissions(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    获取当前用户的权限列表
    """
    # 获取用户详细信息（包含角色和权限）
    user_with_roles = crud_user.get_with_roles(db, id=current_user.id)

    # 收集所有权限
    permissions = []
    permission_codes = set()  # 用于去重

    if user_with_roles and user_with_roles.roles:
        for role in user_with_roles.roles:
            if role.permissions:
                for permission in role.permissions:
                    if permission.code not in permission_codes:
                        permissions.append({
                            "id": permission.id,
                            "name": permission.name,
                            "code": permission.code,
                            "resource": permission.resource,
                            "action": permission.action
                        })
                        permission_codes.add(permission.code)

    return {
        "user_id": current_user.id,
        "permissions": permissions
    }
