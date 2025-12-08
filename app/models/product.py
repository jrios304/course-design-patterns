"""
Modelo de dominio para Producto
Representa la entidad Product en el sistema
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """
    Clase que representa un producto en el sistema.

    Attributes:
        id: Identificador único del producto
        name: Nombre del producto
        category: Categoría a la que pertenece
        price: Precio del producto
    """
    id: int
    name: str
    category: str
    price: float

    def to_dict(self) -> dict:
        """Convierte el producto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price
        }

    @staticmethod
    def from_dict(data: dict) -> 'Product':
        """Crea un producto desde un diccionario"""
        return Product(
            id=data.get('id'),
            name=data.get('name'),
            category=data.get('category'),
            price=data.get('price')
        )

    def __str__(self) -> str:
        return f"Product({self.id}, {self.name}, {self.price})"
