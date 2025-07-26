from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class SystemConfig(Base):
    __tablename__ = "system_configs"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False, comment="配置键")
    value = Column(Text, nullable=True, comment="配置值")
    description = Column(Text, nullable=True, comment="配置描述")
    data_type = Column(String(50), default="string", comment="数据类型: string, integer, boolean, json")
    is_active = Column(Boolean, default=True, comment="是否启用")
    is_system = Column(Boolean, default=False, comment="是否为系统配置(系统配置不可删除)")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<SystemConfig(key='{self.key}', value='{self.value}')>"
