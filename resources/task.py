from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, db

# Parser for parsing JSON data from the request
task_parser = reqparse.RequestParser()
task_parser.add_argument('title', type=str, required=True, help='Title of the task')
task_parser.add_argument('description', type=str, required=False, help='Description of the task')
task_parser.add_argument('status', type=str, choices=('pending', 'in progress', 'completed'), required=True, help='Status of the task')
task_parser.add_argument('due_date', type=str, required=True, help='Due date of the task')

class TaskResource(Resource):
    @jwt_required
    def get(self, task_id):
        task = Task.query.get(task_id)
        if task:
            return task.__dict__, 200
        return {'message': 'Task not found'}, 404

    @jwt_required
    def put(self, task_id):
        args = task_parser.parse_args()
        task = Task.query.get(task_id)
        
        if task:
            task.title = args['title']
            task.description = args['description']
            task.status = args['status']
            task.due_date = args['due_date']
            db.session.commit()
            return {'message': 'Task updated successfully'}, 200
        return {'message': 'Task not found'}, 404

    @jwt_required
    def delete(self, task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return {'message': 'Task deleted successfully'}, 200
        return {'message': 'Task not found'}, 404

class TaskListResource(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=user_id).all()
        return [task.__dict__ for task in tasks], 200

    @jwt_required
    def post(self):
        args = task_parser.parse_args()
        user_id = get_jwt_identity()
        
        task = Task(
            title=args['title'],
            description=args['description'],
            status=args['status'],
            due_date=args['due_date'],
            user_id=user_id
        )
        
        db.session.add(task)
        db.session.commit()
        return {'message': 'Task created successfully'}, 201
