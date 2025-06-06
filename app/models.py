from app.extensions import db  # Importa la instancia de SQLAlchemy

class Task(db.Model):
    """Modelo para la tabla 'tasks'."""
    __tablename__ = 'tasks'  # Nombre exacto de la tabla en PostgreSQL

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20),
        default='Pending',                    # Valor por defecto en SQLAlchemy/Python
        server_default=db.text("'Pending'")   # Valor por defecto en la base de datos
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Fecha automática

    def __repr__(self):
        return f'<Task {self.title}>'