# Libreria Online — Taller TiDB

### Integrantes
- Edwar Esteban Fonseca Jimenez
- David Sebastian Quijano Obando
- Sebastian David Lizarazo Duarte
- Jonathan David Romero Bayona
- Alejandro Huerfano Benitez

Aplicacion web de libreria online.

- **Base de datos**: TiDB (MySQL-compatible)
- **Backend**: Node.js 18+ · Express · mysql2
- **Frontend**: React 18 · Vite · React Router · axios

---

## Instancia de TiDB creada por el grupo

Ya fue creada una instancia en TiDB que configuramos y cargamos con el esquema (`db/schema.sql`) y los datos de prueba presentes en (`db/seed.sql`).


Las credenciales son las siguientes — deben ser copiadas tal cual al archivo `backend/.env`:

```env
TIDB_HOST=gateway01.us-east-1.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USER=kPFxx445k6LR63Z.root
TIDB_PASSWORD=j5Vu2MJtDAuBlXpq
TIDB_DATABASE=libreria
PORT=3001
```

> Esta instancia corre en el plan gratuito de TiDB Cloud y se pausa automaticamente por inactividad. Si aparece un error de conexion tipo `ECONNREFUSED` o `getaddrinfo`, la instancia probablemente esta pausada. Esperá 1-2 minutos, si no funciona puedes optar por el Plan B.

---

## Plan B: cómo crear una instancia propia de TiDB

Si la instancia compartida del taller está pausada y no se reanuda, se puede crear una instancia gratuita y probar la app. Hay dos caminos.

### Opcion 1 — TiDB Cloud Serverless (recomendado, gratis)

**Crear el cluster:**

1. Ir a https://tidbcloud.com y crea una cuenta.
2. Desde el dashboard principal, hacer clic en **"Create Cluster"** (o el botón **"+"**).
3. Elegir el plan **TiDB Cloud Serverless** — es el unico gratuito.
4. Selecciona una region cercana (ej: AWS / N. Virginia `us-east-1`, o Frankfurt `eu-central-1`).
5. Asignale un nombre al cluster (ej: `taller-libreria`).
6. Espera 1-2 minutos mientras se aprovisiona. El estado pasa de `CREATING` a `AVAILABLE`.

**Cargar la base de datos:**

7. Cuando esté listo, hacer clic en el cluster y en el panel izquierdo elige **"SQL Editor"**.
8. Si te pide conectarte, ingresa la password que generaste al crear el cluster.
9. Ejecuta:
   ```sql
   CREATE DATABASE IF NOT EXISTS libreria;
   USE libreria;
   ```
10. Pega todo el contenido de `db/schema.sql` y ejecuta (boton **Run** o `Ctrl+Enter`).
11. Pega todo el contenido de `db/seed.sql` y ejecuta.
12. Verifica con:
    ```sql
    SELECT COUNT(*) FROM libros;
    ```
    Debe devolver **10**.

**Obtener las credenciales para el `backend/.env`:**

13. Debe regresar al detalle del cluster → **"Connect"** → **"Standard Connection"** → **"General"**.
14. Copia los valores:
    - **Host** (ej: `gateway01.us-east-1.prod.aws.tidbcloud.com`)
    - **Port** (`4000`)
    - **User** (ej: `xxx.root`)
    - **Password** (la que generaste)
15. Reemplaza esos valores en `backend/.env` y reinicia el backend (`Ctrl+C` y `npm run dev`).

> Si tu nuevo cluster se pausa por inactividad, la opcion **"SQL Editor"** aparece grisada en el menu lateral — hay que reanudar el cluster primero desde el dashboard.

### Opcion 2 — TiDB local con Docker (sin internet)

Si tiene Docker instalado y desea evitar cualquier dependencia de la nube:

```bash
docker run -d --name tidb-local -p 4000:4000 pingcap/tidb:latest
```

Esperar unos segundos a que arranque. Despues:

1. Conectate con cualquier cliente MySQL a `127.0.0.1:4000` (usuario `root`, sin contraseña).
2. Repetir los pasos 9-12 de la opcion anterior para crear la BD y cargar el esquema.

Las variables en `backend/.env` para esta opcion:

```env
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USER=root
TIDB_PASSWORD=
TIDB_DATABASE=libreria
PORT=3001
```

> El codigo de la aplicacion no cambia entre TiDB Cloud y TiDB local — solo se modifican las 5 variables `TIDB_*` del `.env`.

---

## Requisitos previos

