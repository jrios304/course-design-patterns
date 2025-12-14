"""
Implementación del patrón Repository.
Abstrae el acceso a datos y proporciona una interfaz limpia.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from app.utils.database import DatabaseConnection


T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Clase base para todos los repositorios.

    El patrón Repository proporciona:
    1. Abstracción del acceso a datos
    2. Separación de lógica de negocio y acceso a datos
    3. Facilita testing con mocks
    4. Centraliza queries
    """

    def __init__(self, collection_name: str):
        """
        Inicializa el repositorio.

        Args:
            collection_name: Nombre de la colección en la BD
        """
        self.db = DatabaseConnection()
        self.collection_name = collection_name

    @abstractmethod
    def to_entity(self, data: dict) -> T:
        """Convierte un diccionario a entidad de dominio"""
        pass

    @abstractmethod
    def to_dict(self, entity: T) -> dict:
        """Convierte una entidad de dominio a diccionario"""
        pass

    def find_all(self) -> List[T]:
        """
        Obtiene todos los elementos.

        Returns:
            Lista de entidades
        """
        data = self.db.get_data(self.collection_name)
        return [self.to_entity(item) for item in data]

    def find_by_id(self, entity_id: int) -> Optional[T]:
        """
        Busca una entidad por ID.

        Args:
            entity_id: ID de la entidad

        Returns:
            Entidad o None si no se encuentra
        """
        data = self.db.get_data(self.collection_name)
        for item in data:
            if item.get('id') == entity_id:
                return self.to_entity(item)
        return None

    def save(self, entity: T) -> T:
        """
        Guarda una nueva entidad.

        Args:
            entity: Entidad a guardar

        Returns:
            Entidad guardada con ID asignado
        """
        data = self.to_dict(entity)

        # Asignar ID si no tiene
        if data.get('id') is None:
            existing = self.db.get_data(self.collection_name)
            next_id = max([item.get('id', 0) for item in existing], default=0) + 1
            data['id'] = next_id

        self.db.add_item(self.collection_name, data)
        return self.to_entity(data)

    def update(self, entity_id: int, entity: T) -> Optional[T]:
        """
        Actualiza una entidad existente.

        Args:
            entity_id: ID de la entidad
            entity: Entidad con datos actualizados

        Returns:
            Entidad actualizada o None si no existe
        """
        data = self.to_dict(entity)
        success = self.db.update_item(self.collection_name, entity_id, data)
        if success:
            return self.to_entity(data)
        return None

    def delete(self, entity_id: int) -> bool:
        """
        Elimina una entidad.

        Args:
            entity_id: ID de la entidad

        Returns:
            True si se eliminó exitosamente
        """
        return self.db.remove_item(self.collection_name, entity_id)

    def find_by_criteria(self, filter_fn) -> List[T]:
        """
        Busca entidades que cumplan un criterio.

        Args:
            filter_fn: Función de filtro

        Returns:
            Lista de entidades que cumplen el criterio
        """
        results = self.db.query(self.collection_name, filter_fn)
        return [self.to_entity(item) for item in results]

    def count(self) -> int:
        """Retorna el número total de entidades"""
        return len(self.db.get_data(self.collection_name))

    def exists(self, entity_id: int) -> bool:
        """Verifica si existe una entidad con el ID dado"""
        return self.find_by_id(entity_id) is not None
