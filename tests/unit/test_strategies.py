"""
Pruebas unitarias para las estrategias de notificación.

Valida el patrón Strategy.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.strategies.notification_strategy import (
    NotificationStrategy,
    EmailNotificationStrategy,
    SMSNotificationStrategy,
    PushNotificationStrategy,
    LogNotificationStrategy
)
from app.models.notification import Notification, NotificationType


class TestNotificationStrategies(unittest.TestCase):
    """Suite de pruebas para las estrategias de notificación"""

    def test_email_strategy_implements_interface(self):
        """Verifica que EmailStrategy implementa la interfaz"""
        strategy = EmailNotificationStrategy()

        self.assertIsInstance(strategy, NotificationStrategy)
        self.assertTrue(hasattr(strategy, 'send'))
        self.assertTrue(hasattr(strategy, 'get_strategy_name'))

    def test_sms_strategy_implements_interface(self):
        """Verifica que SMSStrategy implementa la interfaz"""
        strategy = SMSNotificationStrategy()

        self.assertIsInstance(strategy, NotificationStrategy)
        self.assertTrue(hasattr(strategy, 'send'))

    def test_push_strategy_implements_interface(self):
        """Verifica que PushStrategy implementa la interfaz"""
        strategy = PushNotificationStrategy()

        self.assertIsInstance(strategy, NotificationStrategy)
        self.assertTrue(hasattr(strategy, 'send'))

    def test_email_strategy_send(self):
        """Verifica que EmailStrategy puede enviar"""
        strategy = EmailNotificationStrategy()
        notification = Notification(
            user_id=1,
            notification_type=NotificationType.EMAIL,
            title="Test",
            message="Test message"
        )

        result = strategy.send(notification)

        self.assertTrue(result)

    def test_sms_strategy_send(self):
        """Verifica que SMSStrategy puede enviar"""
        strategy = SMSNotificationStrategy()
        notification = Notification(
            user_id=1,
            notification_type=NotificationType.SMS,
            title="Test",
            message="Test message"
        )

        result = strategy.send(notification)

        self.assertTrue(result)

    def test_push_strategy_send(self):
        """Verifica que PushStrategy puede enviar"""
        strategy = PushNotificationStrategy()
        notification = Notification(
            user_id=1,
            notification_type=NotificationType.PUSH,
            title="Test",
            message="Test message"
        )

        result = strategy.send(notification)

        self.assertTrue(result)

    def test_log_strategy_send(self):
        """Verifica que LogStrategy funciona"""
        strategy = LogNotificationStrategy()
        notification = Notification(
            user_id=1,
            notification_type=NotificationType.EMAIL,
            title="Test",
            message="Test message"
        )

        result = strategy.send(notification)

        self.assertTrue(result)

    def test_strategy_names(self):
        """Verifica que cada estrategia tiene un nombre único"""
        strategies = [
            EmailNotificationStrategy(),
            SMSNotificationStrategy(),
            PushNotificationStrategy(),
            LogNotificationStrategy()
        ]

        names = [s.get_strategy_name() for s in strategies]

        # Verificar que todos los nombres son diferentes
        self.assertEqual(len(names), len(set(names)))

    def test_email_strategy_with_config(self):
        """Verifica que EmailStrategy acepta configuración"""
        config = {
            'host': 'smtp.test.com',
            'port': 465,
            'use_tls': False
        }

        strategy = EmailNotificationStrategy(smtp_config=config)

        self.assertEqual(strategy.smtp_config['host'], 'smtp.test.com')
        self.assertEqual(strategy.smtp_config['port'], 465)

    def test_sms_strategy_with_provider(self):
        """Verifica que SMSStrategy acepta proveedor"""
        strategy = SMSNotificationStrategy(sms_provider="CustomProvider")

        self.assertEqual(strategy.sms_provider, "CustomProvider")

    def test_push_strategy_with_service(self):
        """Verifica que PushStrategy acepta servicio"""
        strategy = PushNotificationStrategy(push_service="CustomService")

        self.assertEqual(strategy.push_service, "CustomService")


if __name__ == '__main__':
    unittest.main()
