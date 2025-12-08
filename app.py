from flask import Flask
from flask_restful import Api
from app.controllers.notification_controller import NotificationController, NotificationPendingController

app = Flask(__name__)
api = Api(app)

# Endpoints de notificaciones (nueva arquitectura)
api.add_resource(NotificationController, '/notifications')
api.add_resource(NotificationPendingController, '/notifications/pending')

# TODO: Migrar endpoints legacy a nueva arquitectura:
# - /auth
# - /products
# - /categories
# - /favorites

if __name__ == '__main__':
    print("🚀 API REST con Sistema de Notificaciones")
    print("📡 Endpoints disponibles:")
    print("   GET  /notifications?user_id=<id>")
    print("   POST /notifications")
    print("   GET  /notifications/pending")
    print("   POST /notifications/retry")
    print("\n⚠️  Nota: Los endpoints legacy (/auth, /products, etc.) están pendientes de migración")
    print("💡 Para ver el sistema en acción, ejecuta: python demo_notifications.py\n")
    app.run(debug=True)
