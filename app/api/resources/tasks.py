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
        # {
        #   "title": "Comprar café",
        #   "description": "Ir a plaza vea a comprar café",
        #   "status": "Pending"
        # }
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
    
    def put(self, id):
        """Actualizar estado de una tarea"""
        # {
        #   "title": "Comprar café",
        #   "description": "Ir a plaza vea a comprar café",
        #   "status": "Pending"
        # }
        task = Task.query.get_or_404(id)
        data = api.payload
        
        # Validar que el estado esté en los valores permitidos
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        if 'status' in data and data['status'] not in valid_statuses:
            api.abort(400, f"Estado inválido. Valores permitidos: {', '.join(valid_statuses)}")
        
        # Actualizar solo campos permitidos
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        
        db.session.commit()
        return task_schema.dump(task)