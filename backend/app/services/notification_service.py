"""
通知发送服务
"""
import json
import time
import asyncio
import aiohttp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

from app.utils.notification_configs import NOTIFICATION_CONFIGS


class NotificationSender:
    """通知发送器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    async def send(self, title: str, content: str, extra_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """发送通知"""
        raise NotImplementedError
    
    async def test_connection(self) -> Tuple[bool, str]:
        """测试连接"""
        return await self.send("测试通知", "这是一条测试消息")


class WeChatWorkSender(NotificationSender):
    """企业微信通知发送器"""
    
    async def send(self, title: str, content: str, extra_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        webhook_url = self.config.get("webhook_url")
        if not webhook_url:
            return False, "Webhook URL 未配置"
        
        # 构建消息内容
        message = f"**{title}**\n\n{content}"
        
        # 构建请求数据
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": message
            }
        }
        
        # 添加@成员
        mentioned_list = self.config.get("mentioned_list", "").strip()
        mentioned_mobile_list = self.config.get("mentioned_mobile_list", "").strip()
        
        if mentioned_list or mentioned_mobile_list:
            data["markdown"]["mentioned_list"] = mentioned_list.split(",") if mentioned_list else []
            data["markdown"]["mentioned_mobile_list"] = mentioned_mobile_list.split(",") if mentioned_mobile_list else []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=data, timeout=30) as response:
                    result = await response.json()
                    if result.get("errcode") == 0:
                        return True, "发送成功"
                    else:
                        return False, f"发送失败: {result.get('errmsg', '未知错误')}"
        except Exception as e:
            return False, f"发送异常: {str(e)}"


class TelegramSender(NotificationSender):
    """Telegram 通知发送器"""
    
    async def send(self, title: str, content: str, extra_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        bot_token = self.config.get("bot_token")
        chat_id = self.config.get("chat_id")
        
        if not bot_token or not chat_id:
            return False, "Bot Token 或 Chat ID 未配置"
        
        # 构建消息内容
        message = f"*{title}*\n\n{content}"
        
        # 构建请求数据
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": self.config.get("parse_mode", "Markdown"),
            "disable_web_page_preview": self.config.get("disable_web_page_preview", False)
        }
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, timeout=30) as response:
                    result = await response.json()
                    if result.get("ok"):
                        return True, "发送成功"
                    else:
                        return False, f"发送失败: {result.get('description', '未知错误')}"
        except Exception as e:
            return False, f"发送异常: {str(e)}"


class EmailSender(NotificationSender):
    """邮件通知发送器"""
    
    async def send(self, title: str, content: str, extra_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        smtp_server = self.config.get("smtp_server")
        smtp_port = self.config.get("smtp_port", 587)
        username = self.config.get("username")
        password = self.config.get("password")
        from_email = self.config.get("from_email")
        to_emails = self.config.get("to_emails", "")
        use_tls = self.config.get("use_tls", True)
        
        if not all([smtp_server, username, password, from_email, to_emails]):
            return False, "邮件配置不完整"
        
        to_email_list = [email.strip() for email in to_emails.split(",") if email.strip()]
        if not to_email_list:
            return False, "收件人邮箱列表为空"
        
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ", ".join(to_email_list)
            msg['Subject'] = title
            
            # 添加邮件内容
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # 发送邮件
            server = smtplib.SMTP(smtp_server, smtp_port)
            if use_tls:
                server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
            return True, f"邮件已发送到 {len(to_email_list)} 个收件人"
        except Exception as e:
            return False, f"发送异常: {str(e)}"


class WebhookSender(NotificationSender):
    """Webhook 通知发送器"""
    
    async def send(self, title: str, content: str, extra_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        url = self.config.get("url")
        method = self.config.get("method", "POST").upper()
        headers_str = self.config.get("headers", "{}")
        timeout = self.config.get("timeout", 30)
        verify_ssl = self.config.get("verify_ssl", True)
        
        if not url:
            return False, "Webhook URL 未配置"
        
        try:
            # 解析请求头
            headers = json.loads(headers_str) if headers_str else {}
            headers.setdefault("Content-Type", "application/json")
            
            # 构建请求数据
            data = {
                "title": title,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "extra_data": extra_data or {}
            }
            
            connector = aiohttp.TCPConnector(verify_ssl=verify_ssl)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.request(
                    method, url, json=data, headers=headers, timeout=timeout
                ) as response:
                    if 200 <= response.status < 300:
                        return True, f"发送成功 (HTTP {response.status})"
                    else:
                        return False, f"发送失败 (HTTP {response.status})"
        except json.JSONDecodeError:
            return False, "请求头格式错误，必须是有效的 JSON"
        except Exception as e:
            return False, f"发送异常: {str(e)}"


# 发送器映射
SENDER_MAP = {
    "wechat_work": WeChatWorkSender,
    "telegram": TelegramSender,
    "email": EmailSender,
    "webhook": WebhookSender
}


class NotificationService:
    """通知服务"""
    
    @staticmethod
    def create_sender(notification_type: str, config: Dict[str, Any]) -> NotificationSender:
        """创建通知发送器"""
        sender_class = SENDER_MAP.get(notification_type)
        if not sender_class:
            raise ValueError(f"Unsupported notification type: {notification_type}")
        return sender_class(config)
    
    @staticmethod
    async def test_notification(notification_type: str, config: Dict[str, Any], message: str = "测试消息") -> Tuple[bool, str, float]:
        """测试通知发送"""
        start_time = time.time()
        try:
            sender = NotificationService.create_sender(notification_type, config)
            success, msg = await sender.send("测试通知", message)
            duration = time.time() - start_time
            return success, msg, duration
        except Exception as e:
            duration = time.time() - start_time
            return False, f"测试异常: {str(e)}", duration
    
    @staticmethod
    async def send_notification(
        notification_type: str, 
        config: Dict[str, Any], 
        title: str, 
        content: str,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str]:
        """发送通知"""
        try:
            sender = NotificationService.create_sender(notification_type, config)
            return await sender.send(title, content, extra_data)
        except Exception as e:
            return False, f"发送异常: {str(e)}"
    
    @staticmethod
    async def send_to_multiple(
        clients: List[Dict[str, Any]], 
        title: str, 
        content: str,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """发送到多个客户端"""
        results = []
        
        # 创建发送任务
        tasks = []
        for client in clients:
            task = NotificationService.send_notification(
                client["type"], 
                client["config"], 
                title, 
                content, 
                extra_data
            )
            tasks.append((client, task))
        
        # 并发执行
        for client, task in tasks:
            try:
                success, message = await task
                results.append({
                    "client_id": client.get("id"),
                    "client_name": client.get("name"),
                    "success": success,
                    "message": message
                })
            except Exception as e:
                results.append({
                    "client_id": client.get("id"),
                    "client_name": client.get("name"),
                    "success": False,
                    "message": f"发送异常: {str(e)}"
                })
        
        return results


# 全局通知服务实例
notification_service = NotificationService()
