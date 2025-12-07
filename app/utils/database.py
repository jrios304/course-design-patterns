"""
Implementación del patrón Singleton para la conexión a la base de datos.
Garantiza una única instancia de conexión en toda la aplicación.
"""
import json
import threading
from typing import Dict, Any, Optional


class DatabaseConnection:
    """
    Singleton para gestionar la conexión a la base de datos JSON.

    El patrón Singleton garantiza:
    1. Una única instancia en toda la aplicación
    2. Acceso global a esa instancia
    3. Inicialización lazy (solo cuando se necesita)
    4. Thread-safe
    """

    _instance: Optional['DatabaseConnection'] = None
    _lock: threading.Lock = threading.Lock()
    _initialized: bool = False

    def __new__(cls, *args, **kwargs):
        """
        Implementa el patrón Singleton con thread safety.
        """
        if cls._instance is None:
            with cls._lock:
                # Double-check locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, json_file_path: str = 'db.json'):
        """
        Inicializa la conexión (solo una vez).

        Args:
            json_file_path: Ruta al archivo JSON
        """
        # Evitar reinicialización
        if self._initialized:
            return

        self.json_file_path = json_file_path
        self.data: Optional[Dict[str, Any]] = None
        self._load_data()
        self._initialized = True

    def _load_data(self) -> None:
        """Carga los datos desde el archivo JSON"""
        try:
            with open(self.json_file_path, 'r') as json_file:
                self.data = json.load(json_file)
            print(f"✅ Database loaded from {self.json_file_path}")
        except FileNotFoundError:
            self.data = {
                'products': [],
                'categories': [],
                'favorites': [],
                'notifications': []
            }
            print(f"⚠️  Database file not found. Created new structure.")
            self._save_data()
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}")
            self.data = None

    def _save_data(self) -> None:
        """Guarda los datos en el archivo JSON"""
        if self.data is not None:
            with open(self.json_file_path, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)

    def get_data(self, key: str) -> list:
        """
        Obtiene datos por clave.

        Args:
            key: Clave en el JSON (products, categories, etc.)

        Returns:
            Lista de elementos
        """
        if self.data:
            return self.data.get(key, [])
        return []

    def add_item(self, key: str, item: Dict[str, Any]) -> bool:
        """
        Agrega un item a una colección.

        Args:
            key: Clave de la colección
            item: Item a agregar

        Returns:
            bool: True si se agregó exitosamente
        """
        if self.data is None:
            return False

        collection = self.data.get(key, [])
        collection.append(item)
        self.data[key] = collection
        self._save_data()
        return True

    def update_item(self, key: str, item_id: int, updated_data: Dict[str, Any]) -> bool:
        """
        Actualiza un item en una colección.

        Args:
            key: Clave de la colección
            item_id: ID del item a actualizar
            updated_data: Datos actualizados

        Returns:
            bool: True si se actualizó exitosamente
        """
        if self.data is None:
            return False

        collection = self.data.get(key, [])
        for i, item in enumerate(collection):
            if item.get('id') == item_id:
                collection[i] = {**item, **updated_data}
                self.data[key] = collection
                self._save_data()
                return True
        return False

    def remove_item(self, key: str, item_id: int) -> bool:
        """
        Elimina un item de una colección.

        Args:
            key: Clave de la colección
            item_id: ID del item a eliminar

        Returns:
            bool: True si se eliminó exitosamente
        """
        if self.data is None:
            return False

        collection = self.data.get(key, [])
        original_length = len(collection)
        collection = [item for item in collection if item.get('id') != item_id]

        if len(collection) < original_length:
            self.data[key] = collection
            self._save_data()
            return True
        return False

    def query(self, key: str, filter_fn) -> list:
        """
        Consulta items que cumplan con un filtro.

        Args:
            key: Clave de la colección
            filter_fn: Función de filtro

        Returns:
            Lista de items que cumplen el filtro
        """
        collection = self.get_data(key)
        return [item for item in collection if filter_fn(item)]

    @classmethod
    def reset_instance(cls):
        """
        Resetea la instancia del Singleton.
        Útil para testing.
        """
        with cls._lock:
            cls._instance = None
            cls._initialized = False
