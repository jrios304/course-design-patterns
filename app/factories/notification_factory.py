"""
Implementación del patrón Factory para crear estrategias de notificación.
Centraliza la lógica de creación de objetos complejos.
"""
from typing import Dict, Any
from app.models.notification import NotificationType
from app.strategies.notification_strategy import (
    NotificationStrategy,
    EmailNotificationStrategy,
    SMSNotificationStrategy,
    PushNotificationStrategy,
    LogNotificationStrategy
)


class NotificationFactory:
    """
    Factory para crear estrategias de notificación.

    Ventajas del patrón Factory:
    1. Encapsula la lógica de creación
    2. Facilita agregar nuevos tipos sin modificar código existente (OCP)
    3. Centraliza la configuración
    """

    # Registro de estrategias disponibles
    _strategies: Dict[NotificationType, type] = {
        NotificationType.EMAIL: EmailNotificationStrategy,
        NotificationType.SMS: SMSNotificationStrategy,
        NotificationType.PUSH: PushNotificationStrategy,
    }

    @classmethod
    def create_strategy(
        cls,
        notification_type: NotificationType,
        config: Dict[str, Any] = None
    ) -> NotificationStrategy:
        """
        Crea una estrategia de notificación basada en el tipo.

        Args:
            notification_type: Tipo de notificación
            config: Configuración opcional para la estrategia

        Returns:
            NotificationStrategy: Instancia de la estrategia correspondiente

        Raises:
            ValueError: Si el tipo de notificación no es soportado

        Example:
            >>> factory = NotificationFactory()
            >>> strategy = factory.create_strategy(NotificationType.EMAIL)
            >>> strategy.send(notification)
        """
        config = config or {}

        if notification_type not in cls._strategies:
            raise ValueError(f"Notification type {notification_type} not supported")

        strategy_class = cls._strategies[notification_type]

        # Crear instancia con configuración específica
        if notification_type == NotificationType.EMAIL:
            return strategy_class(smtp_config=config.get('smtp_config'))
        elif notification_type == NotificationType.SMS:
            return strategy_class(sms_provider=config.get('sms_provider', 'Twilio'))
        elif notification_type == NotificationType.PUSH:
            return strategy_class(push_service=config.get('push_service', 'Firebase'))

        return strategy_class()

    @classmethod
    def register_strategy(
        cls,
        notification_type: NotificationType,
        strategy_class: type
    ) -> None:
        """
        Registra una nueva estrategia de notificación.
        Permite extender el sistema sin modificar el código existente.

        Args:
            notification_type: Tipo de notificación
            strategy_class: Clase de la estrategia

        Example:
            >>> class WhatsAppStrategy(NotificationStrategy):
            ...     pass
            >>> NotificationFactory.register_strategy(
            ...     NotificationType.WHATSAPP,
            ...     WhatsAppStrategy
            ... )
        """
        cls._strategies[notification_type] = strategy_class
        print(f"Registered new strategy: {notification_type.value} -> {strategy_class.__name__}")

    @classmethod
    def get_supported_types(cls) -> list:
        """Retorna la lista de tipos de notificación soportados"""
        return list(cls._strategies.keys())

    @classmethod
    def create_log_strategy(cls) -> NotificationStrategy:
        """
        Crea una estrategia de logging.
        Útil para testing y desarrollo.
        """
        return LogNotificationStrategy()
