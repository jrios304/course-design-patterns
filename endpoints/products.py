from flask_restful import Resource, reqparse
from flask import request
from utils.auth_decorator import require_auth
from services.product_service import ProductService


class ProductsResource(Resource):
    """Recurso REST para operaciones con productos."""
    
    def __init__(self):
        self.service = ProductService()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=False)
        self.parser.add_argument('category', type=str, required=False)
        self.parser.add_argument('price', type=float, required=False)
    
    @require_auth
    def get(self, product_id=None):
        """Obtiene productos. Soporta filtrado por categoría y búsqueda por ID."""
        category_filter = request.args.get('category')
        
        if category_filter:
            products = self.service.get_products_by_category(category_filter)
            return products, 200
        
        if product_id is not None:
            product = self.service.get_product_by_id(product_id)
            if product:
                return product, 200
            else:
                return {'message': 'Product not found'}, 404
        
        products = self.service.get_all_products()
        return products, 200

    @require_auth
    def post(self):
        """Crea un nuevo producto."""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the product')
        parser.add_argument('category', type=str, required=True, help='Category of the product')
        parser.add_argument('price', type=float, required=True, help='Price of the product')

        args = parser.parse_args()
        
        try:
            new_product = self.service.create_product({
                'name': args['name'],
                'category': args['category'],
                'price': args['price']
            })
            return {'message': 'Product added', 'product': new_product}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error creating product: {str(e)}'}, 500


