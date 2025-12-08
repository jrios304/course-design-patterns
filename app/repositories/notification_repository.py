"""
Repository para manejar el acceso a datos de notificaciones.
"""
from typing import List
from app.repositories.base_repository import BaseRepository
from app.models.notification import Notification, NotificationStatus


class NotificationRepository(BaseRepository[Notification]):
    """
    Repository para gestionar notificaciones.
    """

    def __init__(self):
        super().__init__('notifications')

    def to_entity(self, data: dict) -> Notification:
        """Convierte diccionario a Notification"""
        return Notification.from_dict(data)

    def to_dict(self, entity: Notification) -> dict:
        """Convierte Notification a diccionario"""
        return entity.to_dict()

    def find_by_user(self, user_id: int) -> List[Notification]:
        """
        Obtiene todas las notificaciones de un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            Lista de notificaciones del usuario
        """
        return self.find_by_criteria(lambda item: item.get('user_id') == user_id)

    def find_pending(self) -> List[Notification]:
        """
        Obtiene todas las notificaciones pendientes.

        Returns:
            Lista de notificaciones pendientes
        """
        return self.find_by_criteria(
            lambda item: item.get('status') == NotificationStatus.PENDING.value
        )

    def mark_as_sent(self, notification_id: int) -> bool:
        """
        Marca una notificación como enviada.

        Args:
            notification_id: ID de la notificación

        Returns:
            True si se actualizó exitosamente
        """
        notification = self.find_by_id(notification_id)
        if notification:
            notification.mark_as_sent()
            return self.update(notification_id, notification) is not None
        return False

    def mark_as_failed(self, notification_id: int) -> bool:
        """
        Marca una notificación como fallida.

        Args:
            notification_id: ID de la notificación

        Returns:
            True si se actualizó exitosamente
        """
        notification = self.find_by_id(notification_id)
        if notification:
            notification.mark_as_failed()
            return self.update(notification_id, notification) is not None
        return False
