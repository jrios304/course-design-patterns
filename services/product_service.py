"""
Servicio de productos.
Implementa el patrón Service Layer para separar la lógica de negocio.
Utiliza el patrón Factory para crear repositorios.
"""
from typing import List, Dict, Optional
from utils.repositories import ProductRepository
from utils.repository_factory import RepositoryFactory


class ProductService:
    """Servicio que encapsula la lógica de negocio de productos."""
    
    def __init__(self, repository: ProductRepository = None):
        # Usa Factory Pattern para crear el repositorio si no se proporciona uno
        self.repository = repository or RepositoryFactory.create_product_repository()
    
    def get_all_products(self) -> List[Dict]:
        """Obtiene todos los productos."""
        return self.repository.get_all()
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Obtiene un producto por su ID."""
        return self.repository.get_by_id(product_id)
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """Obtiene productos filtrados por categoría."""
        return self.repository.get_by_category(category)
    
    def create_product(self, product_data: Dict) -> Dict:
        """Crea un nuevo producto."""
        # Validaciones de negocio
        if not product_data.get('name'):
            raise ValueError('Product name is required')
        if not product_data.get('category'):
            raise ValueError('Product category is required')
        if product_data.get('price') is None or product_data.get('price') < 0:
            raise ValueError('Product price must be a positive number')
        
        return self.repository.add(product_data)
    
    def update_product(self, product_id: int, product_data: Dict) -> Optional[Dict]:
        """Actualiza un producto existente."""
        return self.repository.update(product_id, product_data)
    
    def delete_product(self, product_id: int) -> bool:
        """Elimina un producto."""
        return self.repository.delete(product_id)

