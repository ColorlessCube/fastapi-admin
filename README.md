# FastAPI Admin

🚀 一个基于 FastAPI + Vue 3 的现代化企业级管理系统框架，提供完整的 RBAC 权限控制、系统配置管理、国际化支持等企业级功能。

## ✨ 项目特色

- 🔐 **完整的 RBAC 权限系统** - 用户、角色、权限三级权限控制
- ⚙️ **动态系统配置管理** - 支持运行时配置修改，无需重启服务
- 🌍 **国际化支持** - 内置中英文切换，支持用户个性化语言偏好
- 📊 **实时系统监控** - 系统状态、用户活动、登录统计等
- 🎨 **现代化 UI 设计** - 基于 Element Plus 的响应式界面
- 🔄 **自动数据库迁移** - 基于 Alembic 的版本化数据库管理
- 📝 **自动 API 文档** - Swagger/OpenAPI 自动生成文档
- 🛡️ **安全性保障** - JWT 认证、密码加密、登录追踪

## 🛠️ 技术栈

### 后端技术
- **FastAPI 0.115.13** - 现代、高性能的 Web 框架
- **SQLAlchemy 2.0.36** - Python SQL 工具包和 ORM
- **Alembic 1.14.0** - 数据库迁移工具
- **SQLite** - 轻量级数据库（可扩展至 PostgreSQL/MySQL）
- **JWT** - JSON Web Token 认证
- **Pydantic 2.10.3** - 数据验证和设置管理
- **Uvicorn 0.32.1** - ASGI 服务器
- **Passlib** - 密码哈希和验证
- **Python-Jose** - JWT 处理

### 前端技术
- **Vue 3.4.0** - 渐进式 JavaScript 框架
- **Element Plus 2.4.0** - Vue 3 企业级 UI 组件库
- **Vue Router 4.2.0** - 官方路由管理器
- **Vue I18n 9.14.5** - 国际化解决方案
- **Axios 1.6.0** - HTTP 客户端
- **Vite 5.0.0** - 下一代前端构建工具

## 📁 项目结构

```
fastapi-admin/
├── backend/                    # 后端服务
│   ├── app/                   # 主应用目录
│   │   ├── api/              # API 路由模块
│   │   │   ├── auth.py       # 认证相关 API
│   │   │   ├── users.py      # 用户管理 API
│   │   │   ├── roles.py      # 角色管理 API
│   │   │   ├── permissions.py # 权限管理 API
│   │   │   ├── system_configs.py # 系统配置 API
│   │   │   └── deps.py       # 依赖注入
│   │   ├── core/             # 核心配置
│   │   │   ├── config.py     # 应用配置
│   │   │   ├── database.py   # 数据库配置
│   │   │   └── security.py   # 安全相关
│   │   ├── models/           # SQLAlchemy 数据模型
│   │   │   ├── user.py       # 用户模型
│   │   │   ├── role.py       # 角色模型
│   │   │   ├── permission.py # 权限模型
│   │   │   ├── system_config.py # 系统配置模型
│   │   │   └── base.py       # 基础模型
│   │   ├── schemas/          # Pydantic 数据模式
│   │   │   ├── user.py       # 用户数据模式
│   │   │   ├── role.py       # 角色数据模式
│   │   │   ├── permission.py # 权限数据模式
│   │   │   ├── auth.py       # 认证数据模式
│   │   │   └── system_config.py # 系统配置模式
│   │   ├── crud/             # CRUD 操作层
│   │   │   ├── user.py       # 用户 CRUD
│   │   │   ├── role.py       # 角色 CRUD
│   │   │   ├── permission.py # 权限 CRUD
│   │   │   ├── system_config.py # 系统配置 CRUD
│   │   │   └── base.py       # 基础 CRUD
│   │   ├── services/         # 业务服务层
│   │   │   └── config_manager.py # 配置管理服务
│   │   ├── utils/            # 工具函数
│   │   │   └── pagination.py # 分页工具
│   │   └── main.py           # FastAPI 应用入口
│   ├── alembic/              # 数据库迁移文件
│   ├── alembic.ini           # Alembic 配置
│   ├── requirements.txt      # Python 依赖
│   └── run.py               # 启动脚本
├── frontend/                 # 前端应用
│   ├── src/
│   │   ├── components/       # Vue 组件
│   │   │   └── AdminLayout.vue # 管理布局组件
│   │   ├── views/           # 页面视图
│   │   │   ├── Dashboard.vue # 仪表板
│   │   │   ├── Login.vue     # 登录页面
│   │   │   ├── Users.vue     # 用户管理
│   │   │   ├── Roles.vue     # 角色管理
│   │   │   ├── SystemConfigs.vue # 系统配置
│   │   │   └── Profile.vue   # 用户资料
│   │   ├── router/          # 路由配置
│   │   │   └── index.js     # 路由定义
│   │   ├── api/             # API 调用封装
│   │   │   └── index.js     # API 客户端
│   │   ├── i18n/            # 国际化
│   │   │   └── index.js     # i18n 配置
│   │   ├── locales/         # 语言包
│   │   │   ├── zh-CN.js     # 中文语言包
│   │   │   └── en-US.js     # 英文语言包
│   │   ├── utils/           # 工具函数
│   │   │   ├── permissions.js # 权限工具
│   │   │   └── datetime.js  # 时间工具
│   │   ├── composables/     # Vue 组合式函数
│   │   │   └── useDateTime.js # 时间处理
│   │   ├── App.vue          # 根组件
│   │   └── main.js          # 应用入口
│   ├── package.json         # 前端依赖
│   ├── vite.config.js       # Vite 配置
│   └── index.html           # HTML 模板
├── LICENSE                   # 开源协议
└── README.md                # 项目说明
```

