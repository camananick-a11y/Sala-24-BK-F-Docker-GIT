<img width="1280" height="960" alt="image" src="https://github.com/user-attachments/assets/7b7a5e75-4add-43ea-b88b-20ca369baa43" /># Sala-24-BK-F-Docker-GIT

🧩 **Día 3 — Blog Service**  
Microservicios con Django, DRF, PostgreSQL y Redis

---

## 📚 Descripción general

Este microservicio forma parte del laboratorio Sala 24 – Backend (Día 3), cuyo objetivo fue construir un **Blog Service independiente** que maneje publicaciones y categorías, con:

- Paginación  
- Búsqueda  
- Caché (Redis)  
- Healthcheck  

---

# 📦 Dependencias (requirements.txt)
```
asgiref==3.10.0
blinker==1.9.0
click==8.3.0
colorama==0.4.6
Django==5.2.7
django-filter==25.2
django-redis==6.0.0
djangorestframework==3.16.1
gunicorn==23.0.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
packaging==25.0
psycopg2-binary==2.9.11
python-dotenv==1.2.1
python-slugify==8.0.4
redis==7.0.1
sqlparse==0.5.3
text-unidecode==1.3
tzdata==2025.2
Werkzeug==3.1.3
```
---

## 🏗️ Estructura del Proyecto
```
microservices-lab/
├── docker-compose.yml
├── .env
└── blog-service/
├── Dockerfile
├── manage.py
├── requirements.txt
├── openapi.yaml
├── blog_service/ # Configuración principal (settings, urls, wsgi)
├── core/ # Middleware y utilidades (logging, paginación, cache)
├── authors/ # App de autores (seed local)
├── categories/ # App de categorías
└── posts/ # App de publicaciones
```
---

## 🔧 Instalación y Ejecución

### 1️⃣ Clonar el repositorio

```
git clone https://github.com/camananick-a11y/Sala-24-BK-F-Docker-GIT
cd Sala-24-BK-F-Docker-GIT
```
---

2️⃣ Verificar el archivo .env

Crea o verifica que exista un archivo .env con el siguiente contenido:
```
POSTGRES_USER=devuser
POSTGRES_PASSWORD=devpass
POSTGRES_DB=main_db
REDIS_HOST=redis
REDIS_PORT=6379

```
---

3️⃣ Levantar los servicios
```
docker-compose up --build
Servicios levantados:

PostgreSQL en localhost:5432

Redis en localhost:6379

Blog Service en localhost:8001
```
---


🗃️ Migraciones y Datos Iniciales (Seed)


Dentro del contenedor del blog:
```
docker exec -it blog_service bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_blog
```
---

Verificar los datos cargados:
```
python manage.py shell
>>> from posts.models import Post
>>> Post.objects.count()
30
```
---

🌐 Endpoints Principales

Método	Endpoint	Descripción	Cache	Ejemplo de respuesta
```
GET	/healthz	Verifica conexión a DB y Redis	                                         ❌	{ "db": true, "redis": true }
GET	/api/categories/	Lista categorías activas	                                       ✅ (TTL: 60s)	[{"id":1,"name":"Tech","slug":"tech"}]
GET	/api/posts?search=&page=	Lista posts publicados, filtrables por título o cuerpo	 ❌	{ "count":30,"results":[{"id":1,"title":"Sample Post 1",...}] }
GET	/api/posts/{slug}/	Devuelve detalle del post (y aumenta vistas)	                 ✅ (TTL: 60s)	{ "id":1,"title":"Sample Post 1","body":"Lorem ipsum...", ... }
```
---

⚙️ Paginación y Búsqueda

-Paginación: automática con page_size=10
Ejemplo: /api/posts?page=2

-Búsqueda: parámetro search en título o cuerpo
Ejemplo: /api/posts?search=django

---

🧠 Observabilidad
Healthcheck

---
```
GET http://localhost:8001/healthz
Respuesta esperada:
```

 ```
{
  "db": true,
  "redis": true
}
Logging JSON
Cada request genera un log estructurado:
```
---
```
{
  "method": "GET",
  "path": "/api/posts/",
  "status": 200,
  "duration_ms": 12
}
```
---

🗄️ Docker Compose

```
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
```
---

🧾 Ejemplo de flujo con Postman
```
GET http://localhost:8001/healthz →                       ✅ 200 OK

GET http://localhost:8001/api/categories/ →               ✅ Lista de categorías activas

GET http://localhost:8001/api/posts/ →                    ✅ Lista paginada de posts

GET http://localhost:8001/api/posts/sample-post-1/ →      ✅ Detalle del post
```

---

✅ Estado final — Día 3 completado
```
Componente	                                      Estado
PostgreSQL + Redis funcionando	                  ✅
Migraciones y datos semilla	                     ✅
Endpoints /api/categories, /api/posts, /healthz	 ✅
Caché en categorías y detalle de posts	          ✅
Logging JSON	                                    ✅
Docker Compose operativo	                        ✅
```
## RESPUESTA EN LA TERMINAL

# correr contenedores
<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/ebffa716-6ea7-4408-b59e-5be678cf0b68" />

# ver contenedores
<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/d9e65640-6503-478c-8d55-0d0db354f7c3" />

# ver bd y redis
<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/91e2fc2e-473c-43e1-886a-2046bcaab072" />

# endpoitn para listar categoiras
<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/2a58587d-571b-4173-8e90-d288ca7d91fa" />

# endpoint para lista paginada de posts
<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/897a191e-b525-415e-88ab-436eeea39bae" />

# endpoint para detalle de post
<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/b5f476e3-c3b4-4bdb-a0b7-da67d0b99643" />

# shell - cantidad de registros
<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/68b8cbaa-c8f4-402c-a66f-306a0f81241c" />

# vista - docker
<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/cad036b9-1889-4c7e-8859-23a29904505a" />







