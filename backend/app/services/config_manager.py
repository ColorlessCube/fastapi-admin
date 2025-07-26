"""
系统配置管理服务
用于周期性读取和缓存系统配置
"""
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud.system_config import crud_system_config

logger = logging.getLogger(__name__)


class ConfigManager:
    """系统配置管理器"""
    
    def __init__(self, refresh_interval: int = 60):
        """
        初始化配置管理器
        
        Args:
            refresh_interval: 配置刷新间隔(秒)，默认60秒
        """
        self.refresh_interval = refresh_interval
        self._configs: Dict[str, Any] = {}
        self._last_refresh: Optional[datetime] = None
        self._refresh_task: Optional[asyncio.Task] = None
        self._running = False
    
    async def start(self):
        """启动配置管理器"""
        if self._running:
            return
        
        self._running = True
        logger.info("Starting config manager...")
        
        # 立即加载一次配置
        await self.refresh_configs()
        
        # 启动定期刷新任务
        self._refresh_task = asyncio.create_task(self._refresh_loop())
        logger.info(f"Config manager started with refresh interval: {self.refresh_interval}s")
    
    async def stop(self):
        """停止配置管理器"""
        if not self._running:
            return
        
        self._running = False
        logger.info("Stopping config manager...")
        
        if self._refresh_task:
            self._refresh_task.cancel()
            try:
                await self._refresh_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Config manager stopped")
    
    async def _refresh_loop(self):
        """配置刷新循环"""
        while self._running:
            try:
                await asyncio.sleep(self.refresh_interval)
                if self._running:
                    await self.refresh_configs()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in config refresh loop: {e}")
    
    async def refresh_configs(self):
        """刷新配置"""
        try:
            db = SessionLocal()
            try:
                configs_dict = crud_system_config.get_configs_dict(db)
                self._configs = configs_dict
                self._last_refresh = datetime.now()
                logger.debug(f"Refreshed {len(configs_dict)} configs")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error refreshing configs: {e}")
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        return self._configs.get(key, default)
    
    def get_all_configs(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._configs.copy()
    
    def is_maintenance_mode(self) -> bool:
        """检查是否为维护模式"""
        return self.get_config("system.maintenance_mode", False)
    
    def get_session_timeout(self) -> int:
        """获取会话超时时间"""
        return self.get_config("auth.session_timeout", 3600)
    
    def get_max_login_attempts(self) -> int:
        """获取最大登录尝试次数"""
        return self.get_config("auth.max_login_attempts", 5)
    
    def get_default_theme(self) -> str:
        """获取默认主题"""
        return self.get_config("ui.theme", "light")
    
    def get_default_language(self) -> str:
        """获取默认语言"""
        return self.get_config("ui.language", "zh-CN")
    
    def is_email_notification_enabled(self) -> bool:
        """检查邮件通知是否启用"""
        return self.get_config("notification.email_enabled", False)
    
    def get_password_policy(self) -> Dict[str, Any]:
        """获取密码策略"""
        default_policy = {
            "min_length": 6,
            "require_uppercase": False,
            "require_lowercase": False,
            "require_numbers": False,
            "require_symbols": False
        }
        return self.get_config("security.password_policy", default_policy)
    
    @property
    def last_refresh(self) -> Optional[datetime]:
        """获取最后刷新时间"""
        return self._last_refresh
    
    @property
    def is_running(self) -> bool:
        """检查管理器是否运行中"""
        return self._running


# 全局配置管理器实例
config_manager = ConfigManager()


async def get_config_manager() -> ConfigManager:
    """获取配置管理器实例"""
    return config_manager


def get_config_sync(key: str, default: Any = None) -> Any:
    """
    同步获取配置值
    
    Args:
        key: 配置键
        default: 默认值
        
    Returns:
        配置值或默认值
    """
    return config_manager.get_config(key, default)


# 便捷函数
def is_maintenance_mode() -> bool:
    """检查是否为维护模式"""
    return config_manager.is_maintenance_mode()


def get_session_timeout() -> int:
    """获取会话超时时间"""
    return config_manager.get_session_timeout()


def get_max_login_attempts() -> int:
    """获取最大登录尝试次数"""
    return config_manager.get_max_login_attempts()


def get_default_theme() -> str:
    """获取默认主题"""
    return config_manager.get_default_theme()


def get_default_language() -> str:
    """获取默认语言"""
    return config_manager.get_default_language()


def is_email_notification_enabled() -> bool:
    """检查邮件通知是否启用"""
    return config_manager.is_email_notification_enabled()


def get_password_policy() -> Dict[str, Any]:
    """获取密码策略"""
    return config_manager.get_password_policy()
