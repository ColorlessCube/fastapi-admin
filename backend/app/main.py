"""
FastAPI Admin 主应用
"""
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import json

from app.api import auth, users, roles, permissions, system_configs
from app.core.config import settings
from app.core.database import create_tables
from app.services.config_manager import config_manager





@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    await config_manager.start()
    yield
    # 关闭时
    await config_manager.stop()

# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# 设置 CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 注册路由
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(roles.router, prefix=f"{settings.API_V1_STR}/roles", tags=["roles"])
app.include_router(permissions.router, prefix=f"{settings.API_V1_STR}/permissions", tags=["permissions"])
app.include_router(system_configs.router, prefix=f"{settings.API_V1_STR}/system-configs", tags=["system-configs"])


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    # 创建数据库表
    create_tables()


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to FastAPI Admin",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
