from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SystemConfigBase(BaseModel):
    key: str = Field(..., description="配置键", max_length=255)
    value: Optional[str] = Field(None, description="配置值")
    description: Optional[str] = Field(None, description="配置描述")
    data_type: str = Field("string", description="数据类型")
    is_active: bool = Field(True, description="是否启用")


class SystemConfigCreate(SystemConfigBase):
    pass


class SystemConfigUpdate(BaseModel):
    value: Optional[str] = Field(None, description="配置值")
    description: Optional[str] = Field(None, description="配置描述")
    data_type: Optional[str] = Field(None, description="数据类型")
    is_active: Optional[bool] = Field(None, description="是否启用")


class SystemConfigInDBBase(SystemConfigBase):
    id: int
    is_system: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SystemConfig(SystemConfigInDBBase):
    pass


class SystemConfigInDB(SystemConfigInDBBase):
    pass
