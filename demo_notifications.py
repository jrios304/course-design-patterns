"""
Script de demostración del Sistema de Notificaciones.

Este script demuestra cómo funcionan los patrones de diseño implementados:
- Observer Pattern: FavoriteService notifica a NotificationService
- Strategy Pattern: Diferentes formas de enviar notificaciones
- Factory Pattern: Creación de estrategias de notificación
- Singleton Pattern: Una única instancia de la base de datos
- Repository Pattern: Abstracción del acceso a datos
"""

from app.services.favorite_service import FavoriteService
from app.services.notification_service import NotificationService
from app.models.notification import NotificationType


def print_separator(title: str):
    """Imprime un separador visual"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_observer_pattern():
    """
    Demuestra el patrón Observer.

    El FavoriteService (Subject) notifica al NotificationService (Observer)
    cuando se agrega un favorito.
    """
    print_separator("DEMO: Patrón Observer")

    # Crear el Subject (FavoriteService)
    favorite_service = FavoriteService()

    # Crear el Observer (NotificationService)
    notification_service = NotificationService()

    # Suscribir el observer al subject
    favorite_service.attach(notification_service)
    print(f"✅ Observer attached. Total observers: {favorite_service.get_observers_count()}\n")

    # Agregar un favorito - esto notificará automáticamente
    print("📝 Adding favorite...")
    favorite_service.add_favorite(
        user_id=1,
        product_id=101,
        product_name="Laptop Dell XPS 15"
    )

    print("\n✨ El observer fue notificado automáticamente!")


def demo_strategy_pattern():
    """
    Demuestra el patrón Strategy.

    El NotificationService puede usar diferentes estrategias para enviar
    notificaciones sin cambiar su código.
    """
    print_separator("DEMO: Patrón Strategy")

    from app.models.notification import Notification

    notification_service = NotificationService()

    # Crear una notificación
    notification = Notification(
        user_id=2,
        notification_type=NotificationType.EMAIL,
        title="Oferta Especial",
        message="¡50% de descuento en tu producto favorito!"
    )

    # Enviar usando diferentes estrategias
    print("📧 Enviando por EMAIL, SMS y PUSH...\n")
    notification_service.send_notification(
        notification,
        notification_types=[
            NotificationType.EMAIL,
            NotificationType.SMS,
            NotificationType.PUSH
        ]
    )


def demo_factory_pattern():
    """
    Demuestra el patrón Factory.

    El Factory crea las estrategias apropiadas basándose en el tipo.
    """
    print_separator("DEMO: Patrón Factory")

    from app.factories.notification_factory import NotificationFactory

    factory = NotificationFactory()

    # Mostrar tipos soportados
    print("📋 Tipos de notificación soportados:")
    for notif_type in factory.get_supported_types():
        print(f"   - {notif_type.value}")

    print("\n🏭 Creando estrategias con el Factory...\n")

    # Crear diferentes estrategias
    email_strategy = factory.create_strategy(NotificationType.EMAIL)
    sms_strategy = factory.create_strategy(NotificationType.SMS)
    push_strategy = factory.create_strategy(NotificationType.PUSH)

    print(f"✅ Creada: {email_strategy.get_strategy_name()}")
    print(f"✅ Creada: {sms_strategy.get_strategy_name()}")
    print(f"✅ Creada: {push_strategy.get_strategy_name()}")


def demo_repository_pattern():
    """
    Demuestra el patrón Repository.

    El repository abstrae el acceso a datos.
    """
    print_separator("DEMO: Patrón Repository")

    from app.repositories.notification_repository import NotificationRepository
    from app.models.notification import Notification

    repo = NotificationRepository()

    # Crear y guardar notificación
    notification = Notification(
        user_id=3,
        notification_type=NotificationType.EMAIL,
        title="Bienvenida",
        message="Gracias por registrarte"
    )

    print("💾 Guardando notificación en el repository...")
    saved = repo.save(notification)
    print(f"✅ Guardada con ID: {saved.id}")

    # Buscar por usuario
    print(f"\n🔍 Buscando notificaciones del usuario 3...")
    user_notifications = repo.find_by_user(3)
    print(f"✅ Encontradas {len(user_notifications)} notificaciones")

    for notif in user_notifications:
        print(f"   - {notif.title}: {notif.message}")


def demo_singleton_pattern():
    """
    Demuestra el patrón Singleton.

    La base de datos tiene una única instancia compartida.
    """
    print_separator("DEMO: Patrón Singleton")

    from app.utils.database import DatabaseConnection

    print("🔨 Creando múltiples instancias de DatabaseConnection...\n")

    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    db3 = DatabaseConnection()

    print(f"db1 ID: {id(db1)}")
    print(f"db2 ID: {id(db2)}")
    print(f"db3 ID: {id(db3)}")

    if db1 is db2 is db3:
        print("\n✅ ¡Todas las instancias son la misma (Singleton)!")
    else:
        print("\n❌ Error: Las instancias son diferentes")


def demo_complete_flow():
    """
    Demuestra el flujo completo del sistema.

    Combina todos los patrones en un caso de uso real.
    """
    print_separator("DEMO: Flujo Completo del Sistema")

    print("🎯 Caso de uso: Usuario agrega producto a favoritos\n")

    # 1. Crear servicios
    print("1️⃣  Inicializando servicios...")
    favorite_service = FavoriteService()
    notification_service = NotificationService(
        default_strategies=[NotificationType.EMAIL, NotificationType.PUSH]
    )

    # 2. Configurar Observer
    print("2️⃣  Configurando patrón Observer...")
    favorite_service.attach(notification_service)

    # 3. Simular acción del usuario
    print("3️⃣  Usuario agrega producto a favoritos...\n")
    favorite_service.add_favorite(
        user_id=100,
        product_id=999,
        product_name="iPhone 15 Pro Max"
    )

    # 4. Consultar notificaciones
    print("\n4️⃣  Consultando notificaciones del usuario...")
    notifications = notification_service.get_user_notifications(100)
    print(f"✅ Usuario tiene {len(notifications)} notificaciones")

    for notif in notifications:
        print(f"\n   📬 {notif.title}")
        print(f"      {notif.message}")
        print(f"      Estado: {notif.status.value}")
        print(f"      Tipo: {notif.notification_type.value}")


def main():
    """Función principal que ejecuta todas las demos"""
    print("\n" + "🚀" * 35)
    print("  SISTEMA DE NOTIFICACIONES - DEMOSTRACIÓN DE PATRONES")
    print("🚀" * 35)

    demos = [
        ("Observer Pattern", demo_observer_pattern),
        ("Strategy Pattern", demo_strategy_pattern),
        ("Factory Pattern", demo_factory_pattern),
        ("Repository Pattern", demo_repository_pattern),
        ("Singleton Pattern", demo_singleton_pattern),
        ("Flujo Completo", demo_complete_flow),
    ]

    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Error en demo {name}: {e}")
            import traceback
            traceback.print_exc()

        if i < len(demos):
            input("\n⏸️  Presiona ENTER para continuar a la siguiente demo...")

    print_separator("FIN DE LA DEMOSTRACIÓN")
    print("✅ Todos los patrones de diseño han sido demostrados exitosamente!")
    print("\nPatrones implementados:")
    print("  ✓ Observer Pattern (Subject/Observer)")
    print("  ✓ Strategy Pattern (NotificationStrategy)")
    print("  ✓ Factory Pattern (NotificationFactory)")
    print("  ✓ Repository Pattern (BaseRepository)")
    print("  ✓ Singleton Pattern (DatabaseConnection)")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
