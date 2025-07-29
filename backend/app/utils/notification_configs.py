"""
通知配置定义
"""
from typing import Dict, List, Any


class NotificationFieldType:
    """字段类型常量"""
    TEXT = "text"
    PASSWORD = "password"
    SELECT = "select"
    SWITCH = "switch"
    NUMBER = "number"
    TEXTAREA = "textarea"
    URL = "url"


class NotificationField:
    """通知配置字段定义"""
    
    def __init__(
        self,
        key: str,
        label: str,
        field_type: str,
        required: bool = False,
        default: Any = None,
        placeholder: str = "",
        help_text: str = "",
        options: List[Dict[str, Any]] = None,
        validation: Dict[str, Any] = None
    ):
        self.key = key
        self.label = label
        self.field_type = field_type
        self.required = required
        self.default = default
        self.placeholder = placeholder
        self.help_text = help_text
        self.options = options or []
        self.validation = validation or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "key": self.key,
            "label": self.label,
            "type": self.field_type,
            "required": self.required,
            "default": self.default,
            "placeholder": self.placeholder,
            "helpText": self.help_text,
            "options": self.options,
            "validation": self.validation
        }


class NotificationTypeConfig:
    """通知类型配置定义"""
    
    def __init__(
        self,
        type_key: str,
        name: str,
        description: str,
        icon: str,
        fields: List[NotificationField],
        supports_interactive: bool = False
    ):
        self.type_key = type_key
        self.name = name
        self.description = description
        self.icon = icon
        self.fields = fields
        self.supports_interactive = supports_interactive
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "typeKey": self.type_key,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "fields": [field.to_dict() for field in self.fields],
            "supportsInteractive": self.supports_interactive
        }


# 通知类型配置定义
NOTIFICATION_CONFIGS = {
    "wechat_work": NotificationTypeConfig(
        type_key="wechat_work",
        name="企业微信",
        description="通过企业微信机器人发送通知",
        icon="wechat",
        supports_interactive=True,
        fields=[
            NotificationField(
                key="webhook_url",
                label="Webhook URL",
                field_type=NotificationFieldType.URL,
                required=True,
                placeholder="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
                help_text="企业微信机器人的 Webhook 地址"
            ),
            NotificationField(
                key="mentioned_list",
                label="@成员列表",
                field_type=NotificationFieldType.TEXTAREA,
                placeholder="user1,user2",
                help_text="需要@的成员userid，多个用逗号分隔"
            ),
            NotificationField(
                key="mentioned_mobile_list",
                label="@手机号列表",
                field_type=NotificationFieldType.TEXTAREA,
                placeholder="13800138000,13900139000",
                help_text="需要@的成员手机号，多个用逗号分隔"
            )
        ]
    ),
    
    "telegram": NotificationTypeConfig(
        type_key="telegram",
        name="Telegram",
        description="通过 Telegram Bot 发送通知",
        icon="telegram",
        supports_interactive=True,
        fields=[
            NotificationField(
                key="bot_token",
                label="Bot Token",
                field_type=NotificationFieldType.PASSWORD,
                required=True,
                placeholder="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
                help_text="从 @BotFather 获取的 Bot Token"
            ),
            NotificationField(
                key="chat_id",
                label="Chat ID",
                field_type=NotificationFieldType.TEXT,
                required=True,
                placeholder="-1001234567890",
                help_text="目标聊天的 Chat ID"
            ),
            NotificationField(
                key="parse_mode",
                label="解析模式",
                field_type=NotificationFieldType.SELECT,
                default="Markdown",
                options=[
                    {"label": "Markdown", "value": "Markdown"},
                    {"label": "HTML", "value": "HTML"},
                    {"label": "无", "value": ""}
                ],
                help_text="消息格式解析模式"
            ),
            NotificationField(
                key="disable_web_page_preview",
                label="禁用网页预览",
                field_type=NotificationFieldType.SWITCH,
                default=False,
                help_text="是否禁用链接的网页预览"
            )
        ]
    ),
    
    "email": NotificationTypeConfig(
        type_key="email",
        name="邮件",
        description="通过 SMTP 发送邮件通知",
        icon="email",
        supports_interactive=False,
        fields=[
            NotificationField(
                key="smtp_server",
                label="SMTP 服务器",
                field_type=NotificationFieldType.TEXT,
                required=True,
                placeholder="smtp.gmail.com",
                help_text="SMTP 服务器地址"
            ),
            NotificationField(
                key="smtp_port",
                label="SMTP 端口",
                field_type=NotificationFieldType.NUMBER,
                required=True,
                default=587,
                help_text="SMTP 服务器端口"
            ),
            NotificationField(
                key="username",
                label="用户名",
                field_type=NotificationFieldType.TEXT,
                required=True,
                placeholder="your-email@gmail.com",
                help_text="SMTP 认证用户名"
            ),
            NotificationField(
                key="password",
                label="密码",
                field_type=NotificationFieldType.PASSWORD,
                required=True,
                help_text="SMTP 认证密码或应用专用密码"
            ),
            NotificationField(
                key="from_email",
                label="发件人邮箱",
                field_type=NotificationFieldType.TEXT,
                required=True,
                placeholder="noreply@yourcompany.com",
                help_text="发件人邮箱地址"
            ),
            NotificationField(
                key="to_emails",
                label="收件人邮箱",
                field_type=NotificationFieldType.TEXTAREA,
                required=True,
                placeholder="user1@example.com,user2@example.com",
                help_text="收件人邮箱地址，多个用逗号分隔"
            ),
            NotificationField(
                key="use_tls",
                label="使用 TLS",
                field_type=NotificationFieldType.SWITCH,
                default=True,
                help_text="是否使用 TLS 加密连接"
            )
        ]
    ),
    
    "webhook": NotificationTypeConfig(
        type_key="webhook",
        name="Webhook",
        description="通过 HTTP POST 发送通知到自定义端点",
        icon="webhook",
        supports_interactive=False,
        fields=[
            NotificationField(
                key="url",
                label="Webhook URL",
                field_type=NotificationFieldType.URL,
                required=True,
                placeholder="https://your-api.com/webhook",
                help_text="接收通知的 Webhook 地址"
            ),
            NotificationField(
                key="method",
                label="HTTP 方法",
                field_type=NotificationFieldType.SELECT,
                default="POST",
                options=[
                    {"label": "POST", "value": "POST"},
                    {"label": "PUT", "value": "PUT"},
                    {"label": "PATCH", "value": "PATCH"}
                ],
                help_text="HTTP 请求方法"
            ),
            NotificationField(
                key="headers",
                label="请求头",
                field_type=NotificationFieldType.TEXTAREA,
                placeholder='{"Authorization": "Bearer token", "Content-Type": "application/json"}',
                help_text="自定义请求头，JSON 格式"
            ),
            NotificationField(
                key="timeout",
                label="超时时间(秒)",
                field_type=NotificationFieldType.NUMBER,
                default=30,
                validation={"min": 1, "max": 300},
                help_text="请求超时时间"
            ),
            NotificationField(
                key="verify_ssl",
                label="验证 SSL 证书",
                field_type=NotificationFieldType.SWITCH,
                default=True,
                help_text="是否验证 SSL 证书"
            )
        ]
    )
}


