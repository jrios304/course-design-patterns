from flask import Blueprint, request
from flask_restful import Resource, Api

class AuthenticationResource(Resource):
    def post(self):
        if not request.is_json:
            return {'message': 'Content-Type must be application/json'}, 400
        
        try:
            data = request.get_json()
        except Exception as e:
            return {'message': f'Invalid JSON: {str(e)}'}, 400
        
        if not data:
            return {'message': 'JSON body is required'}, 400
        
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'username and password are required'}, 400

        if username == 'student' and password == 'desingp':
            token = 'abcd12345'
            return {'token': token}, 200
        else:
            return {'message': 'unauthorized'}, 401



