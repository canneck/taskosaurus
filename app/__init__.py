from flask import Flask
from flask_restx import Api
from app.config import Config
from app.extensions import db, ma, jwt
from sqlalchemy import text
from app.api.resources.tasks import api as tasks_ns

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Inicializar extensiones básicas
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # 2. Configurar API REST
    api = Api(
        app, 
        title="Taskosaurus API",
        version="1.0",
        description="API para gestión de tareas"
    )
    api.add_namespace(tasks_ns, path='/tasks')

    # 3. Creación de tablas y validación (solo en desarrollo)
    with app.app_context():
        try:
            db.create_all()  # Crea todas las tablas
            print("✅ Tablas creadas/existentes en PostgreSQL")
            
            # Test de conexión
            db.session.execute(text('SELECT 1'))
            print("✅ Conexión a PostgreSQL activa")
            
        except Exception as e:
            print(f"❌ Error en base de datos: {str(e)}")
            if "already exists" not in str(e):  # Ignora errores de tablas existentes
                raise

    return app