def get_notification_types() -> List[Dict[str, Any]]:
    """获取所有通知类型配置"""
    return [config.to_dict() for config in NOTIFICATION_CONFIGS.values()]


def get_notification_type_config(type_key: str) -> Dict[str, Any]:
    """获取指定类型的配置"""
    config = NOTIFICATION_CONFIGS.get(type_key)
    if not config:
        raise ValueError(f"Unknown notification type: {type_key}")
    return config.to_dict()


def validate_notification_config(type_key: str, config_data: Dict[str, Any]) -> Dict[str, str]:
    """验证通知配置数据"""
    errors = {}
    
    if type_key not in NOTIFICATION_CONFIGS:
        errors["type"] = f"Unknown notification type: {type_key}"
        return errors
    
    type_config = NOTIFICATION_CONFIGS[type_key]
    
    for field in type_config.fields:
        value = config_data.get(field.key)
        
        # 检查必填字段
        if field.required and (value is None or value == ""):
            errors[field.key] = f"{field.label} is required"
            continue
        
        # 跳过空值的验证
        if value is None or value == "":
            continue
        
        # 数字类型验证
        if field.field_type == NotificationFieldType.NUMBER:
            try:
                num_value = float(value)
                if "min" in field.validation and num_value < field.validation["min"]:
                    errors[field.key] = f"{field.label} must be at least {field.validation['min']}"
                if "max" in field.validation and num_value > field.validation["max"]:
                    errors[field.key] = f"{field.label} must be at most {field.validation['max']}"
            except (ValueError, TypeError):
                errors[field.key] = f"{field.label} must be a valid number"
        
        # URL 类型验证
        if field.field_type == NotificationFieldType.URL:
            if not str(value).startswith(("http://", "https://")):
                errors[field.key] = f"{field.label} must be a valid URL"
    
    return errors


# 推送场景配置
NOTIFICATION_SCENARIOS = {
    "user_login": {
        "key": "user_login",
        "name": "用户登录",
        "description": "用户登录系统时发送通知",
        "default": False
    },
    "user_created": {
        "key": "user_created", 
        "name": "用户创建",
        "description": "创建新用户时发送通知",
        "default": True
    },
    "role_changed": {
        "key": "role_changed",
        "name": "角色变更",
        "description": "用户角色发生变更时发送通知", 
        "default": True
    },
    "system_error": {
        "key": "system_error",
        "name": "系统错误",
        "description": "系统发生错误时发送通知",
        "default": True
    },
    "config_changed": {
        "key": "config_changed",
        "name": "配置变更",
        "description": "系统配置发生变更时发送通知",
        "default": False
    },
    "security_alert": {
        "key": "security_alert",
        "name": "安全警报",
        "description": "检测到安全威胁时发送通知",
        "default": True
    }
}


def get_notification_scenarios() -> List[Dict[str, Any]]:
    """获取所有推送场景配置"""
    return list(NOTIFICATION_SCENARIOS.values())
