"""
Implementación del patrón Strategy para notificaciones.
Permite cambiar dinámicamente el método de envío de notificaciones.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models.notification import Notification


class NotificationStrategy(ABC):
    """
    Interfaz para estrategias de notificación.
    Define el contrato que todas las estrategias deben cumplir.
    """

    @abstractmethod
    def send(self, notification: Notification) -> bool:
        """
        Envía una notificación usando la estrategia específica.

        Args:
            notification: La notificación a enviar

        Returns:
            bool: True si se envió exitosamente, False en caso contrario
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Retorna el nombre de la estrategia"""
        pass


class EmailNotificationStrategy(NotificationStrategy):
    """
    Estrategia para enviar notificaciones por email.
    """

    def __init__(self, smtp_config: Dict[str, Any] = None):
        """
        Inicializa la estrategia de email.

        Args:
            smtp_config: Configuración del servidor SMTP
        """
        self.smtp_config = smtp_config or {
            'host': 'smtp.gmail.com',
            'port': 587,
            'use_tls': True
        }

    def send(self, notification: Notification) -> bool:
        """
        Envía un email.

        En una implementación real, aquí se conectaría a un servidor SMTP.
        Por ahora, simulamos el envío.
        """
        print(f"📧 [EMAIL] Sending to user {notification.user_id}")
        print(f"   Subject: {notification.title}")
        print(f"   Body: {notification.message}")
        print(f"   SMTP: {self.smtp_config['host']}:{self.smtp_config['port']}")

        # Simulación de envío exitoso
        # En producción:
        # import smtplib
        # server = smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port'])
        # ...
        return True

    def get_strategy_name(self) -> str:
        return "EmailStrategy"


class SMSNotificationStrategy(NotificationStrategy):
    """
    Estrategia para enviar notificaciones por SMS.
    """

    def __init__(self, sms_provider: str = "Twilio"):
        """
        Inicializa la estrategia de SMS.

        Args:
            sms_provider: Proveedor de SMS (Twilio, AWS SNS, etc.)
        """
        self.sms_provider = sms_provider

    def send(self, notification: Notification) -> bool:
        """
        Envía un SMS.

        En una implementación real, aquí se usaría la API de Twilio o similar.
        """
        print(f"📱 [SMS] Sending via {self.sms_provider} to user {notification.user_id}")
        print(f"   Message: {notification.message}")

        # Simulación de envío exitoso
        # En producción con Twilio:
        # from twilio.rest import Client
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(...)
        return True

    def get_strategy_name(self) -> str:
        return "SMSStrategy"


class PushNotificationStrategy(NotificationStrategy):
    """
    Estrategia para enviar notificaciones push.
    """

    def __init__(self, push_service: str = "Firebase"):
        """
        Inicializa la estrategia de push notifications.

        Args:
            push_service: Servicio de push (Firebase, OneSignal, etc.)
        """
        self.push_service = push_service

    def send(self, notification: Notification) -> bool:
        """
        Envía una notificación push.

        En una implementación real, aquí se usaría Firebase Cloud Messaging o similar.
        """
        print(f"🔔 [PUSH] Sending via {self.push_service} to user {notification.user_id}")
        print(f"   Title: {notification.title}")
        print(f"   Body: {notification.message}")

        # Simulación de envío exitoso
        # En producción con Firebase:
        # from firebase_admin import messaging
        # message = messaging.Message(...)
        # messaging.send(message)
        return True

    def get_strategy_name(self) -> str:
        return "PushStrategy"


class LogNotificationStrategy(NotificationStrategy):
    """
    Estrategia para logging de notificaciones (útil para testing).
    """

    def send(self, notification: Notification) -> bool:
        """Simplemente loguea la notificación sin enviarla"""
        print(f"📝 [LOG] Notification for user {notification.user_id}: {notification.message}")
        return True

    def get_strategy_name(self) -> str:
        return "LogStrategy"
