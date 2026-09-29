# Recolector de Sismos — USGS → TiDB Cloud

Proyecto del curso **Manejo de Base de Datos**.

Un script en Python consulta periódicamente la API pública de sismos del **USGS**
(United States Geological Survey) y guarda cada evento nuevo en una base de datos
relacional alojada gratuitamente en la nube, administrada desde un gestor web.

## Arquitectura

```
        ┌──────────────────────┐
        │   USGS Earthquake    │   API pública, sin API key
        │      GeoJSON API     │
        └──────────┬───────────┘
                   │ HTTPS
                   ▼
        ┌──────────────────────┐
        │   fetch_sismos.py    │   Python: descarga, normaliza y deduplica
        └──────────┬───────────┘
                   │ MySQL protocol sobre TLS
                   ▼
        ┌──────────────────────┐
        │   TiDB Cloud Starter │   Base de datos + SQL Editor web
        │      tabla `sismos`  │
        └──────────────────────┘

  Ejecución periódica: GitHub Actions (cron cada 15 min) o `--interval` en local
```

## Servicio de hosting elegido

**[TiDB Cloud Starter](https://tidbcloud.com/)** (de PingCAP), con su **SQL Editor**
web como gestor de la base de datos — el equivalente a phpMyAdmin.

Por qué se eligió:

| Criterio | TiDB Cloud Starter |
|---|---|
| Costo | Gratis permanente, sin tarjeta de crédito |
| Almacenamiento | 25 GiB |
| Gestor web | SQL Editor integrado en la consola (crear tablas, consultar, ver resultados) |
| Compatibilidad | Habla el protocolo MySQL: misma sintaxis SQL y mismo driver de Python |
| Conexión remota | Sí, cifrada con TLS |
| Respaldo institucional | PingCAP, empresa establecida; TiDB es un proyecto open source con +40k estrellas en GitHub |

Se descartaron otras alternativas de "free hosting con phpMyAdmin":

- **db4free.net** — el dominio está comprometido y hoy redirige a contenido no relacionado. Descartado por seguridad.
- **freedb.tech** — las bases gratuitas se autoeliminan a los 7 días, incompatible con una recolección continua.
- **InfinityFree** — ofrece phpMyAdmin real, pero bloquea conexiones MySQL remotas en el plan gratuito, así que el script de Python no podría conectarse.

## Fuente de datos

`https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson`

Feed oficial del USGS con los sismos registrados en la última hora a nivel mundial,
en formato GeoJSON. Es de dominio público y no requiere API key ni autenticación.

## Estructura de la tabla `sismos`

Definida en [`schema.sql`](schema.sql):

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | VARCHAR(50) | ID único del evento en USGS — **llave primaria** |
| `magnitud` | DECIMAL(3,1) | Magnitud del sismo |
| `tipo_magnitud` | VARCHAR(10) | Escala usada (ml, mw, md, …) |
| `lugar` | VARCHAR(255) | Descripción de la ubicación |
| `tiempo_evento` | DATETIME | Fecha/hora (UTC) en que ocurrió el sismo |
| `latitud` | DECIMAL(9,6) | Latitud del epicentro |
| `longitud` | DECIMAL(9,6) | Longitud del epicentro |
| `profundidad_km` | DECIMAL(6,2) | Profundidad en kilómetros |
| `url` | VARCHAR(255) | Enlace al detalle del evento en USGS |
| `fecha_insercion` | TIMESTAMP | Cuándo lo guardó el script (automático) |

**Deduplicación:** el `id` del USGS es la llave primaria y el script usa
`INSERT IGNORE`, así que ejecutar el recolector muchas veces nunca duplica un
sismo ya registrado. Como los feeds se traslapan entre ejecuciones, esto es
esencial para mantener la tabla consistente.

**Índices:** se indexan `tiempo_evento` y `magnitud`, que son los campos por los
que se filtran las consultas más comunes (sismos por rango de fechas o por
magnitud mínima).

## Manejo de credenciales

Las credenciales **nunca** están en el código ni en el historial de git:

- **En local:** se leen de un archivo `.env`, que está listado en [`.gitignore`](.gitignore) y por lo tanto nunca se sube al repositorio. El repo solo incluye [`.env.example`](.env.example), una plantilla con valores ficticios.
- **En la nube:** el workflow de GitHub Actions las inyecta como variables de entorno desde **GitHub Secrets**, que están cifrados y no son visibles ni en el código ni en los logs.

## Instalación

1. Crear el cluster gratuito en [TiDB Cloud](https://tidbcloud.com/) y la base de datos.
2. Crear la tabla ejecutando el contenido de `schema.sql` en el **SQL Editor** de la consola.
3. Configurar las credenciales locales:

   ```bash
   cp .env.example .env
   ```

   Y llenar `.env` con los datos reales que da TiDB Cloud en el botón **Connect**.

4. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Una sola ejecución (útil para probar):

```bash
python fetch_sismos.py
```

Ejecución periódica en local, consultando cada 10 minutos:

```bash
python fetch_sismos.py --interval 600
```

Ejecución periódica en la nube: el workflow
[`.github/workflows/recolectar-sismos.yml`](.github/workflows/recolectar-sismos.yml)
corre el script **cada 15 minutos** automáticamente vía GitHub Actions, sin
necesidad de mantener la computadora encendida. También puede dispararse a
mano desde la pestaña *Actions* del repositorio.

**Nota sobre la puntualidad:** GitHub no garantiza que un `cron` programado
dispare siempre a tiempo — bajo carga alta, el evento se descarta en vez de
encolarse (documentado en la
[documentación oficial de GitHub Actions](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)).
Programarlo cada hora dejaba huecos de hasta 5 horas cuando un disparo se
perdía. Corriendo cada 15 minutos, si un disparo se pierde el siguiente llega
poco después en vez de una hora (o más) después — la recolección se vuelve
mucho más consistente sin depender de que GitHub cumpla el horario exacto.

## Consultas de ejemplo

```sql
-- Los 10 sismos más fuertes registrados
SELECT lugar, magnitud, tiempo_evento
FROM sismos
ORDER BY magnitud DESC
LIMIT 10;

-- Cantidad de sismos por día
SELECT DATE(tiempo_evento) AS dia, COUNT(*) AS total
FROM sismos
GROUP BY dia
ORDER BY dia DESC;

-- Sismos significativos (magnitud 4.5+)
SELECT lugar, magnitud, profundidad_km, tiempo_evento
FROM sismos
WHERE magnitud >= 4.5
ORDER BY tiempo_evento DESC;
```
