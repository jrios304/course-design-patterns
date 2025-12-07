"""
Módulo de autenticación centralizado.
Implementa el patrón Decorator para validación de tokens.
Utiliza el patrón Strategy para diferentes métodos de autenticación.
"""
from functools import wraps
from flask import request
from flask_restful import abort
from utils.auth_strategy import AuthenticationContext, SimpleTokenStrategy

# Contexto global de autenticación con estrategia por defecto
_auth_context = AuthenticationContext(SimpleTokenStrategy('abcd12345'))


def set_auth_strategy(strategy):
    """
    Permite cambiar la estrategia de autenticación globalmente.
    Útil para testing o cambiar entre diferentes métodos de autenticación.
    
    Args:
        strategy: Instancia de AuthenticationStrategy
    """
    global _auth_context
    _auth_context.set_strategy(strategy)


def require_auth(func):
    """
    Decorador que valida el token de autenticación antes de ejecutar el método.
    Implementa el patrón Decorator.
    Utiliza el patrón Strategy para la validación.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            abort(401, message='Unauthorized: access token not found')
        
        if not _auth_context.validate_token(token):
            abort(401, message='Unauthorized: invalid token')
        
        return func(*args, **kwargs)
    
    return wrapper


def is_valid_token(token):
    """
    Valida si un token es válido usando la estrategia configurada.
    Mantiene compatibilidad con código existente.
    
    Args:
        token: Token a validar
        
    Returns:
        True si el token es válido, False en caso contrario
    """
    return _auth_context.validate_token(token)