- **Node.js >= 18** ([descargar](https://nodejs.org))
- **Git** para clonar el repositorio
- Tres terminales abiertas (una por servicio)

---

## Estructura del proyecto

```
taller-electiva1-tidb/
├── db/                  # Esquema SQL + seed (referencia — ya cargados en la BD)
│   ├── schema.sql
│   └── seed.sql
├── backend/             # API REST (Node + Express)
│   ├── src/
│   ├── .env.example
│   └── package.json
├── frontend/            # SPA (React + Vite)
│   ├── src/
│   └── package.json
└── README.md            # este archivo (guia unica de setup y uso)
```

---

## Setup paso a paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/SebastianLizarazo/taller-electiva1-tidb.git
cd taller-electiva1-tidb
```

### 2. Configurar el backend

```bash
cd backend
cp .env.example .env
```

Edita `backend/.env` y reemplaza los valores de las variables `TIDB_*` con los de la sección **"Instancia de TiDB creada por el grupo"** de mas arriba. Tiene que quedar asi:

```env
TIDB_HOST=gateway01.us-east-1.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USER=kPFxx445k6LR63Z.root
TIDB_PASSWORD=j5Vu2MJtDAuBlXpq
TIDB_DATABASE=libreria
PORT=3001
```

Después instala dependencias:

```bash
npm install
```

### 3. Configurar el frontend

```bash
cd ../frontend
npm install
```

El frontend no necesita variables de entorno — apunta a `http://localhost:3001` por defecto (configurable en `src/api/client.js`).

---

## Cómo correr la aplicación

Necesitas **tres terminales** abiertas:

**Terminal 1 — Backend:**
```bash
cd taller-electiva1-tidb/backend
npm run dev
```
Deberias ver algo como `Server listening on port 3001`. Usa `nodemon`, asi que se reinicia solo al editar.

**Terminal 2 — Frontend:**
```bash
cd taller-electiva1-tidb/frontend
npm run dev
```
Deberias ver algo como `Local: http://localhost:5173`. Abre esa URL en el navegador.

**Terminal 3:** libre, para smoke tests o consultas SQL.

Para detener cualquier servicio: `Ctrl+C` en su terminal.

---

## Verificacion rapida

Con el backend corriendo, prueba estas URLs en el navegador:

| URL | Esperado |
|---|---|
| http://localhost:3001/health | `{"status":"ok"}` |
| http://localhost:3001/api/libros | Array con 10 libros |
| http://localhost:3001/api/autores | 5 autores |
| http://localhost:3001/api/categorias | 5 categorias |
| http://localhost:3001/api/usuarios | 4 usuarios |

---

## Recorrido funcional

Una vez en http://localhost:5173:

1. **Selecciona un usuario** en el dropdown del navbar (sin login — se elige de una lista).
2. **Explora el catalogo** — busca por titulo, filtra por categoria o autor.
3. **Hacer clic en un libro** → detalle → elige la cantidad → "Agregar al carrito".
4. **Carrito** → revisa el total → "Ir a checkout".
5. **Confirma el pedido** → se crea en TiDB con sus lineas en una sola transaccion.
6. **"Mis pedidos"** → el pedido nuevo aparece arriba con su total y lineas.

---

## API de referencia

Base URL: `http://localhost:3001`. Todas las queries usan prepared statements (placeholders `?`), nunca se concatena input del usuario al SQL.

| Metodo | Endpoint | Descripcion |
|---|---|---|
| GET | `/health` | Sanity check (no toca la BD, anda aun sin `.env`) |
| GET | `/api/autores` | Listado de autores |
| GET | `/api/categorias` | Listado de categorias |
| GET | `/api/libros?q=&categoria_id=&autor_id=` | Catalogo con filtros opcionales. Devuelve `autor_nombre` y `categoria_nombre` via JOIN |
| GET | `/api/libros/:id` | Detalle de un libro (con autor y categoria) |
| POST | `/api/libros` | Crear libro. Requeridos: `titulo`, `precio` |
| PUT | `/api/libros/:id` | Actualizar libro (mismo body que POST) |
| DELETE | `/api/libros/:id` | Eliminar libro |
| GET | `/api/usuarios` | Listado de clientes |
| POST | `/api/pedidos` | Crear pedido en transaccion. Body: `{ usuario_id, items: [{ libro_id, cantidad }] }` |
| GET | `/api/pedidos?usuario_id=` | Pedidos de un usuario (mas recientes primero) |
| GET | `/api/pedidos/:id` | Detalle de un pedido con sus lineas |



### Formato de error

Todos los errores se devuelven como JSON:

```json
{ "error": "mensaje" }
```

| Status | Significado |
|---|---|
| 400 | Campos invalidos o faltantes, stock insuficiente |
| 404 | Recurso o ruta no encontrada |
| 503 | Credenciales de BD no configuradas |
| 500 | Error inesperado del servidor |

Si no hay stock suficiente para algun item, el rollback devuelve 400 con detalle:

```json
{
  "error": "No se pudo crear el pedido",
  "details": [
    { "libro_id": 7, "titulo": "Rayuela", "solicitado": 99, "disponible": 7, "motivo": "Stock insuficiente" }
  ]
}
```

---

## Decisiones tecnicas relevantes

- **Sin autenticacion**: el taller es de TiDB, no de auth. La tabla `usuarios` es solo un directorio de clientes — el usuario se elige de un dropdown en el navbar.
- **Transacciones atomicas en pedidos**: `POST /api/pedidos` valida y decrementa stock dentro de una sola transaccion con `SELECT ... FOR UPDATE` + `UPDATE ... WHERE stock >= ?` (doble cerrojo contra race conditions).
- **Precios siempre server-side**: el cliente nunca envia el precio — el backend lo computa desde la tabla `libros` para evitar manipulacion.
- **CORS preconfigurado**: el backend ya permite requests desde `http://localhost:5173` (Vite default).
- **Pool lazy**: el pool de mysql2 no conecta al arrancar el servidor, asi que el back levanta sin `.env` y devuelve 503 con mensaje claro cuando se hace una query sin configurar.

---

## Modelo de datos

```
autores ──< libros >── categorias
            │
            └──< detalle_pedidos >── pedidos >── usuarios
```

## Respuesta a las preguntas de clase

**¿Qué diferencia hay entre Neon y una VM tradicional con PostgreSQL?**

La principal diferencia es que mientras una máquina virtual tradicional acopla el cómputo y el almacenamiento en una sola sintancia fija, Neon usa un modelo serverless que separa el motor 
de procesamiento del almacenamiento distribuido. En una VM uno se debe encargar de la administración del sistema operativo, hacer la distribución de recursos de manera manual, gestionar 
los parches de seguridad y los respaldos. En cambio, Neon es una solución ya totalmente administrada que escala de manera automática.

**¿Qué ventajas tiene el branching en BD en la nube?**

La mayor ventaja es que nos permite trabajar con bases de datos igual a como lo hacemos con ramas en Git. Podemos sacar una copia instantánea e independiente de la base de datos de producción para hacer pruebas o desarrollar nuevas funcionalidades sin miedo a dañar los datos reales. Además, al usar Copy-on-Write, no se duplica toda la información desde cero, sino que solo se almacena lo que modificamos en esa rama, ahorrando bastante espacio y facilitando la integración con entornos de prueba y pipelines de integración continua.

**¿Qué riesgos existen al usar DBaaS?**

Uno de los riesgos más comunes es el vendor lock-in, ya que al depender de herramientas o configuraciones propias de un proveedor específico se vuelve complicado migrar la base de datos a otro servicio o a servidores propios en el futuro. También perdemos el control a bajo nivel, pues no podemos modificar parámetros avanzados del sistema operativo ni instalar extensiones que el proveedor no soporte de forma nativa.

Otro factor importante son los costos variables, porque al cobrarse por métricas de consumo (como lecturas/escrituras o ancho de banda), una mala optimización de consultas o un pico inesperado de tráfico puede disparar la factura. Además, al delegar la infraestructura a un tercero, siempre se debe tener en cuenta el cumplimiento normativo sobre la privacidad y la soberanía de los datos.

**¿Dónde se aplicaría GitOps en bases de datos?**

GitOps se aplica usando un repositorio de Git como la única fuente de verdad para definir y versionar todo lo relacionado con la base de datos. Se utiliza principalmente para gestionar los esquemas y las migraciones como código (Database-as-Code); así, cualquier cambio en las tablas o procedimientos pasa por un pull request, se revisa entre el equipo y se aplica automáticamente en el entorno correspondiente mediante pipelines de CI/CD.

También se aplica en el aprovisionamiento de la propia infraestructura mediante herramientas de Infraestructura como Código (IaC), permitiendo declarar instancias, réplicas, roles de usuario y permisos en archivos de configuración que se sincronizan de forma automatizada y auditable.