from flask_restx import Resource, Namespace
from app.models import Task
from app.extensions import db
from app.schemas import task_schema, tasks_schema

api = Namespace('tasks', description='Operaciones con tareas')

@api.route('/')
class TaskList(Resource):
    def get(self):
        """Listar todas las tareas"""
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)

    def post(self):
        """Crear una nueva tarea"""
        data = api.payload  # JSON enviado en la request
        new_task = task_schema.load(data)
        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task), 201

@api.route('/<int:id>')
class TaskDetail(Resource):
    def get(self, id):
        """Obtener una tarea por ID"""
        task = Task.query.get_or_404(id)
        return task_schema.dump(task)