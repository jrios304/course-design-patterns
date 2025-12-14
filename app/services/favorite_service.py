"""
Servicio de favoritos que actúa como Subject en el patrón Observer.
Notifica a los observadores cuando se agregan favoritos.
"""
from typing import List, Dict, Any
from app.observers.subject import Subject
from app.utils.database import DatabaseConnection


class FavoriteService(Subject):
    """
    Servicio de favoritos que extiende Subject.

    Cuando se agregan favoritos, notifica a los observadores (NotificationService).
    Esto demuestra el patrón Observer en acción.
    """

    def __init__(self):
        """Inicializa el servicio"""
        super().__init__()
        self.db = DatabaseConnection()

    def add_favorite(
        self,
        user_id: int,
        product_id: int,
        product_name: str = None
    ) -> Dict[str, Any]:
        """
        Agrega un producto a favoritos y notifica a los observadores.

        Args:
            user_id: ID del usuario
            product_id: ID del producto
            product_name: Nombre del producto (opcional)

        Returns:
            Diccionario con el favorito agregado
        """
        # Crear favorito
        favorite = {
            'user_id': user_id,
            'product_id': product_id
        }

        # Guardar en base de datos
        self.db.add_item('favorites', favorite)
        print(f"❤️  Favorite added: User {user_id}, Product {product_id}")

        # Notificar a los observadores (ej: NotificationService)
        event_data = {
            'user_id': user_id,
            'product_id': product_id,
            'product_name': product_name or f'Product #{product_id}'
        }
        self.notify('favorite_added', event_data)

        return favorite

    def remove_favorite(
        self,
        user_id: int,
        product_id: int
    ) -> bool:
        """
        Elimina un producto de favoritos.

        Args:
            user_id: ID del usuario
            product_id: ID del producto

        Returns:
            True si se eliminó exitosamente
        """
        favorites = self.db.get_data('favorites')
        new_favorites = [
            f for f in favorites
            if not (f['user_id'] == user_id and f['product_id'] == product_id)
        ]

        if len(new_favorites) < len(favorites):
            # Actualizar la base de datos
            self.db.data['favorites'] = new_favorites
            self.db._save_data()
            print(f"💔 Favorite removed: User {user_id}, Product {product_id}")
            return True

        return False

    def get_user_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene los favoritos de un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            Lista de favoritos
        """
        favorites = self.db.get_data('favorites')
        return [f for f in favorites if f.get('user_id') == user_id]

    def is_favorite(self, user_id: int, product_id: int) -> bool:
        """
        Verifica si un producto está en favoritos.

        Args:
            user_id: ID del usuario
            product_id: ID del producto

        Returns:
            True si está en favoritos
        """
        favorites = self.get_user_favorites(user_id)
        return any(f['product_id'] == product_id for f in favorites)
