"""
Pruebas unitarias para NotificationFactory.

Valida el patrón Factory.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.factories.notification_factory import NotificationFactory
from app.models.notification import NotificationType
from app.strategies.notification_strategy import (
    EmailNotificationStrategy,
    SMSNotificationStrategy,
    PushNotificationStrategy
)


class TestNotificationFactory(unittest.TestCase):
    """Suite de pruebas para NotificationFactory"""

    def test_create_email_strategy(self):
        """Verifica que el factory crea EmailStrategy"""
        strategy = NotificationFactory.create_strategy(NotificationType.EMAIL)

        self.assertIsInstance(strategy, EmailNotificationStrategy)

    def test_create_sms_strategy(self):
        """Verifica que el factory crea SMSStrategy"""
        strategy = NotificationFactory.create_strategy(NotificationType.SMS)

        self.assertIsInstance(strategy, SMSNotificationStrategy)

    def test_create_push_strategy(self):
        """Verifica que el factory crea PushStrategy"""
        strategy = NotificationFactory.create_strategy(NotificationType.PUSH)

        self.assertIsInstance(strategy, PushNotificationStrategy)

    def test_create_strategy_with_invalid_type(self):
        """Verifica que lanza error con tipo inválido"""
        # Crear un tipo falso que no está en el enum
        class FakeType:
            pass

        with self.assertRaises((ValueError, KeyError)):
            NotificationFactory.create_strategy(FakeType())

    def test_create_email_strategy_with_config(self):
        """Verifica que el factory pasa configuración a la estrategia"""
        config = {
            'smtp_config': {
                'host': 'custom.smtp.com',
                'port': 587
            }
        }

        strategy = NotificationFactory.create_strategy(
            NotificationType.EMAIL,
            config
        )

        self.assertIsInstance(strategy, EmailNotificationStrategy)
        self.assertEqual(strategy.smtp_config['host'], 'custom.smtp.com')

    def test_create_sms_strategy_with_config(self):
        """Verifica que el factory configura SMS provider"""
        config = {'sms_provider': 'CustomProvider'}

        strategy = NotificationFactory.create_strategy(
            NotificationType.SMS,
            config
        )

        self.assertEqual(strategy.sms_provider, 'CustomProvider')

    def test_create_push_strategy_with_config(self):
        """Verifica que el factory configura Push service"""
        config = {'push_service': 'CustomService'}

        strategy = NotificationFactory.create_strategy(
            NotificationType.PUSH,
            config
        )

        self.assertEqual(strategy.push_service, 'CustomService')

    def test_get_supported_types(self):
        """Verifica que retorna los tipos soportados"""
        types = NotificationFactory.get_supported_types()

        self.assertIn(NotificationType.EMAIL, types)
        self.assertIn(NotificationType.SMS, types)
        self.assertIn(NotificationType.PUSH, types)
        self.assertEqual(len(types), 3)

    def test_create_log_strategy(self):
        """Verifica que puede crear estrategia de logging"""
        from app.strategies.notification_strategy import LogNotificationStrategy

        strategy = NotificationFactory.create_log_strategy()

        self.assertIsInstance(strategy, LogNotificationStrategy)


if __name__ == '__main__':
    unittest.main()
