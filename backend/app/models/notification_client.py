"""
通知客户端数据模型
"""
from sqlalchemy import Column, String, Text, Boolean, Integer
from sqlalchemy.dialects.sqlite import JSON

from .base import BaseModel


class NotificationClient(BaseModel):
    """
    通知客户端模型
    """
    __tablename__ = "notification_clients"
    
    name = Column(String(100), nullable=False, comment="客户端名称")
    type = Column(String(50), nullable=False, comment="通知类型")
    config = Column(JSON, nullable=True, comment="配置信息(JSON格式)")
    switches = Column(JSON, nullable=True, comment="推送场景开关(JSON格式)")
    enabled = Column(Boolean, default=True, nullable=False, comment="是否启用")
    interactive = Column(Boolean, default=False, nullable=False, comment="是否支持交互")
    
    def __repr__(self):
        return f"<NotificationClient(name='{self.name}', type='{self.type}')>"