## 🎯 功能特性

### 🔐 认证与授权
- ✅ **JWT 认证系统** - 安全的无状态认证
- ✅ **RBAC 权限控制** - 用户-角色-权限三级权限模型
- ✅ **登录状态追踪** - 记录登录时间、IP地址、登录次数
- ✅ **会话管理** - 支持令牌过期和刷新
- ✅ **权限验证** - 细粒度的 API 权限控制

### 👥 用户管理
- ✅ **用户 CRUD** - 完整的用户增删改查
- ✅ **用户资料管理** - 支持头像、个人信息编辑
- ✅ **用户偏好设置** - 语言、时区等个性化配置
- ✅ **用户状态管理** - 启用/禁用用户账户
- ✅ **批量操作** - 支持批量用户管理

### 🎭 角色与权限
- ✅ **角色管理** - 灵活的角色定义和分配
- ✅ **权限管理** - 基于资源和操作的权限定义
- ✅ **权限继承** - 角色权限的继承机制
- ✅ **动态权限** - 运行时权限检查和验证
- ✅ **权限审计** - 权限变更记录和追踪

### ⚙️ 系统配置
- ✅ **动态配置管理** - 无需重启的配置热更新
- ✅ **配置分类** - 支持不同数据类型的配置项
- ✅ **配置缓存** - 高性能的配置读取机制
- ✅ **配置验证** - 配置值的格式验证
- ✅ **系统配置保护** - 防止误删关键系统配置

### 🌍 国际化与本地化
- ✅ **多语言支持** - 内置中英文，可扩展其他语言
- ✅ **用户语言偏好** - 个人语言设置同步
- ✅ **时区支持** - 用户时区设置和时间显示
- ✅ **动态语言切换** - 无需刷新页面的语言切换

### 📊 系统监控
- ✅ **系统状态监控** - 实时系统运行状态
- ✅ **用户活动统计** - 登录统计、活跃用户分析
- ✅ **性能监控** - 系统运行时间、版本信息
- ✅ **操作日志** - 用户操作记录和审计

### 🎨 用户界面
- ✅ **响应式设计** - 适配桌面和移动设备
- ✅ **现代化 UI** - 基于 Element Plus 的美观界面
- ✅ **主题支持** - 支持明暗主题切换
- ✅ **组件化开发** - 可复用的 Vue 组件
- ✅ **路由守卫** - 基于权限的页面访问控制

### 🔧 开发特性
- ✅ **RESTful API** - 标准化的 API 设计
- ✅ **自动 API 文档** - Swagger/OpenAPI 文档生成
- ✅ **数据库迁移** - Alembic 版本化数据库管理
- ✅ **代码规范** - 完整的类型注解和文档
- ✅ **测试支持** - 内置测试框架和工具

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+
- **Node.js**: 16+
- **npm**: 8+ 或 **yarn**: 1.22+

### 1. 克隆项目

```bash
git clone https://github.com/ColorlessCube/fastapi-admin.git
cd fastapi-admin
```

### 2. 后端设置

#### 安装 Python 依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head

