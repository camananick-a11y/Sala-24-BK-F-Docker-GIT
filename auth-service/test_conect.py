import os
import psycopg2
import redis
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env que está un nivel arriba
load_dotenv("../.env")

def test_postgres():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="localhost",
            port="5432"
        )
        print("✅ Conexión a PostgreSQL exitosa")
        conn.close()
    except Exception as e:
        print("❌ Error al conectar a PostgreSQL:", e)

def test_redis():
    try:
        r = redis.Redis(
            host="localhost",
            port=os.getenv("REDIS_PORT"),
            decode_responses=True
        )
        r.ping()
        print("✅ Conexión a Redis exitosa")
    except Exception as e:
        print("❌ Error al conectar a Redis:", e)

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de conexión...")
    test_postgres()
    test_redis()
