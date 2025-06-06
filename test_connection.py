from sqlalchemy import create_engine, text
from app.config import Config  # Agrega esta línea

if __name__ == "__main__":
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("¡Conexión exitosa!", result.scalar())
    except Exception as e:
        print("Error al conectar:", e)