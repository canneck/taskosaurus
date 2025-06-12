import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde .env

class Config:
    # Clave secreta para Flask (¡cambia esto en producción!)
    SECRET_KEY = os.environ['SECRET_KEY']

    # Conexión PostgreSQL (ajusta con tus credenciales)
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Evita warnings innecesarios