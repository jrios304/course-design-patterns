"""
Factory para creación de repositorios.
Implementa el patrón Factory para centralizar la creación de instancias de repositorios.
"""
from typing import Optional
from utils.repositories import (
    ProductRepository,
    CategoryRepository,
    FavoriteRepository,
    BaseRepository
)


class RepositoryFactory:
    """
    Factory para crear instancias de repositorios.
    Implementa el patrón Factory Pattern.
    """
    
    # Configuración por defecto de archivos
    DEFAULT_DB_FILE = 'db.json'
    DEFAULT_FAVORITES_FILE = 'favorites.json'
    
    # Cache de instancias (Singleton-like para evitar múltiples conexiones)
    _instances = {}
    
    @classmethod
    def create_product_repository(cls, json_file_path: str = None) -> ProductRepository:
        """
        Crea una instancia de ProductRepository.
        
        Args:
            json_file_path: Ruta del archivo JSON (opcional, usa default si no se proporciona)
            
        Returns:
            Instancia de ProductRepository
        """
        key = f'product_{json_file_path or cls.DEFAULT_DB_FILE}'
        if key not in cls._instances:
            cls._instances[key] = ProductRepository(json_file_path or cls.DEFAULT_DB_FILE)
        return cls._instances[key]
    
    @classmethod
    def create_category_repository(cls, json_file_path: str = None) -> CategoryRepository:
        """
        Crea una instancia de CategoryRepository.
        
        Args:
            json_file_path: Ruta del archivo JSON (opcional, usa default si no se proporciona)
            
        Returns:
            Instancia de CategoryRepository
        """
        key = f'category_{json_file_path or cls.DEFAULT_DB_FILE}'
        if key not in cls._instances:
            cls._instances[key] = CategoryRepository(json_file_path or cls.DEFAULT_DB_FILE)
        return cls._instances[key]
    
    @classmethod
    def create_favorite_repository(cls, json_file_path: str = None) -> FavoriteRepository:
        """
        Crea una instancia de FavoriteRepository.
        
        Args:
            json_file_path: Ruta del archivo JSON (opcional, usa default si no se proporciona)
            
        Returns:
            Instancia de FavoriteRepository
        """
        key = f'favorite_{json_file_path or cls.DEFAULT_FAVORITES_FILE}'
        if key not in cls._instances:
            cls._instances[key] = FavoriteRepository(json_file_path or cls.DEFAULT_FAVORITES_FILE)
        return cls._instances[key]
    
    @classmethod
    def create_repository(cls, repository_type: str, json_file_path: str = None) -> Optional[BaseRepository]:
        """
        Crea un repositorio basado en el tipo especificado.
        Método genérico del factory.
        
        Args:
            repository_type: Tipo de repositorio ('product', 'category', 'favorite')
            json_file_path: Ruta del archivo JSON (opcional)
            
        Returns:
            Instancia del repositorio solicitado o None si el tipo no es válido
        """
        repository_type = repository_type.lower()
        
        if repository_type == 'product':
            return cls.create_product_repository(json_file_path)
        elif repository_type == 'category':
            return cls.create_category_repository(json_file_path)
        elif repository_type == 'favorite':
            return cls.create_favorite_repository(json_file_path)
        else:
            raise ValueError(f"Tipo de repositorio desconocido: {repository_type}")
    
    @classmethod
    def clear_cache(cls):
        """Limpia el cache de instancias. Útil para testing."""
        cls._instances.clear()
    
    @classmethod
    def reset(cls):
        """Resetea el factory. Útil para testing."""
        cls.clear_cache()

