"""
Estrategias de autenticación.
Implementa el patrón Strategy para permitir diferentes métodos de validación de tokens.
"""
from abc import ABC, abstractmethod


class AuthenticationStrategy(ABC):
    """Interfaz abstracta para estrategias de autenticación."""
    
    @abstractmethod
    def validate_token(self, token: str) -> bool:
        """
        Valida un token de autenticación.
        
        Args:
            token: Token a validar
            
        Returns:
            True si el token es válido, False en caso contrario
        """
        pass


class SimpleTokenStrategy(AuthenticationStrategy):
    """Estrategia simple de validación de tokens (comparación directa)."""
    
    def __init__(self, valid_token: str = 'abcd12345'):
        """
        Inicializa la estrategia con un token válido.
        
        Args:
            valid_token: Token válido para comparación
        """
        self.valid_token = valid_token
    
    def validate_token(self, token: str) -> bool:
        """Valida el token comparándolo directamente con el token válido."""
        return token == self.valid_token


class JWTStrategy(AuthenticationStrategy):
    """Estrategia para validación de tokens JWT (preparada para futura implementación)."""
    
    def __init__(self, secret_key: str = None):
        """
        Inicializa la estrategia JWT.
        
        Args:
            secret_key: Clave secreta para validar JWT (opcional)
        """
        self.secret_key = secret_key
    
    def validate_token(self, token: str) -> bool:
        """
        Valida un token JWT.
        
        Nota: Esta es una implementación básica. En producción se usaría
        una librería como PyJWT para validar tokens JWT reales.
        """
        # Implementación básica - en producción usar PyJWT
        if not token or not token.startswith('Bearer '):
            return False
        
        # Por ahora, validación simple
        # En producción: decodificar y validar JWT
        return len(token) > 10


class DatabaseTokenStrategy(AuthenticationStrategy):
    """Estrategia para validar tokens consultando una base de datos."""
    
    def __init__(self, token_repository=None):
        """
        Inicializa la estrategia con un repositorio de tokens.
        
        Args:
            token_repository: Repositorio para consultar tokens válidos
        """
        self.token_repository = token_repository
    
    def validate_token(self, token: str) -> bool:
        """
        Valida el token consultando la base de datos.
        
        En una implementación real, consultaría una tabla de tokens
        o sesiones activas.
        """
        if not self.token_repository:
            return False
        
        # Simulación: en producción consultaría la base de datos
        # return self.token_repository.is_token_valid(token)
        return False  # Por ahora retorna False hasta implementar repositorio


class AuthenticationContext:
    """
    Contexto que utiliza una estrategia de autenticación.
    Implementa el patrón Strategy.
    """
    
    def __init__(self, strategy: AuthenticationStrategy = None):
        """
        Inicializa el contexto con una estrategia.
        
        Args:
            strategy: Estrategia de autenticación a utilizar
        """
        self.strategy = strategy or SimpleTokenStrategy()
    
    def set_strategy(self, strategy: AuthenticationStrategy):
        """Cambia la estrategia de autenticación en tiempo de ejecución."""
        self.strategy = strategy
    
    def validate_token(self, token: str) -> bool:
        """
        Valida un token usando la estrategia configurada.
        
        Args:
            token: Token a validar
            
        Returns:
            True si el token es válido según la estrategia
        """
        return self.strategy.validate_token(token)

