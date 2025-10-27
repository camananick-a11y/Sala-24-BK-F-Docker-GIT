# Sala-24-BK-F-Docker-GIT

#  Laboratorio de Microservicios (Django + React)

##  Día 1 — Fundamentos + Entorno Docker / Git

#  Día 2 — Microservicio de Autenticación con Docker y PostgreSQL

##  Objetivo
Implementar el microservicio **Auth Service** utilizando **Docker** y **PostgreSQL**, ejecutar las migraciones dentro del contenedor, y probar los tres endpoints principales de autenticación con **Postman**: registro de usuario, obtención de token y refresco de token.

---

##  Configuración del entorno

### 1️ Clonar el proyecto
```bash
git clone https://github.com/usuario/Sala-24-BK-F-Docker-GIT.git
cd Sala-24-BK-F-Docker-GIT/auth-service

rear entorno virtual (si aún no existe)
python -m venv venv
venv\Scripts\activate

3️ Instalar dependencias
pip install -r requirements.txt

4️ Levantar los contenedores con Docker

Desde la carpeta raíz del proyecto:

docker compose up -d


Verifica que los contenedores estén corriendo:

docker ps


 Deberías ver los contenedores:

db_postgres → PostgreSQL

cache_redis → Redis

(El Auth Service puede levantarse manualmente o integrarse en siguientes días)

 Migraciones de la base de datos

Ejecutar el contenedor del Auth Service (si está corriendo):

docker exec -it auth_service bash


Dentro del contenedor:

python manage.py makemigrations
python manage.py migrate
exit


Esto crea las tablas necesarias para la autenticación y usuarios en la base de datos PostgreSQL.

 Conexión a la base de datos

Configuración en .env:

POSTGRES_DB=auth_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_HOST=db_postgres
POSTGRES_PORT=5432


El microservicio Auth utiliza estas variables de entorno para conectarse a PostgreSQL dentro del contenedor.

 Endpoints implementados y probados
Acción	Método	Endpoint	Descripción
Registro de usuario	POST	/api/register/	Crea un nuevo usuario
Obtener token JWT	POST	/api/token/	Devuelve access y refresh token
Refrescar token	POST	/api/token/refresh/	Genera un nuevo access token usando el refresh
 Pruebas en Postman
 1. Registro de usuario

POST /api/register/

Body (JSON):

{
  "username": "usuario1",
  "email": "usuario1@example.com",
  "password": "12345678"
}


Respuesta esperada:

{
  "message": "User registered successfully"
}

 2. Obtener Token JWT

POST /api/token/

Body (JSON):

{
  "username": "usuario1",
  "password": "12345678"
}


Respuesta esperada:

{
  "access": "<ACCESS_TOKEN>",
  "refresh": "<REFRESH_TOKEN>"
}

 3. Refrescar Token

POST /api/token/refresh/

Body (JSON):

{
  "refresh": "<REFRESH_TOKEN>"
}


Respuesta esperada:

{
  "access": "<NEW_ACCESS_TOKEN>"
}

 Base de datos PostgreSQL

Motor: PostgreSQL 15

Contenedor: db_postgres

Puerto: 5432

Usuario y contraseña: Definidos en .env

Las tablas se crean correctamente después de ejecutar las migraciones del Auth Service.

 Evidencias recomendadas

Incluye en tu entrega o commit:

Captura del comando docker ps mostrando los contenedores activos (db_postgres, cache_redis).

Captura del comando docker-compose ps mostrando los mismos servicios.

Capturas de Postman:

Registro exitoso de usuario.

Obtención del token JWT.

Refresco del token.

Log de migraciones exitosas en consola.

 Resultado final del Día 2

Al finalizar este día:

 PostgreSQL y Redis están ejecutándose correctamente en contenedores Docker.

 Migraciones del servicio de autenticación completadas con éxito.

 Endpoints /api/register/, /api/token/ y /api/token/refresh/ funcionan correctamente en Postman.

 El microservicio Auth Service está completamente funcional y conectado a la base de datos Dockerizada.
