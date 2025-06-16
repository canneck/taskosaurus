from flask_restx import Resource, Namespace
from app.models import Task
from app.extensions import db
from app.schemas import task_schema, tasks_schema
from app.validators.status_validator import StatusValidator
from flask import request

api = Namespace('tasks', description='Operaciones con tareas')

@api.route('/')
class TaskList(Resource):
    def get(self):
        """
        Listar todas las tareas con filtros opcionales:
        - status
        - created_at (YYYY-MM-DD)
        - title (búsqueda parcial)
        """
        query = Task.query.filter(Task.status != 'archived')  # Excluye archivadas

        status = request.args.get('status')
        created_at = request.args.get('created_at')
        title = request.args.get('title')

        if status:
            query = query.filter(Task.status == status)

        if created_at:
            from datetime import datetime
            try:
                date = datetime.strptime(created_at, "%Y-%m-%d").date()
                query = query.filter(db.func.date(Task.created_at) == date)
            except ValueError:
                api.abort(400, "Formato de fecha inválido. Usa YYYY-MM-DD")

        if title:
            query = query.filter(Task.title.ilike(f"%{title}%"))

        tasks = query.all()
        return tasks_schema.dump(tasks)

    def post(self):
        """Crear una nueva tarea"""
        # {
        #   "title": "Comprar café",
        #   "description": "Ir a plaza vea a comprar café",
        #   "status": "pending"
        # }
        data = api.payload  # JSON enviado en la request
        new_task = task_schema.load(data)
        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task), 201
    
    
@api.route('/get-archived')
class ArchivedTasks(Resource):
    def get(self):
        """Listar solo tareas archivadas"""
        archived_tasks = Task.query.filter_by(status='archived').all()
        return tasks_schema.dump(archived_tasks)


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
        #   "status": "pending"
        # }
        task = Task.query.get_or_404(id)
        data = api.payload
        
        validator = StatusValidator()
        
        if 'status' in data:
            if not validator.is_valid_transition(task.status, data['status']):
                api.abort(400, f"Transición no permitida de {task.status} a {data['status']}")
        
        # Resto de la lógica de actualización...
        task.status = data.get('status', task.status)
        db.session.commit()
        
        return task_schema.dump(task)    
    
    def delete(self, id):
        """Eliminar una tarea por ID"""
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return {'message': f'Tarea con ID {id} eliminada correctamente.'}, 200