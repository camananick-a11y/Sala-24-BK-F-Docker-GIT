# Sala-24-BK-F-Docker-GIT

# 🧩 Día 3 — Blog Service (Microservicios con Django, DRF, PostgreSQL y Redis)

### 📚 Descripción general
Este microservicio forma parte del laboratorio **Sala 24 – Backend (Día 3)**, cuyo objetivo fue construir un **servicio de Blog** independiente que maneje publicaciones y categorías, con **paginación, búsqueda, caché (Redis)** y **healthcheck**.

Este servicio está listo para integrarse más adelante con el microservicio de **autenticación (Auth Service)** mediante JWT.

---

## ⚙️ Stack Tecnológico
- **Django 5.0**
- **Django REST Framework (DRF)**
- **PostgreSQL 15**
- **Redis 7**
- **Docker & Docker Compose**
- **django-redis**
- **django-filter**
- **python-slugify**
- **gunicorn**

---

## 🏗️ Estructura del Proyecto

microservices-lab/
│
├── docker-compose.yml
├── .env
│
└── blog-service/
├── Dockerfile
├── manage.py
├── requirements.txt
├── openapi.yaml
│
├── blog_service/ # Configuración principal (settings, urls, wsgi)
├── core/ # Middleware y utilidades (logging, paginación, cache)
├── authors/ # App de autores (seed local)
├── categories/ # App de categorías
└── posts/ # App de publicaciones

yaml
Copiar código

---

## 🔧 Instalación y Ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/microservices-lab.git
cd microservices-lab
2️⃣ Verificar el archivo .env
Crea o verifica que exista un archivo .env con el siguiente contenido:

env
Copiar código
POSTGRES_USER=devuser
POSTGRES_PASSWORD=devpass
POSTGRES_DB=main_db
REDIS_HOST=redis
REDIS_PORT=6379
3️⃣ Levantar los servicios
Ejecuta en la raíz del proyecto:

bash
Copiar código
docker-compose up --build
Esto levantará los servicios:

PostgreSQL en localhost:5432

Redis en localhost:6379

Blog Service en localhost:8001

🗃️ Migraciones y Datos Iniciales (Seed)
Una vez dentro del contenedor del blog:

bash
Copiar código
docker exec -it blog_service bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_blog
Verifica los datos cargados:

bash
Copiar código
python manage.py shell
>>> from posts.models import Post
>>> Post.objects.count()
30
🌐 Endpoints Principales
Método	Endpoint	Descripción	Cache	Ejemplo de respuesta
GET	/healthz	Verifica conexión a DB y Redis	❌	{ "db": true, "redis": true }
GET	/api/categories/	Lista categorías activas	✅ (TTL: 60s)	[{"id":1,"name":"Tech","slug":"tech"}]
GET	/api/posts?search=&page=	Lista posts publicados, filtrables por título o cuerpo	❌	{ "count":30,"results":[{"id":1,"title":"Sample Post 1",...}]}
GET	/api/posts/{slug}/	Devuelve detalle del post (y aumenta vistas)	✅ (TTL: 60s)	{ "id":1,"title":"Sample Post 1","body":"Lorem ipsum...", ... }

⚙️ Paginación y Búsqueda
Paginación: automática con page_size=10

Ejemplo: /api/posts?page=2

Búsqueda: parámetro search en título o cuerpo

Ejemplo: /api/posts?search=django

🧠 Observabilidad
Healthcheck
bash
Copiar código
GET http://localhost:8001/healthz
Respuesta esperada:

json
Copiar código
{
  "db": true,
  "redis": true
}
Logging JSON
Cada request genera un log estructurado con:

json
Copiar código
{
  "method": "GET",
  "path": "/api/posts/",
  "status": 200,
  "duration_ms": 12
}
🗄️ Docker Compose
yaml
Copiar código
version: "3.9"
services:
  postgres:
    image: postgres:15
    container_name: db_postgres
    restart: always
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: main_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7
    container_name: cache_redis
    restart: always
    ports:
      - "6379:6379"

  blog:
    build: ./blog-service
    container_name: blog_service
    environment:
      - DB_HOST=postgres
      - DB_NAME=main_db
      - DB_USER=devuser
      - DB_PASS=devpass
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - DEBUG=1
    depends_on:
      - postgres
      - redis
    ports:
      - "8001:8001"

volumes:
  pgdata:
🧾 Ejemplo de flujo con Postman
GET http://localhost:8001/healthz → ✅ 200 OK

GET http://localhost:8001/api/categories/ → ✅ lista de categorías activas

GET http://localhost:8001/api/posts/ → ✅ lista paginada de posts

GET http://localhost:8001/api/posts/sample-post-1/ → ✅ detalle del post

(Opcional) Repetir #4 → valor views incrementa

✅ Estado final — Día 3 completado
Componente	Estado
PostgreSQL + Redis funcionando	✅
Migraciones y datos semilla	✅
Endpoints /api/categories, /api/posts, /healthz	✅
Caché en categorías y detalle de posts	✅
Logging JSON	✅
Docker Compose operativo	✅
