from flask import request
from flask_restful import Resource, reqparse
from utils.auth_decorator import require_auth
from services.category_service import CategoryService


class CategoriesResource(Resource):
    """Recurso REST para operaciones con categorías."""
    
    def __init__(self):
        self.service = CategoryService()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=False)

    @require_auth
    def get(self, category_id=None):
        """Obtiene categorías. Soporta búsqueda por ID."""
        if category_id is not None:
            category = self.service.get_category_by_id(category_id)
            if category:
                return category, 200
            else:
                return {'message': 'Category not found'}, 404
        
        categories = self.service.get_all_categories()
        return categories, 200

    @require_auth
    def post(self):
        """Crea una nueva categoría."""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the category')
        
        args = parser.parse_args()
        
        try:
            new_category = self.service.create_category({'name': args['name']})
            return {'message': 'Category added successfully', 'category': new_category}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error creating category: {str(e)}'}, 500

    @require_auth
    def delete(self):
        """Elimina una categoría por nombre."""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the category')
        
        args = parser.parse_args()
        category_name = args.get('name')
        
        try:
            deleted = self.service.delete_category(category_name)
            if deleted:
                return {'message': 'Category removed successfully'}, 200
            else:
                return {'message': 'Category not found'}, 404
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error deleting category: {str(e)}'}, 500

