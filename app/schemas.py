from app.extensions import ma
from app.models import Task

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task  # Usa el modelo Task
        load_instance = True  # Convierte JSON a objeto Task automáticamente

# Instancia los esquemas
task_schema = TaskSchema()  # Para un solo registro
tasks_schema = TaskSchema(many=True)  # Para múltiples registros