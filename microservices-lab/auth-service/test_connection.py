import os
import psycopg2
import redis

# ---------------------------
# 📦 Prueba conexión PostgreSQL
# ---------------------------
print("🔍 Probando conexión a PostgreSQL...")

try:
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )
    print("✅ Conexión a PostgreSQL exitosa!")
    conn.close()
except Exception as e:
    print("❌ Error al conectar a PostgreSQL:", e)

# ---------------------------
# ⚡ Prueba conexión Redis
# ---------------------------
print("\n🔍 Probando conexión a Redis...")

try:
    r = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        db=0
    )
    r.ping()
    print("✅ Conexión a Redis exitosa!")
except Exception as e:
    print("❌ Error al conectar a Redis:", e)
