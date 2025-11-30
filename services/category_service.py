"""
Servicio de categorías.
Implementa el patrón Service Layer para separar la lógica de negocio.
Utiliza el patrón Factory para crear repositorios.
"""
from typing import List, Dict, Optional
from utils.repositories import CategoryRepository
from utils.repository_factory import RepositoryFactory


class CategoryService:
    """Servicio que encapsula la lógica de negocio de categorías."""
    
    def __init__(self, repository: CategoryRepository = None):
        # Usa Factory Pattern para crear el repositorio si no se proporciona uno
        self.repository = repository or RepositoryFactory.create_category_repository()
    
    def get_all_categories(self) -> List[Dict]:
        """Obtiene todas las categorías."""
        return self.repository.get_all()
    
    def get_category_by_id(self, category_id: int) -> Optional[Dict]:
        """Obtiene una categoría por su ID."""
        return self.repository.get_by_id(category_id)
    
    def create_category(self, category_data: Dict) -> Dict:
        """Crea una nueva categoría."""
        # Validaciones de negocio
        name = category_data.get('name', '').strip()
        if not name:
            raise ValueError('Category name is required')
        
        # Verificar si ya existe
        if self.repository.get_by_name(name):
            raise ValueError('Category already exists')
        
        return self.repository.add({'name': name})
    
    def delete_category(self, name: str) -> bool:
        """Elimina una categoría por su nombre."""
        if not name or not name.strip():
            raise ValueError('Category name is required')
        
        category = self.repository.get_by_name(name.strip())
        if not category:
            return False
        
        return self.repository.delete_by_name(name.strip())

