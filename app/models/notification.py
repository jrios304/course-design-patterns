"""
Modelo de dominio para Notificación
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class NotificationType(Enum):
    """Tipos de notificaciones soportados"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationStatus(Enum):
    """Estados de una notificación"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


@dataclass
class Notification:
    """
    Clase que representa una notificación en el sistema.

    Attributes:
        id: Identificador único de la notificación
        user_id: ID del usuario destinatario
        notification_type: Tipo de notificación (EMAIL, SMS, PUSH)
        title: Título de la notificación
        message: Mensaje de la notificación
        status: Estado de la notificación
        created_at: Fecha y hora de creación
        sent_at: Fecha y hora de envío
    """
    user_id: int
    notification_type: NotificationType
    title: str
    message: str
    id: Optional[int] = None
    status: NotificationStatus = NotificationStatus.PENDING
    created_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None

    def __post_init__(self):
        """Inicialización posterior"""
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self) -> dict:
        """Convierte la notificación a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'notification_type': self.notification_type.value,
            'title': self.title,
            'message': self.message,
            'status': self.status.value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }

    @staticmethod
    def from_dict(data: dict) -> 'Notification':
        """Crea una notificación desde un diccionario"""
        return Notification(
            id=data.get('id'),
            user_id=data.get('user_id'),
            notification_type=NotificationType(data.get('notification_type', 'email')),
            title=data.get('title'),
            message=data.get('message'),
            status=NotificationStatus(data.get('status', 'pending')),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            sent_at=datetime.fromisoformat(data['sent_at']) if data.get('sent_at') else None
        )

    def mark_as_sent(self):
        """Marca la notificación como enviada"""
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.now()

    def mark_as_failed(self):
        """Marca la notificación como fallida"""
        self.status = NotificationStatus.FAILED
