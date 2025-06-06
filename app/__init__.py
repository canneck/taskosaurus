from flask import Flask
from flask_restx import Api
from app.config import Config
from app.extensions import db, ma, jwt, migrate
from sqlalchemy import text
from app.api.resources.tasks import api as tasks_ns

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)  # Flask-Migrate

    # Registro manual de extensiones para verificación
    app.extensions['marshmallow'] = ma
    app.extensions['jwt'] = jwt
    app.extensions['migrate'] = migrate

    # Inicializa Flask-RESTX
    api = Api(app, title="Taskosaurus API", version="1.0", description="API de tareas")
    api.add_namespace(tasks_ns, path='/tasks')

    with app.app_context():
        # Validación de conexión y extensiones
        print("\n🔍 Validando configuraciones iniciales:")
        
        # 1. Verificar conexión a DB
        try:
            db.session.execute(text('SELECT 1'))
            print("✅ 1. Conexión a PostgreSQL: Correcta")
        except Exception as e:
            print(f"❌ 1. Conexión a PostgreSQL: Falló - {str(e)}")

        # 2. Verificar extensiones clave
        print(f"✅ 2. SQLAlchemy: {'Cargado' if 'sqlalchemy' in app.extensions else 'Error'}")
        print(f"✅ 3. Marshmallow: {'Cargado' if 'marshmallow' in app.extensions else 'Error'}")
        print(f"✅ 4. JWT: {'Cargado' if 'jwt' in app.extensions else 'Error'}")
        print(f"✅ 5. Flask-Migrate: {'Cargado' if 'migrate' in app.extensions else 'Error'}")

        # 3. Verificar modelo Task (opcional)
        try:
            from app.models import Task
            print("✅ 6. Modelo 'Task': Importado correctamente")
        except Exception as e:
            print(f"❌ 6. Modelo 'Task': Error - {str(e)}")

    return app