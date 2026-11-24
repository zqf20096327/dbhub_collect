# Gowayki Nest — Backend del panel

API REST del panel de administración de Gowayki Nest. Está construida con Django y Django REST Framework.

## Tecnologías

- Python 3.12
- Django 5.1 y Django REST Framework
- PostgreSQL 15 + PostGIS
- drf-spectacular para la documentación de la API

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone git@github.com:VizcardoFabrizzio/gowayki-nest-admin-back.git
   cd gowayki-nest-admin-back
   ```

2. Crear el entorno virtual e instalar las dependencias:

   ```powershell
   py -3.12 -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Copiar `.env.example` a `.env` y completar los datos de la base.

4. Levantar el servidor:

   ```powershell
   python manage.py runserver 8000
   ```

## Endpoints

- `GET /api/estado`: comprueba que la API está en línea.
- `GET /api/docs/`: documentación interactiva de la API.

## Estructura

El código está separado en carpetas para que cada parte tenga una tarea clara:

- `config\`: configuración de Django y rutas principales.
- `core\`: app base del proyecto.
- `src\domain\`: entidades y reglas del negocio.
- `src\application\`: casos de uso y reglas de sistema.
- `src\infrastructure\`: acceso a la base de datos y repositorios.
- `src\presentation\`: endpoints, serializers y manejo de errores.

## Historial de cambios

Los cambios los registro en commits granulares (son pequeños y verificables): cada uno
agrega o modifica una parte concreta de un módulo. Lo que me facilita a futuro
revisar, entender y revertir cambios.