# 或者直接运行应用（会自动创建表）
python run.py
```

#### 启动后端服务

```bash
python run.py
```

后端服务将在 http://localhost:8000 启动

### 3. 前端设置

#### 安装依赖

```bash
cd frontend
npm install
# 或使用 yarn
yarn install
```

#### 启动开发服务器

```bash
npm run dev
# 或使用 yarn
yarn dev
```

前端服务将在 http://localhost:3000 启动

### 4. 访问应用

- **前端应用**: http://localhost:3000
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **ReDoc 文档**: http://localhost:8000/redoc

## 🔑 默认账号

首次启动应用后，系统会自动创建默认管理员账号：

- **用户名**: `admin`
- **密码**: `admin123`
- **角色**: 超级管理员（拥有所有权限）

> ⚠️ **安全提示**: 生产环境中请立即修改默认密码！

## 📚 API 文档

启动后端服务后，可以访问以下地址查看完整的 API 文档：

- **Swagger UI**: http://localhost:8000/docs - 交互式 API 文档
- **ReDoc**: http://localhost:8000/redoc - 美观的 API 文档

## 🔌 API 端点详览

### 🔐 认证模块 (`/api/v1/auth`)
```
POST   /login              # 用户登录
POST   /login/test-token    # 测试访问令牌有效性
```

### 👥 用户管理 (`/api/v1/users`)
```
GET    /                   # 获取用户列表（支持分页、搜索）
POST   /                   # 创建新用户
GET    /me                 # 获取当前用户信息
PUT    /me                 # 更新当前用户信息
PUT    /me/preferences     # 更新用户偏好设置
GET    /{user_id}          # 获取指定用户详情
PUT    /{user_id}          # 更新指定用户信息
DELETE /{user_id}          # 删除用户（软删除）
POST   /{user_id}/roles    # 为用户分配角色
DELETE /{user_id}/roles/{role_id}  # 移除用户角色
```

### 🎭 角色管理 (`/api/v1/roles`)
```
GET    /                   # 获取角色列表
POST   /                   # 创建新角色
GET    /{role_id}          # 获取角色详情
PUT    /{role_id}          # 更新角色信息
DELETE /{role_id}          # 删除角色
GET    /{role_id}/permissions  # 获取角色权限列表
POST   /{role_id}/permissions  # 为角色分配权限
DELETE /{role_id}/permissions/{permission_id}  # 移除角色权限
```

### 🔒 权限管理 (`/api/v1/permissions`)
```
GET    /                   # 获取权限列表
POST   /                   # 创建新权限
GET    /{permission_id}    # 获取权限详情
PUT    /{permission_id}    # 更新权限信息
DELETE /{permission_id}    # 删除权限
```

### ⚙️ 系统配置 (`/api/v1/system-configs`)
```
GET    /                   # 获取配置列表
POST   /                   # 创建新配置
GET    /{config_id}        # 获取配置详情
PUT    /{config_id}        # 更新配置
DELETE /{config_id}        # 删除配置
GET    /key/{config_key}   # 根据键获取配置值
GET    /active/all         # 获取所有启用的配置
```

## 🛠️ 开发指南

### 数据库管理

#### 数据库迁移

```bash
cd backend

# 创建新的迁移文件
alembic revision --autogenerate -m "添加新功能"

# 应用迁移到最新版本
alembic upgrade head

# 回滚到上一个版本
alembic downgrade -1

# 查看迁移历史
alembic history

# 查看当前版本
alembic current
```

#### 重置数据库

```bash
# 删除数据库文件（开发环境）
rm fastapi_admin.db

# 重新运行迁移
alembic upgrade head
```

### 后端开发

#### 添加新的 API 模块

1. **创建数据模型** (`backend/app/models/`)
```python
# models/example.py
from sqlalchemy import Column, String, Text
from .base import BaseModel

class Example(BaseModel):
    __tablename__ = "examples"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
```

2. **定义数据模式** (`backend/app/schemas/`)
```python
# schemas/example.py
from pydantic import BaseModel
from typing import Optional

class ExampleBase(BaseModel):
    name: str
    description: Optional[str] = None

class ExampleCreate(ExampleBase):
    pass

class Example(ExampleBase):
    id: int
    class Config:
        from_attributes = True
```

3. **实现 CRUD 操作** (`backend/app/crud/`)
```python
# crud/example.py
from app.crud.base import CRUDBase
from app.models.example import Example
from app.schemas.example import ExampleCreate, ExampleUpdate

class CRUDExample(CRUDBase[Example, ExampleCreate, ExampleUpdate]):
    pass

example = CRUDExample(Example)
```

4. **创建 API 路由** (`backend/app/api/`)
```python
# api/examples.py
from fastapi import APIRouter, Depends
from app.api import deps
from app.crud.example import example as crud_example

router = APIRouter()

@router.get("/")
def read_examples(db: Session = Depends(deps.get_db)):
    return crud_example.get_multi(db)
