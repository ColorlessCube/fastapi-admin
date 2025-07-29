from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
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

    def get_multi_with_search(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        keyword: Optional[str] = None,
        data_type: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[SystemConfig], int]:
        """
        获取系统配置列表（支持搜索和筛选）
        """
        query = db.query(SystemConfig)

        # 关键词搜索
        if keyword:
            search_filter = or_(
                SystemConfig.key.ilike(f"%{keyword}%"),
                SystemConfig.value.ilike(f"%{keyword}%"),
                SystemConfig.description.ilike(f"%{keyword}%")
            )
            query = query.filter(search_filter)

        # 数据类型筛选
        if data_type:
            query = query.filter(SystemConfig.data_type == data_type)

        # 状态筛选
        if is_active is not None:
            query = query.filter(SystemConfig.is_active == is_active)

        # 获取总数
        total = query.count()

        # 分页
        configs = query.offset(skip).limit(limit).all()

        return configs, total

    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """
        获取系统配置统计信息
        """
        total = db.query(SystemConfig).count()
        active = db.query(SystemConfig).filter(SystemConfig.is_active == True).count()
        system = db.query(SystemConfig).filter(SystemConfig.is_system == True).count()

        # 按数据类型统计
        type_stats = db.query(
            SystemConfig.data_type,
            func.count(SystemConfig.id)
        ).group_by(SystemConfig.data_type).all()

        by_type = {data_type: count for data_type, count in type_stats}

        return {
            "total": total,
            "active": active,
            "system": system,
            "by_type": by_type
        }


crud_system_config = CRUDSystemConfig(SystemConfig)
