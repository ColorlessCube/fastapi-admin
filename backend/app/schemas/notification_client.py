"""
通知客户端相关的 Pydantic 模式
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, validator


class NotificationClientBase(BaseModel):
    """通知客户端基础模式"""
    name: str = Field(..., min_length=1, max_length=100, description="客户端名称")
    type: str = Field(..., min_length=1, max_length=50, description="通知类型")
    config: Optional[Dict[str, Any]] = Field(None, description="配置信息")
    switches: Optional[Dict[str, bool]] = Field(None, description="推送场景开关")
    enabled: bool = Field(True, description="是否启用")
    interactive: bool = Field(False, description="是否支持交互")


class NotificationClientCreate(NotificationClientBase):
    """创建通知客户端模式"""
    
    @validator('config')
    def validate_config(cls, v, values):
        """验证配置信息"""
        if v is None:
            return {}
        
        # 这里可以添加更详细的配置验证逻辑
        # 实际验证会在 API 层使用 notification_configs 模块进行
        return v
    
    @validator('switches')
    def validate_switches(cls, v):
        """验证推送场景开关"""
        if v is None:
            return {}
        return v


class NotificationClientUpdate(BaseModel):
    """更新通知客户端模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="客户端名称")
    type: Optional[str] = Field(None, min_length=1, max_length=50, description="通知类型")
    config: Optional[Dict[str, Any]] = Field(None, description="配置信息")
    switches: Optional[Dict[str, bool]] = Field(None, description="推送场景开关")
    enabled: Optional[bool] = Field(None, description="是否启用")
    interactive: Optional[bool] = Field(None, description="是否支持交互")


class NotificationClientInDBBase(NotificationClientBase):
    """数据库中的通知客户端基础模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NotificationClient(NotificationClientInDBBase):
    """通知客户端响应模式"""
    pass


class NotificationClientWithStatus(NotificationClient):
    """包含状态信息的通知客户端模式"""
    last_test_at: Optional[datetime] = Field(None, description="最后测试时间")
    last_test_result: Optional[bool] = Field(None, description="最后测试结果")
    last_test_error: Optional[str] = Field(None, description="最后测试错误信息")


class NotificationTypeConfig(BaseModel):
    """通知类型配置模式"""
    typeKey: str = Field(..., description="类型键")
    name: str = Field(..., description="类型名称")
    description: str = Field(..., description="类型描述")
    icon: str = Field(..., description="图标")
    fields: List[Dict[str, Any]] = Field(..., description="配置字段")
    supportsInteractive: bool = Field(..., description="是否支持交互")


class NotificationScenario(BaseModel):
    """通知场景模式"""
    key: str = Field(..., description="场景键")
    name: str = Field(..., description="场景名称")
    description: str = Field(..., description="场景描述")
    default: bool = Field(..., description="默认是否启用")


class NotificationTestRequest(BaseModel):
    """通知测试请求模式"""
    type: str = Field(..., description="通知类型")
    config: Dict[str, Any] = Field(..., description="配置信息")
    message: Optional[str] = Field("这是一条测试消息", description="测试消息内容")


class NotificationTestResponse(BaseModel):
    """通知测试响应模式"""
    success: bool = Field(..., description="测试是否成功")
    message: str = Field(..., description="响应消息")
    error: Optional[str] = Field(None, description="错误信息")
    duration: Optional[float] = Field(None, description="耗时(秒)")


class NotificationSendRequest(BaseModel):
    """发送通知请求模式"""
    client_ids: List[int] = Field(..., description="客户端ID列表")
    scenario: str = Field(..., description="推送场景")
    title: str = Field(..., description="通知标题")
    content: str = Field(..., description="通知内容")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="额外数据")


class NotificationSendResponse(BaseModel):
    """发送通知响应模式"""
    total: int = Field(..., description="总数")
    success: int = Field(..., description="成功数")
    failed: int = Field(..., description="失败数")
    results: List[Dict[str, Any]] = Field(..., description="详细结果")


class NotificationConfigValidationResponse(BaseModel):
    """配置验证响应模式"""
    valid: bool = Field(..., description="是否有效")
    errors: Dict[str, str] = Field(..., description="错误信息")
