"""
Repositorios para acceso a datos.
Implementa el patrón Repository para separar la lógica de acceso a datos.
"""
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class BaseRepository(ABC):
    """Clase base abstracta para repositorios."""
    
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.data = None
    
    def connect(self):
        """Carga los datos del archivo JSON."""
        try:
            with open(self.json_file_path, 'r') as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            self.data = {}
            print(f"Warning: JSON file {self.json_file_path} not found. Creating new file.")
    
    def save(self):
        """Guarda los datos en el archivo JSON."""
        try:
            with open(self.json_file_path, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)
        except Exception as e:
            raise Exception(f"Error saving to {self.json_file_path}: {str(e)}")


class ProductRepository(BaseRepository):
    """Repositorio para operaciones con productos."""
    
    def __init__(self, json_file_path: str = 'db.json'):
        super().__init__(json_file_path)
        self.connect()
    
    def get_all(self) -> List[Dict]:
        """Obtiene todos los productos."""
        if self.data:
            return self.data.get('products', [])
        return []
    
    def get_by_id(self, product_id: int) -> Optional[Dict]:
        """Obtiene un producto por su ID."""
        products = self.get_all()
        return next((p for p in products if p['id'] == product_id), None)
    
    def get_by_category(self, category: str) -> List[Dict]:
        """Obtiene productos filtrados por categoría."""
        products = self.get_all()
        return [p for p in products if p.get('category', '').lower() == category.lower()]
    
    def add(self, product: Dict) -> Dict:
        """Agrega un nuevo producto."""
        if not self.data:
            self.data = {}
        
        products = self.data.get('products', [])
        
        # Generar ID si no existe
        if 'id' not in product:
            max_id = max([p.get('id', 0) for p in products], default=0)
            product['id'] = max_id + 1
        
        products.append(product)
        self.data['products'] = products
        self.save()
        return product
    
    def update(self, product_id: int, product_data: Dict) -> Optional[Dict]:
        """Actualiza un producto existente."""
        products = self.get_all()
        product = self.get_by_id(product_id)
        
        if product:
            product.update(product_data)
            self.data['products'] = products
            self.save()
            return product
        return None
    
    def delete(self, product_id: int) -> bool:
        """Elimina un producto."""
        products = self.get_all()
        original_count = len(products)
        products = [p for p in products if p['id'] != product_id]
        
        if len(products) < original_count:
            self.data['products'] = products
            self.save()
            return True
        return False


class CategoryRepository(BaseRepository):
    """Repositorio para operaciones con categorías."""
    
    def __init__(self, json_file_path: str = 'db.json'):
        super().__init__(json_file_path)
        self.connect()
    
    def get_all(self) -> List[Dict]:
        """Obtiene todas las categorías."""
        if self.data:
            return self.data.get('categories', [])
        return []
    
    def get_by_id(self, category_id: int) -> Optional[Dict]:
        """Obtiene una categoría por su ID."""
        categories = self.get_all()
        return next((c for c in categories if c['id'] == category_id), None)
    
    def get_by_name(self, name: str) -> Optional[Dict]:
        """Obtiene una categoría por su nombre."""
        categories = self.get_all()
        return next((c for c in categories if c.get('name', '').lower() == name.lower()), None)
    
    def add(self, category: Dict) -> Dict:
        """Agrega una nueva categoría."""
        if not self.data:
            self.data = {}
        
        categories = self.data.get('categories', [])
        
        # Verificar si ya existe
        if self.get_by_name(category.get('name', '')):
            raise ValueError('Category already exists')
        
        # Generar ID si no existe
        if 'id' not in category:
            max_id = max([c.get('id', 0) for c in categories], default=0)
            category['id'] = max_id + 1
        
        categories.append(category)
        self.data['categories'] = categories
        self.save()
        return category
    
    def delete_by_name(self, name: str) -> bool:
        """Elimina una categoría por su nombre."""
        categories = self.get_all()
        original_count = len(categories)
        categories = [c for c in categories if c.get('name', '').lower() != name.lower()]
        
        if len(categories) < original_count:
            self.data['categories'] = categories
            self.save()
            return True
        return False


class FavoriteRepository(BaseRepository):
    """Repositorio para operaciones con favoritos."""
    
    def __init__(self, json_file_path: str = 'favorites.json'):
        super().__init__(json_file_path)
        self.connect()
    
    def get_all(self) -> List[Dict]:
        """Obtiene todos los favoritos."""
        if self.data:
            return self.data.get('favorites', [])
        return []
    
    def get_by_user(self, user_id: int) -> List[Dict]:
        """Obtiene favoritos de un usuario."""
        favorites = self.get_all()
        return [f for f in favorites if f.get('user_id') == user_id]
    
    def add(self, favorite: Dict) -> Dict:
        """Agrega un nuevo favorito."""
        if not self.data:
            self.data = {}
        
        favorites = self.data.get('favorites', [])
        
        # Verificar si ya existe
        if self.exists(favorite.get('user_id'), favorite.get('product_id')):
            raise ValueError('Favorite already exists')
        
        favorites.append(favorite)
        self.data['favorites'] = favorites
        self.save()
        return favorite
    
    def exists(self, user_id: int, product_id: int) -> bool:
        """Verifica si un favorito ya existe."""
        favorites = self.get_all()
        return any(f.get('user_id') == user_id and f.get('product_id') == product_id 
                  for f in favorites)
    
    def delete(self, user_id: int, product_id: int) -> bool:
        """Elimina un favorito."""
        favorites = self.get_all()
        original_count = len(favorites)
        favorites = [f for f in favorites 
                    if not (f.get('user_id') == user_id and f.get('product_id') == product_id)]
        
        if len(favorites) < original_count:
            self.data['favorites'] = favorites
            self.save()
            return True
        return False

