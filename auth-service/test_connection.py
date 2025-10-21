import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import redis

# Cargar variables de entorno (busca automáticamente en la raíz montada)
load_dotenv()

# Variables de entorno
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db_postgres')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)

REDIS_HOST = os.getenv('REDIS_HOST', 'cache_redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')  # Opcional

def test_postgres_connection():
    """Prueba conexión a PostgreSQL y verifica versión."""
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ Conexión a PostgreSQL exitosa. Versión: {version[0]}")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error en conexión a PostgreSQL: {e}")
        return False

def test_redis_connection():
    """Prueba conexión a Redis con ping y set/get básico."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
        response = r.ping()
        if response:
            print("✅ Conexión a Redis exitosa. Ping: PONG")
            # Prueba extra
            r.set('test_key', 'test_value')
            value = r.get('test_key')
            print(f"   Prueba extra: GET 'test_key' = {value}")
            r.delete('test_key')
            return True
        else:
            print("❌ Respuesta inválida de Redis.")
            return False
    except Exception as e:
        print(f"❌ Error en conexión a Redis: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Probando conexiones en auth-service...")
    postgres_ok = test_postgres_connection()
    redis_ok = test_redis_connection()
    
    if postgres_ok and redis_ok:
        print("\n🎉 ¡Todas las conexiones funcionan! Entorno listo para microservicios.")
        sys.exit(0)
    else:
        print("\n⚠️  Algunas conexiones fallaron. Revisa .env o logs de Docker.")
        sys.exit(1)