```

5. **注册路由** (`backend/app/main.py`)
```python
from app.api import examples
app.include_router(examples.router, prefix=f"{settings.API_V1_STR}/examples", tags=["examples"])
```

### 前端开发

#### 项目结构说明

- **`src/views/`** - 页面组件，对应路由页面
- **`src/components/`** - 可复用的 Vue 组件
- **`src/router/`** - Vue Router 路由配置
- **`src/api/`** - API 调用封装和拦截器
- **`src/utils/`** - 工具函数和辅助方法
- **`src/locales/`** - 国际化语言包

#### 添加新页面

1. **创建页面组件** (`src/views/ExamplePage.vue`)
2. **添加路由配置** (`src/router/index.js`)
3. **添加导航菜单** (在布局组件中)
4. **添加权限控制** (在路由 meta 中定义所需权限)

#### 国际化开发

1. **添加语言键值** (`src/locales/zh-CN.js`, `src/locales/en-US.js`)
2. **在组件中使用** `{{ $t('key') }}` 或 `useI18n()`
3. **动态切换语言** 使用 `setLocale()` 函数

### 权限系统开发

#### 权限定义规范

权限采用 `资源:操作` 的格式，例如：
- `user:read` - 查看用户
- `user:create` - 创建用户
- `role:update` - 更新角色
- `system:config_read` - 读取系统配置

#### 在 API 中使用权限

```python
from app.api import deps

@router.get("/")
def read_users(
    current_user: User = Depends(deps.require_permission("user:read"))
):
    # 需要 user:read 权限才能访问
    pass
```

#### 在前端中使用权限

```javascript
// 在路由中定义权限要求
{
  path: '/users',
  component: Users,
  meta: {
    requiresAuth: true,
    requiredPermission: 'user:read'
  }
}

// 在组件中检查权限
import permissionManager from '@/utils/permissions'

if (permissionManager.hasPermission('user:create')) {
  // 显示创建按钮
}
```

## 🚀 部署指南

### 生产环境部署

#### 1. 环境变量配置

创建 `.env` 文件：

```bash
# 安全配置
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost/fastapi_admin

# CORS 配置
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

#### 2. 使用 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/fastapi_admin
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=fastapi_admin
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

#### 3. 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # 前端静态文件
    location / {
        root /var/www/fastapi-admin;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 性能优化

#### 后端优化

1. **数据库连接池配置**
2. **Redis 缓存集成**
3. **异步任务队列**（Celery）
4. **API 限流**（slowapi）

#### 前端优化

1. **代码分割和懒加载**
2. **静态资源 CDN**
3. **Gzip 压缩**
4. **缓存策略**

## ⚙️ 配置说明

### 后端配置

主要配置文件：`backend/app/core/config.py`

```python
class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "FastAPI Admin"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # 安全配置
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./fastapi_admin.db"

    # CORS 配置
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
```

### 前端配置

主要配置文件：`frontend/vite.config.js`

```javascript
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
```

### 系统配置管理

系统支持动态配置管理，可在运行时修改以下配置：

- **认证配置**: 会话超时、最大登录尝试次数
- **UI 配置**: 默认主题、默认语言
- **通知配置**: 邮件通知开关
- **安全配置**: 密码策略
- **系统配置**: 维护模式开关

## 🧪 测试

### 运行后端测试

```bash
cd backend
pytest
```

### 运行前端测试

```bash
cd frontend
npm run test
```

## 📝 更新日志

### v1.0.0 (2024-01-01)

#### 新功能
- ✨ 完整的 RBAC 权限系统
- ✨ 动态系统配置管理
- ✨ 国际化支持
- ✨ 用户偏好设置
- ✨ 系统监控面板

#### 技术特性
- 🔧 FastAPI + Vue 3 技术栈
- 🔧 JWT 认证系统
- 🔧 SQLAlchemy ORM
- 🔧 Alembic 数据库迁移
- 🔧 Element Plus UI 组件

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork 项目**
2. **创建功能分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **创建 Pull Request**

### 开发规范

- **代码风格**: 遵循 PEP 8 (Python) 和 ESLint (JavaScript)
- **提交信息**: 使用清晰的提交信息
- **测试**: 为新功能添加测试
- **文档**: 更新相关文档

### 报告问题

如果发现 Bug 或有功能建议，请：

1. 检查是否已有相关 Issue
2. 创建新的 Issue，详细描述问题
3. 提供复现步骤和环境信息

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Element Plus](https://element-plus.org/) - Vue 3 UI 组件库
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL 工具包

## 📞 联系方式

- **项目地址**: https://github.com/ColorlessCube/fastapi-admin
- **问题反馈**: https://github.com/ColorlessCube/fastapi-admin/issues
- **讨论交流**: https://github.com/ColorlessCube/fastapi-admin/discussions

---

⭐ 如果这个项目对你有帮助，请给它一个 Star！
