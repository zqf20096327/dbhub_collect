# n8n Base Config Alcore

Repositorio base para levantar un entorno local de automatizacion con **n8n**, **PostgreSQL**, **Node.js** y **ngrok** usando Docker.

La idea es que cualquier estudiante pueda clonar el repositorio, ejecutar un comando y empezar a practicar sin instalar cada herramienta manualmente.

## Que incluye

- n8n listo en `http://localhost:5678`
- PostgreSQL listo en `localhost:5433` desde tu computadora
- API Node.js de prueba lista en `http://localhost:3000`
- ngrok preparado para publicar n8n cuando se necesite probar webhooks externos
- Base de datos inicial con tablas de practica
- Archivo `.env.example` con valores locales faciles de entender
- Scripts para crear `.env` y reiniciar el entorno
- Documentacion paso a paso para estudiantes

## Requisitos

Antes de empezar necesitas:

1. Tener instalado **Docker Desktop**.
2. Tener instalado **Git**.
3. Tener una terminal disponible:
   - Windows: PowerShell, Git Bash o terminal de VS Code.
   - macOS: Terminal.
   - Linux: Terminal.

No necesitas instalar n8n, PostgreSQL ni Node.js en tu computadora. Docker se encarga.

## Inicio rapido

Clona el repositorio:

```bash
git clone https://github.com/anndreloopez012/n8n-base-config-alcore.git
cd n8n-base-config-alcore
```

### Opcion mas rapida

macOS o Linux:

```bash
chmod +x start.sh scripts/*.sh
./start.sh
```

Windows PowerShell:

```powershell
.\start.ps1
```

El script hace esto por ti:

- valida que Docker este corriendo
- crea `.env` si no existe
- valida `docker-compose.yml`
- levanta los servicios
- muestra las URLs de trabajo

### Opcion directa con Docker

Tambien puedes levantar todo con:

```bash
docker compose up -d
```

Espera unos segundos y abre:

- n8n: http://localhost:5678
- API Node.js: http://localhost:3000
- Health check de Node.js: http://localhost:3000/health

Verifica contenedores:

```bash
docker compose ps
```

Si todos aparecen como `running` o `healthy`, el entorno esta listo.

Guia corta de comandos:

```text
docs/COMANDOS-RAPIDOS.md
```

## Crear el archivo .env

El proyecto funciona aunque no tengas `.env`, porque `docker-compose.yml` trae valores locales por defecto.

Pero lo recomendado es crear tu propio `.env`:

### macOS o Linux

```bash
chmod +x scripts/setup-env.sh
./scripts/setup-env.sh
```

### Windows PowerShell

```powershell
copy .env.example .env
```

Luego puedes levantar el entorno:

```bash
docker compose up -d
```

## Accesos locales

### n8n

URL:

```text
http://localhost:5678
```

La primera vez n8n te pedira crear un usuario administrador local.

### PostgreSQL

Valores por defecto:

```text
Host: localhost
Puerto: 5433
Base de datos: n8n_alcore
Usuario: alcore
Password: alcore_local_123
```

Nota: dentro de Docker, PostgreSQL sigue usando el puerto `5432`. El cambio a `5433` aplica solo cuando te conectas desde tu computadora para evitar conflictos con instalaciones locales de PostgreSQL.

Desde dentro de Docker, otros servicios se conectan usando:

```text
Host: postgres
Puerto: 5432
```

### Node.js

URL:

```text
http://localhost:3000
```

Endpoints utiles:

```text
GET  /health
GET  /api/ping
POST /api/webhook-test
```

Ejemplo para probar desde terminal:

```bash
curl http://localhost:3000/api/ping
```

Ejemplo para guardar un evento en PostgreSQL:

```bash
curl -X POST http://localhost:3000/api/webhook-test \
  -H "Content-Type: application/json" \
  -d '{"student":"demo","topic":"n8n","status":"testing"}'
```

## Usar ngrok

ngrok sirve para exponer tu n8n local a internet. Esto es util cuando un servicio externo necesita enviar datos a tu webhook de n8n.

Importante: ngrok necesita un token gratuito de tu cuenta.

1. Crea una cuenta en https://ngrok.com
2. Copia tu authtoken desde el dashboard.
3. Crea tu `.env`.
4. Edita esta variable:

```env
NGROK_AUTHTOKEN=CAMBIAR_POR_TU_TOKEN_GRATUITO_DE_NGROK
```

Levanta ngrok:

```bash
docker compose --profile tunnel up -d
```

Mira los logs para copiar la URL publica:

```bash
docker compose logs -f ngrok
```

Cuando tengas la URL de ngrok, actualiza tu `.env`:

```env
WEBHOOK_URL=https://tu-url-de-ngrok.ngrok-free.app/
N8N_EDITOR_BASE_URL=https://tu-url-de-ngrok.ngrok-free.app/
```

Reinicia n8n:

```bash
docker compose restart n8n
```

## Comandos principales

Levantar:

```bash
docker compose up -d
```

Ver estado:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f
```

Ver logs solo de n8n:

```bash
docker compose logs -f n8n
```

Detener sin borrar datos:

```bash
docker compose down
```

Detener y borrar datos locales:

```bash
./scripts/reset-local.sh
```

## Estructura del proyecto

```text
n8n-base-config-alcore/
├── docker-compose.yml
├── .env.example
├── README.md
├── CONTRIBUTING.md
├── Makefile
├── start.sh
├── start.ps1
├── docs/
│   ├── COMANDOS-RAPIDOS.md
│   ├── INSTALACION-PASO-A-PASO.md
│   ├── GUIA-N8N-NGROK.md
│   └── SOLUCION-DE-PROBLEMAS.md
├── node-app/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       └── server.js
├── postgres/
│   └── init/
│       └── 001-create-learning-schema.sql
└── scripts/
    ├── setup-env.sh
    └── reset-local.sh
```

## Flujo recomendado para estudiantes

1. Clona el repo.
2. Entra a la carpeta.
3. Ejecuta `docker compose up -d`.
4. Abre n8n.
5. Crea tu usuario local.
6. Prueba la API Node.js con `/api/ping`.
7. Crea tu primer workflow en n8n.
8. Si necesitas recibir webhooks externos, configura ngrok.

## Buenas practicas

- No subas tu archivo `.env`.
- No compartas tu token de ngrok.
- No borres los volumenes si quieres conservar workflows y credenciales.
- Usa `docker compose down` para apagar sin perder datos.
- Usa `scripts/reset-local.sh` solo cuando quieras empezar desde cero.
- Si cambias `N8N_ENCRYPTION_KEY` despues de guardar credenciales en n8n, puedes perder acceso a esas credenciales.

## Referencias oficiales

- n8n Docker: https://docs.n8n.io/hosting/installation/docker/
- n8n PostgreSQL: https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/database/
- ngrok Docker: https://ngrok.com/docs/using-ngrok-with/docker/
- Docker Compose variables: https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/
