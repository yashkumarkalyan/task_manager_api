from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import User, db

# Parser for parsing JSON data from the request
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username')
user_parser.add_argument('password', type=str, required=True, help='Password')

class UserResource(Resource):
    @jwt_required
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return {'id': user.id, 'username': user.username}, 200
        return {'message': 'User not found'}, 404

class UserRegisterResource(Resource):
    def post(self):
        args = user_parser.parse_args()
        
        if User.query.filter_by(username=args['username']).first():
            return {'message': 'Username already exists'}, 400
        
        user = User(username=args['username'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'message': 'User registered successfully',
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201
