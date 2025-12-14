"""
Módulo de implementación del patrón Strategy
"""
from .notification_strategy import (
    NotificationStrategy,
    EmailNotificationStrategy,
    SMSNotificationStrategy,
    PushNotificationStrategy,
    LogNotificationStrategy
)

__all__ = [
    'NotificationStrategy',
    'EmailNotificationStrategy',
    'SMSNotificationStrategy',
    'PushNotificationStrategy',
    'LogNotificationStrategy'
]
