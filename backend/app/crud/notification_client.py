"""
通知客户端 CRUD 操作
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.notification_client import NotificationClient
from app.schemas.notification_client import NotificationClientCreate, NotificationClientUpdate


class CRUDNotificationClient(CRUDBase[NotificationClient, NotificationClientCreate, NotificationClientUpdate]):
    """通知客户端 CRUD 操作类"""
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[NotificationClient]:
        """根据名称获取通知客户端"""
        return db.query(NotificationClient).filter(NotificationClient.name == name).first()
    
    def get_by_type(self, db: Session, *, type: str, skip: int = 0, limit: int = 100) -> List[NotificationClient]:
        """根据类型获取通知客户端列表"""
        return (
            db.query(NotificationClient)
            .filter(NotificationClient.type == type)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_enabled(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[NotificationClient]:
        """获取启用的通知客户端列表"""
        return (
            db.query(NotificationClient)
            .filter(NotificationClient.enabled == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_scenario(self, db: Session, *, scenario: str) -> List[NotificationClient]:
        """根据推送场景获取启用的通知客户端"""
        return (
            db.query(NotificationClient)
            .filter(
                and_(
                    NotificationClient.enabled == True,
                    NotificationClient.switches.op('->')(scenario).astext.cast(db.Boolean) == True
                )
            )
            .all()
        )
    
    def search(
        self, 
        db: Session, 
        *, 
        keyword: Optional[str] = None,
        type: Optional[str] = None,
        enabled: Optional[bool] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[NotificationClient]:
        """搜索通知客户端"""
        query = db.query(NotificationClient)
        
        # 关键词搜索
        if keyword:
            query = query.filter(
                or_(
                    NotificationClient.name.contains(keyword),
                    NotificationClient.type.contains(keyword)
                )
            )
        
        # 类型过滤
        if type:
            query = query.filter(NotificationClient.type == type)
        
        # 启用状态过滤
        if enabled is not None:
            query = query.filter(NotificationClient.enabled == enabled)
        
        return query.offset(skip).limit(limit).all()
    
    def count_search(
        self,
        db: Session,
        *,
        keyword: Optional[str] = None,
        type: Optional[str] = None,
        enabled: Optional[bool] = None
    ) -> int:
        """搜索结果计数"""
        query = db.query(NotificationClient)
        
        # 关键词搜索
        if keyword:
            query = query.filter(
                or_(
                    NotificationClient.name.contains(keyword),
                    NotificationClient.type.contains(keyword)
                )
            )
        
        # 类型过滤
        if type:
            query = query.filter(NotificationClient.type == type)
        
        # 启用状态过滤
        if enabled is not None:
            query = query.filter(NotificationClient.enabled == enabled)
        
        return query.count()
    
    def update_switches(
        self, 
        db: Session, 
        *, 
        db_obj: NotificationClient, 
        switches: Dict[str, bool]
    ) -> NotificationClient:
        """更新推送场景开关"""
        # 合并现有开关配置
        current_switches = db_obj.switches or {}
        current_switches.update(switches)
        
        return self.update(db, db_obj=db_obj, obj_in={"switches": current_switches})
    
    def toggle_enabled(self, db: Session, *, db_obj: NotificationClient) -> NotificationClient:
        """切换启用状态"""
        return self.update(db, db_obj=db_obj, obj_in={"enabled": not db_obj.enabled})
    
    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """获取统计信息"""
        total = db.query(NotificationClient).count()
        enabled = db.query(NotificationClient).filter(NotificationClient.enabled == True).count()
        
        # 按类型统计
        type_stats = {}
        types = db.query(NotificationClient.type).distinct().all()
        for (type_name,) in types:
            count = db.query(NotificationClient).filter(NotificationClient.type == type_name).count()
            enabled_count = db.query(NotificationClient).filter(
                and_(
                    NotificationClient.type == type_name,
                    NotificationClient.enabled == True
                )
            ).count()
            type_stats[type_name] = {
                "total": count,
                "enabled": enabled_count
            }
        
        return {
            "total": total,
            "enabled": enabled,
            "disabled": total - enabled,
            "by_type": type_stats
        }


notification_client = CRUDNotificationClient(NotificationClient)
