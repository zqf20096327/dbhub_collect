# OpenSensorNet

Una red abierta de sensores ciudadanos. Cualquier persona con un teléfono, una
Raspberry Pi o un microcontrolador ESP32 puede mandar una lectura — calidad de
aire, ruido, temperatura, radiación, humedad del suelo, lo que sea — a una API
pública, y verla al instante en un mapa en vivo.

**Todo es gratis y abierto.** Exportar datos, ver analíticas, configurar
alertas — no hay una versión "premium" escondida. Redes de datos abiertos
serias (PurpleAir, Sensor.Community, Safecast, OpenAQ) funcionan así, y
cobrar por eso rompe la confianza que hace que la gente sume su sensor a la
red.

## Qué incluye

| Endpoint | Qué hace |
|---|---|
| `POST /devices` | Registrar un dispositivo y obtener un token (opcional) |
| `POST /readings` | Mandar una lectura |
| `GET /readings` | Listar lecturas recientes (con paginación) |
| `GET /sensor_types` | Ver qué tipos de sensor hay en la red |
| `GET /export.csv` | Bajar el dataset completo en CSV |
| `GET /analytics/hourly-summary` | Promedio/mín/máx por hora para un sensor |
| `POST /alerts` | Registrar un webhook que se dispara al cruzar un umbral |
| `GET /health` | Chequeo de salud del servidor |

## Anti-spam, no anti-usuario

No hay paywall, pero sí hay un límite de **120 requests/hora por IP** para
evitar que alguien inunde la base de datos, y un sistema de **tokens de
dispositivo opcional**: si registrás tu `device_id` con `POST /devices`,
nadie más puede mandar datos falsos haciéndose pasar por tu sensor. Si no lo
registrás, tu `device_id` funciona igual — primero en llegar, primero en
usarlo — así no hay barrera para probar la API.

## Cómo correrlo en 2 minutos

**Con Docker (recomendado para producción):**
```bash
docker compose up
```
Eso levanta la API en `http://localhost:8000` con los datos persistidos en un
volumen, listo para instalar en el servidor de un municipio, escuela u ONG
sin que necesiten saber Python.

**Sin Docker (para desarrollo):**
```bash
pip install -r requirements.txt --break-system-packages
uvicorn backend.main:app --reload --port 8000
```

Abrí `dashboard/index.html` en el navegador y apuntá el campo "servidor de la
api" a `http://localhost:8000`. Documentación interactiva en
`http://localhost:8000/docs`.

## Ejemplo de uso completo

```bash
# 1. Registrar tu dispositivo (opcional pero recomendado)
curl -X POST http://localhost:8000/devices \
  -H "Content-Type: application/json" \
  -d '{"device_id":"mi-sensor-casa","owner_label":"tu@email.com"}'
# -> te devuelve un token, guardalo

# 2. Mandar una lectura con tu token
curl -X POST http://localhost:8000/readings \
  -H "Content-Type: application/json" -H "X-Device-Token: dev_xxx..." \
  -d '{"device_id":"mi-sensor-casa","lat":-16.5,"lon":-68.15,"sensor_type":"air_quality_pm25","value":18.5,"unit":"ug/m3"}'

# 3. Exportar todos los datos
curl http://localhost:8000/export.csv -o datos.csv

# 4. Crear una alerta (te avisa por webhook si el PM2.5 supera 25)
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{"sensor_type":"air_quality_pm25","threshold":25,"direction":"above","webhook_url":"https://tu-servidor.com/webhook"}'
```

O usá el script de conveniencia:
```bash
python3 cli/submit.py --server http://localhost:8000 \
    --device mi-primer-sensor --lat -16.5 --lon -68.15 \
    --type temperatura_c --value 22.3 --unit "°C"
```

## Administración

```bash
python3 scripts/admin.py devices    # ver dispositivos registrados
python3 scripts/admin.py summary    # cantidad de lecturas por tipo de sensor
```

## Tests

```bash
pytest tests/ -v
```

## Cómo conectar un sensor real

- **Raspberry Pi / ESP32**: leé el sensor con tu código y hacé un `POST` a
  `/readings` (mirá `cli/submit.py` como referencia).
- **Teléfono (Termux en Android)**: instalá Python, copiá `cli/submit.py` y
  corré el mismo comando, leyendo el sensor que quieras (micrófono para
  ruido, cámara para luz, etc.).
- **Cron job**: agregá el comando de `submit.py` a tu crontab para mandar
  lecturas automáticamente cada X minutos.

## Estructura

```
opensensornet/
├── backend/
│   ├── main.py       API en FastAPI: todos los endpoints, todos gratis
│   ├── models.py     Modelos de datos y validación
│   └── auth.py       Rate limiting + tokens de dispositivo (anti-spam)
├── scripts/
│   └── admin.py      Ver dispositivos y estadísticas (para quien hostea)
├── cli/
│   └── submit.py     Mandar una lectura desde cualquier dispositivo
├── dashboard/
│   └── index.html    Mapa en vivo, un solo archivo, sin build
├── tests/
│   └── test_api.py   Suite de tests automatizados
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Cómo se puede monetizar esto (honestamente)

No cobrando por usar la red — eso choca con la cultura de datos abiertos y no
tenés todavía el efecto de red que justificaría que alguien pague por acceso.
Donde sí hay negocio real, una vez que el proyecto tenga tracción:

- **Hosting gestionado**: un municipio, escuela u ONG paga para que vos les
  instales y mantengas su propia instancia (con `docker compose up` ya es
  trivial hacerlo). Cobrás por el servicio, no por el software.
- **Consultoría e integración**: te pagan para conectar sus sensores
  existentes a la red, o para construirles un dashboard a medida.
- **Venta de hardware**: kits de sensor + cable + instrucciones, con margen
  sobre el costo (así funciona Smart Citizen Kit).
- **Grants y financiamiento**: proyectos de ciencia ciudadana suelen
  financiarse con fondos ambientales o de investigación, no con
  suscripciones a usuarios individuales.

## Roadmap

- [ ] Migrar de SQLite a Postgres cuando el volumen de datos crezca.
- [ ] Agregaciones espaciales (promedio por zona/barrio) para que el mapa no
      se sature con miles de puntos.
- [ ] Dataset público diario (CSV/Parquet) generado automáticamente.
- [ ] Panel de administración web (hoy `scripts/admin.py` es solo CLI).

## Contribuir

Pull requests bienvenidos. El objetivo es que esto siga siendo útil y
gratuito para cualquiera que quiera sumar datos.

## Licencia

MIT — usalo, modificalo, vendé servicios de hosting o consultoría alrededor.
El software en sí siempre queda abierto.
