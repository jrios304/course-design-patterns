"""
Pruebas unitarias para el NotificationService.

Estas pruebas validan:
- Patrón Observer
- Patrón Strategy
- Integración con Repository
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.notification_service import NotificationService
from app.services.favorite_service import FavoriteService
from app.models.notification import Notification, NotificationType, NotificationStatus
from app.repositories.notification_repository import NotificationRepository


class TestNotificationService(unittest.TestCase):
    """Suite de pruebas para NotificationService"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        self.mock_repository = Mock(spec=NotificationRepository)
        self.service = NotificationService(repository=self.mock_repository)

    def test_notification_service_is_observer(self):
        """Verifica que NotificationService implementa la interfaz Observer"""
        from app.observers.subject import Observer

        self.assertIsInstance(self.service, Observer)
        self.assertTrue(hasattr(self.service, 'update'))

    def test_update_handles_favorite_added_event(self):
        """Verifica que el observer maneja el evento favorite_added"""
        # Preparar datos del evento
        event_data = {
            'user_id': 1,
            'product_id': 100,
            'product_name': 'Test Product'
        }

        # Mock del repository
        mock_notification = Notification(
            id=1,
            user_id=1,
            notification_type=NotificationType.EMAIL,
            title="Test",
            message="Test"
        )
        self.mock_repository.save.return_value = mock_notification
        self.mock_repository.mark_as_sent.return_value = True

        # Llamar al update
        with patch.object(self.service, 'send_notification', return_value=True) as mock_send:
            self.service.update(None, 'favorite_added', event_data)

            # Verificar que se llamó send_notification
            mock_send.assert_called_once()

    def test_send_notification_saves_to_repository(self):
        """Verifica que las notificaciones se guardan en el repository"""
        notification = Notification(
            user_id=1,
            notification_type=NotificationType.EMAIL,
            title="Test",
            message="Test message"
        )

        # Mock del repository
        mock_saved = Notification(
            id=1,
            user_id=1,
            notification_type=NotificationType.EMAIL,
            title="Test",
            message="Test message"
        )
        self.mock_repository.save.return_value = mock_saved
        self.mock_repository.mark_as_sent.return_value = True

        # Enviar notificación
        result = self.service.send_notification(notification)

        # Verificar que se guardó
        self.mock_repository.save.assert_called_once()
        self.assertTrue(result)

    def test_send_notification_uses_strategy(self):
        """Verifica que se usa el patrón Strategy para enviar"""
        notification = Notification(
            user_id=1,
            notification_type=NotificationType.EMAIL,
            title="Test",
            message="Test"
        )

        mock_saved = Notification(
            id=1,
            user_id=1,
            notification_type=NotificationType.EMAIL,
            title="Test",
            message="Test"
        )
        self.mock_repository.save.return_value = mock_saved
        self.mock_repository.mark_as_sent.return_value = True

        # Enviar
        result = self.service.send_notification(notification)

        # Verificar que se marcó como enviada
        self.mock_repository.mark_as_sent.assert_called_once_with(1)
        self.assertTrue(result)

    def test_get_user_notifications(self):
        """Verifica que se pueden obtener notificaciones por usuario"""
        user_id = 1
        mock_notifications = [
            Notification(
                id=1,
                user_id=user_id,
                notification_type=NotificationType.EMAIL,
                title="Test 1",
                message="Message 1"
            ),
            Notification(
                id=2,
                user_id=user_id,
                notification_type=NotificationType.SMS,
                title="Test 2",
                message="Message 2"
            )
        ]

        self.mock_repository.find_by_user.return_value = mock_notifications

        # Obtener notificaciones
        notifications = self.service.get_user_notifications(user_id)

        # Verificar
        self.assertEqual(len(notifications), 2)
        self.mock_repository.find_by_user.assert_called_once_with(user_id)

    def test_get_pending_notifications(self):
        """Verifica que se pueden obtener notificaciones pendientes"""
        mock_pending = [
            Notification(
                id=1,
                user_id=1,
                notification_type=NotificationType.EMAIL,
                title="Pending",
                message="Pending message",
                status=NotificationStatus.PENDING
            )
        ]

        self.mock_repository.find_pending.return_value = mock_pending

        # Obtener pendientes
        pending = self.service.get_pending_notifications()

        # Verificar
        self.assertEqual(len(pending), 1)
        self.mock_repository.find_pending.assert_called_once()


class TestFavoriteService(unittest.TestCase):
    """Suite de pruebas para FavoriteService"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        from app.utils.database import DatabaseConnection
        DatabaseConnection.reset_instance()
        self.service = FavoriteService()

    def test_favorite_service_is_subject(self):
        """Verifica que FavoriteService extiende Subject"""
        from app.observers.subject import Subject

        self.assertIsInstance(self.service, Subject)
        self.assertTrue(hasattr(self.service, 'attach'))
        self.assertTrue(hasattr(self.service, 'detach'))
        self.assertTrue(hasattr(self.service, 'notify'))

    def test_attach_observer(self):
        """Verifica que se pueden agregar observers"""
        mock_observer = Mock()

        self.service.attach(mock_observer)

        self.assertEqual(self.service.get_observers_count(), 1)

    def test_add_favorite_notifies_observers(self):
        """Verifica que al agregar favorito se notifica a observers"""
        mock_observer = Mock()
        self.service.attach(mock_observer)

        # Agregar favorito
        self.service.add_favorite(1, 100, "Test Product")

        # Verificar que se notificó
        mock_observer.update.assert_called_once()

        # Verificar los argumentos
        args = mock_observer.update.call_args
        self.assertEqual(args[0][1], 'favorite_added')  # Evento
        self.assertEqual(args[0][2]['user_id'], 1)  # Datos


class TestObserverIntegration(unittest.TestCase):
    """Pruebas de integración del patrón Observer"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        from app.utils.database import DatabaseConnection
        DatabaseConnection.reset_instance()

    def test_observer_pattern_integration(self):
        """Verifica la integración completa del patrón Observer"""
        # Crear subject y observer
        favorite_service = FavoriteService()

        mock_repository = Mock(spec=NotificationRepository)
        mock_notification = Notification(
            id=1,
            user_id=1,
            notification_type=NotificationType.EMAIL,
            title="Test",
            message="Test"
        )
        mock_repository.save.return_value = mock_notification
        mock_repository.mark_as_sent.return_value = True

        notification_service = NotificationService(repository=mock_repository)

        # Suscribir observer
        favorite_service.attach(notification_service)

        # Agregar favorito - esto debe notificar
        favorite_service.add_favorite(1, 100, "Test Product")

        # Verificar que se guardó la notificación
        mock_repository.save.assert_called()


if __name__ == '__main__':
    unittest.main()
