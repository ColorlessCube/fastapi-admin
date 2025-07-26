from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.system_config import SystemConfig
from app.schemas.system_config import SystemConfigCreate, SystemConfigUpdate
import json


class CRUDSystemConfig(CRUDBase[SystemConfig, SystemConfigCreate, SystemConfigUpdate]):
    def get_by_key(self, db: Session, *, key: str) -> Optional[SystemConfig]:
        """根据配置键获取配置"""
        return db.query(SystemConfig).filter(SystemConfig.key == key).first()

    def get_active_configs(self, db: Session) -> List[SystemConfig]:
        """获取所有启用的配置"""
        return db.query(SystemConfig).filter(SystemConfig.is_active == True).all()

    def get_config_value(self, db: Session, *, key: str, default: Any = None) -> Any:
        """获取配置值，并根据数据类型进行转换"""
        config = self.get_by_key(db, key=key)
        if not config or not config.is_active:
            return default
        
        if config.data_type == "integer":
            try:
                return int(config.value)
            except (ValueError, TypeError):
                return default
        elif config.data_type == "boolean":
            return config.value.lower() in ("true", "1", "yes", "on")
        elif config.data_type == "json":
            try:
                return json.loads(config.value)
            except (json.JSONDecodeError, TypeError):
                return default
        else:
            return config.value

    def set_config_value(self, db: Session, *, key: str, value: Any, description: str = None, data_type: str = "string") -> SystemConfig:
        """设置配置值"""
        config = self.get_by_key(db, key=key)
        
        # 根据数据类型转换值
        if data_type == "json":
            value_str = json.dumps(value) if not isinstance(value, str) else value
        else:
            value_str = str(value)
        
        if config:
            # 更新现有配置
            update_data = {"value": value_str}
            if description is not None:
                update_data["description"] = description
            if data_type != config.data_type:
                update_data["data_type"] = data_type
            return self.update(db, db_obj=config, obj_in=update_data)
        else:
            # 创建新配置
            create_data = SystemConfigCreate(
                key=key,
                value=value_str,
                description=description,
                data_type=data_type
            )
            return self.create(db, obj_in=create_data)

    def get_configs_dict(self, db: Session) -> Dict[str, Any]:
        """获取所有启用配置的字典形式"""
        configs = self.get_active_configs(db)
        result = {}
        for config in configs:
            result[config.key] = self.get_config_value(db, key=config.key)
        return result

    def delete_if_not_system(self, db: Session, *, id: int) -> bool:
        """删除非系统配置"""
        config = self.get(db, id=id)
        if config and not config.is_system:
            self.remove(db, id=id)
            return True
        return False


crud_system_config = CRUDSystemConfig(SystemConfig)
