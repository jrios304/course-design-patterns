"""
Servicio de notificaciones que implementa el patrón Observer.
Reacciona a eventos del sistema y envía notificaciones.
"""
from typing import List, Dict, Any
from app.observers.subject import Observer, Subject
from app.models.notification import Notification, NotificationType, NotificationStatus
from app.repositories.notification_repository import NotificationRepository
from app.factories.notification_factory import NotificationFactory
from app.strategies.notification_strategy import NotificationStrategy


class NotificationService(Observer):
    """
    Servicio de notificaciones que actúa como Observer.

    Escucha eventos del sistema (como agregar favoritos) y envía notificaciones.
    Combina los patrones Observer, Strategy y Factory.
    """

    def __init__(
        self,
        repository: NotificationRepository = None,
        default_strategies: List[NotificationType] = None
    ):
        """
        Inicializa el servicio de notificaciones.

        Args:
            repository: Repository de notificaciones
            default_strategies: Estrategias de notificación por defecto
        """
        self.repository = repository or NotificationRepository()
        self.default_strategies = default_strategies or [NotificationType.EMAIL]
        self.factory = NotificationFactory()

        # Configuración de estrategias (puede venir de archivo de config)
        self.config: Dict[str, Any] = {
            'smtp_config': {
                'host': 'smtp.gmail.com',
                'port': 587
            },
            'sms_provider': 'Twilio',
            'push_service': 'Firebase'
        }

    def update(self, subject: Subject, event: str, data: Any) -> None:
        """
        Método del Observer. Se llama cuando el Subject notifica un evento.

        Args:
            subject: El subject que generó el evento
            event: Nombre del evento
            data: Datos del evento
        """
        print(f"\n🔔 NotificationService received event: {event}")

        # Manejar diferentes tipos de eventos
        if event == "favorite_added":
            self._handle_favorite_added(data)
        elif event == "product_price_changed":
            self._handle_price_changed(data)
        elif event == "product_back_in_stock":
            self._handle_back_in_stock(data)
        else:
            print(f"⚠️  Unhandled event: {event}")

    def _handle_favorite_added(self, data: Dict[str, Any]) -> None:
        """
        Maneja el evento cuando se agrega un producto a favoritos.

        Args:
            data: Datos del evento (user_id, product_id, product_name)
        """
        user_id = data.get('user_id')
        product_name = data.get('product_name', 'Unknown product')

        notification = Notification(
            user_id=user_id,
            notification_type=NotificationType.EMAIL,
            title="¡Producto agregado a favoritos!",
            message=f"Has agregado '{product_name}' a tus favoritos."
        )

        self.send_notification(notification)

    def _handle_price_changed(self, data: Dict[str, Any]) -> None:
        """
        Maneja el evento cuando cambia el precio de un producto.

        Args:
            data: Datos del evento
        """
        user_id = data.get('user_id')
        product_name = data.get('product_name')
        old_price = data.get('old_price')
        new_price = data.get('new_price')

        notification = Notification(
            user_id=user_id,
            notification_type=NotificationType.PUSH,
            title="¡Cambio de precio!",
            message=f"El precio de '{product_name}' cambió de ${old_price} a ${new_price}"
        )

        self.send_notification(notification)

    def _handle_back_in_stock(self, data: Dict[str, Any]) -> None:
        """
        Maneja el evento cuando un producto vuelve a estar disponible.

        Args:
            data: Datos del evento
        """
        user_id = data.get('user_id')
        product_name = data.get('product_name')

        notification = Notification(
            user_id=user_id,
            notification_type=NotificationType.SMS,
            title="¡Producto disponible!",
            message=f"'{product_name}' está nuevamente en stock."
        )

        self.send_notification(notification)

    def send_notification(
        self,
        notification: Notification,
        notification_types: List[NotificationType] = None
    ) -> bool:
        """
        Envía una notificación usando las estrategias especificadas.

        Args:
            notification: La notificación a enviar
            notification_types: Tipos de notificación a usar

        Returns:
            bool: True si se enviaron todas exitosamente
        """
        # Guardar notificación en la base de datos
        saved_notification = self.repository.save(notification)
        print(f"💾 Notification saved with ID: {saved_notification.id}")

        # Usar estrategias por defecto si no se especifican
        types_to_use = notification_types or self.default_strategies

        success = True
        for notif_type in types_to_use:
            try:
                # Usar el Factory para crear la estrategia apropiada
                strategy = self.factory.create_strategy(notif_type, self.config)

                # Enviar usando la estrategia
                if strategy.send(notification):
                    print(f"✅ Sent via {strategy.get_strategy_name()}")
                else:
                    print(f"❌ Failed to send via {strategy.get_strategy_name()}")
                    success = False

            except Exception as e:
                print(f"❌ Error sending notification via {notif_type}: {e}")
                success = False

        # Actualizar estado en la base de datos
        if success:
            self.repository.mark_as_sent(saved_notification.id)
        else:
            self.repository.mark_as_failed(saved_notification.id)

        return success

    def send_bulk_notifications(
        self,
        notifications: List[Notification]
    ) -> Dict[str, int]:
        """
        Envía múltiples notificaciones.

        Args:
            notifications: Lista de notificaciones

        Returns:
            Diccionario con estadísticas de envío
        """
        stats = {'sent': 0, 'failed': 0}

        for notification in notifications:
            if self.send_notification(notification):
                stats['sent'] += 1
            else:
                stats['failed'] += 1

        return stats

    def get_user_notifications(
        self,
        user_id: int,
        status: NotificationStatus = None
    ) -> List[Notification]:
        """
        Obtiene las notificaciones de un usuario.

        Args:
            user_id: ID del usuario
            status: Filtro por estado (opcional)

        Returns:
            Lista de notificaciones
        """
        notifications = self.repository.find_by_user(user_id)

        if status:
            notifications = [n for n in notifications if n.status == status]

        return notifications

    def get_pending_notifications(self) -> List[Notification]:
        """
        Obtiene todas las notificaciones pendientes.

        Returns:
            Lista de notificaciones pendientes
        """
        return self.repository.find_pending()

    def retry_failed_notifications(self) -> int:
        """
        Reintenta enviar notificaciones fallidas.

        Returns:
            Número de notificaciones reenviadas exitosamente
        """
        failed_notifications = self.repository.find_by_criteria(
            lambda item: item.get('status') == NotificationStatus.FAILED.value
        )

        retry_count = 0
        for notification in failed_notifications:
            if self.send_notification(notification):
                retry_count += 1

        return retry_count
