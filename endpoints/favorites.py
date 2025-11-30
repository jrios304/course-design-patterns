from flask_restful import Resource, reqparse
from flask import request
from utils.auth_decorator import require_auth
from services.favorite_service import FavoriteService


class FavoritesResource(Resource):
    """Recurso REST para operaciones con favoritos."""
    
    def __init__(self):
        self.service = FavoriteService()

    @require_auth
    def get(self):
        """Obtiene todos los favoritos."""
        favorites = self.service.get_all_favorites()
        return favorites, 200

    @require_auth
    def post(self):
        """Agrega un producto a favoritos."""
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')
        
        args = parser.parse_args()
        
        try:
            new_favorite = self.service.add_favorite({
                'user_id': args['user_id'],
                'product_id': args['product_id']
            })
            return {'message': 'Product added to favorites', 'favorite': new_favorite}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error adding favorite: {str(e)}'}, 500

    @require_auth
    def delete(self):
        """Elimina un producto de favoritos."""
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')

        args = parser.parse_args()
        user_id = args['user_id']
        product_id = args['product_id']

        try:
            deleted = self.service.remove_favorite(user_id, product_id)
            if deleted:
                return {'message': 'Product removed from favorites'}, 200
            else:
                return {'message': 'Favorite not found'}, 404
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error removing favorite: {str(e)}'}, 500
