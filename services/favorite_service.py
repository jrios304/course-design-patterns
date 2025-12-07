"""
Servicio de favoritos.
Implementa el patrón Service Layer para separar la lógica de negocio.
Utiliza el patrón Factory para crear repositorios.
"""
from typing import List, Dict
from utils.repositories import FavoriteRepository
from utils.repository_factory import RepositoryFactory


class FavoriteService:
    """Servicio que encapsula la lógica de negocio de favoritos."""
    
    def __init__(self, repository: FavoriteRepository = None):
        # Usa Factory Pattern para crear el repositorio si no se proporciona uno
        self.repository = repository or RepositoryFactory.create_favorite_repository()
    
    def get_all_favorites(self) -> List[Dict]:
        """Obtiene todos los favoritos."""
        return self.repository.get_all()
    
    def get_user_favorites(self, user_id: int) -> List[Dict]:
        """Obtiene los favoritos de un usuario."""
        return self.repository.get_by_user(user_id)
    
    def add_favorite(self, favorite_data: Dict) -> Dict:
        """Agrega un producto a favoritos."""
        # Validaciones de negocio
        user_id = favorite_data.get('user_id')
        product_id = favorite_data.get('product_id')
        
        if user_id is None:
            raise ValueError('User ID is required')
        if product_id is None:
            raise ValueError('Product ID is required')
        
        return self.repository.add(favorite_data)
    
    def remove_favorite(self, user_id: int, product_id: int) -> bool:
        """Elimina un producto de favoritos."""
        if user_id is None:
            raise ValueError('User ID is required')
        if product_id is None:
            raise ValueError('Product ID is required')
        
        return self.repository.delete(user_id, product_id)

