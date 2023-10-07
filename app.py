from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your own secret key

db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)

if __name__ == '__main__':
    from resourcesx.task import TaskResource, TaskListResource
    from resourcesx.user import UserResource, UserRegisterResource
    
    db.create_all()
    
    api.add_resource(TaskListResource, '/tasks')
    api.add_resource(TaskResource, '/tasks/<int:task_id>')
    api.add_resource(UserResource, '/users/<int:user_id>')
    api.add_resource(UserRegisterResource, '/register')
    
    app.run(debug=True)
