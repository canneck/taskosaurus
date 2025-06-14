import os
from dotenv import load_dotenv

load_dotenv()  # Solo se usa en desarrollo

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-por-defecto')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
