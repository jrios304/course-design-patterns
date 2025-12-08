"""
Controller para gestionar notificaciones (Presentation Layer).
"""
from flask import request
from flask_restful import Resource, reqparse
from app.services.notification_service import NotificationService
from app.models.notification import NotificationType, NotificationStatus


def is_valid_token(token):
    """Valida el token de autenticación (simplificado)"""
    return token == 'abcd1234' or token == 'abcd12345'


class NotificationController(Resource):
    """
    Controller para endpoints de notificaciones.

    Endpoints:
        GET /notifications - Obtiene notificaciones del usuario
        POST /notifications/send - Envía una notificación manual
    """

    def __init__(self):
        """Inicializa el controller"""
        self.notification_service = NotificationService()
        self.parser = reqparse.RequestParser()

    def get(self):
        """
        Obtiene las notificaciones de un usuario.

        Query params:
            user_id: ID del usuario (requerido)
            status: Filtro por estado (opcional)

        Returns:
            Lista de notificaciones
        """
        # Validar autenticación
        token = request.headers.get('Authorization')
        if not token or not is_valid_token(token):
            return {'message': 'Unauthorized'}, 401

        # Obtener parámetros
        user_id = request.args.get('user_id', type=int)
        status = request.args.get('status')

        if not user_id:
            return {'message': 'user_id is required'}, 400

        # Convertir status a enum si se proporciona
        notification_status = None
        if status:
            try:
                notification_status = NotificationStatus(status)
            except ValueError:
                return {'message': f'Invalid status: {status}'}, 400

        # Obtener notificaciones
        notifications = self.notification_service.get_user_notifications(
            user_id,
            notification_status
        )

        return {
            'count': len(notifications),
            'notifications': [n.to_dict() for n in notifications]
        }, 200

    def post(self):
        """
        Envía una notificación manual.

        Body:
            user_id: ID del usuario
            type: Tipo de notificación (email, sms, push)
            title: Título de la notificación
            message: Mensaje

        Returns:
            Confirmación de envío
        """
        # Validar autenticación
        token = request.headers.get('Authorization')
        if not token or not is_valid_token(token):
            return {'message': 'Unauthorized'}, 401

        # Parsear argumentos
        self.parser.add_argument('user_id', type=int, required=True, help='User ID')
        self.parser.add_argument('type', type=str, required=True, help='Notification type')
        self.parser.add_argument('title', type=str, required=True, help='Title')
        self.parser.add_argument('message', type=str, required=True, help='Message')

        args = self.parser.parse_args()

        # Validar tipo de notificación
        try:
            notif_type = NotificationType(args['type'])
        except ValueError:
            return {
                'message': f"Invalid notification type: {args['type']}",
                'valid_types': [t.value for t in NotificationType]
            }, 400

        # Crear y enviar notificación
        from app.models.notification import Notification

        notification = Notification(
            user_id=args['user_id'],
            notification_type=notif_type,
            title=args['title'],
            message=args['message']
        )

        success = self.notification_service.send_notification(notification)

        if success:
            return {
                'message': 'Notification sent successfully',
                'notification': notification.to_dict()
            }, 201
        else:
            return {'message': 'Failed to send notification'}, 500


class NotificationPendingController(Resource):
    """
    Controller para notificaciones pendientes.
    """

    def __init__(self):
        """Inicializa el controller"""
        self.notification_service = NotificationService()

    def get(self):
        """
        Obtiene todas las notificaciones pendientes.

        Returns:
            Lista de notificaciones pendientes
        """
        # Validar autenticación
        token = request.headers.get('Authorization')
        if not token or not is_valid_token(token):
            return {'message': 'Unauthorized'}, 401

        pending = self.notification_service.get_pending_notifications()

        return {
            'count': len(pending),
            'notifications': [n.to_dict() for n in pending]
        }, 200

    def post(self):
        """
        Reintenta enviar notificaciones fallidas.

        Returns:
            Número de notificaciones reenviadas
        """
        # Validar autenticación
        token = request.headers.get('Authorization')
        if not token or not is_valid_token(token):
            return {'message': 'Unauthorized'}, 401

        retry_count = self.notification_service.retry_failed_notifications()

        return {
            'message': f'Retried {retry_count} failed notifications',
            'retried': retry_count
        }, 200
