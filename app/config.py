import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde .env

class Config:
    # Clave secreta para Flask (¡cambia esto en producción!)
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    # Conexión PostgreSQL (ajusta con tus credenciales)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:fRpFnmb8E4A3UR31@localhost:5432/taskosaurus'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Evita warnings innecesarios