<p align="center">

# 🎓 Sistema Integral de Gestión de Asistencia Escolar

> 🖥️ App de escritorio + 🔌 API REST + 📱 App móvil para digitalizar el control de asistencia. Proyecto académico EEST (EACP).

![C#](https://img.shields.io/badge/C%23-.NET_Framework_4.7.2-239120?logo=csharp&logoColor=white)
![WinForms](https://img.shields.io/badge/UI-Windows_Forms_+_MaterialSkin-blue)
![MySQL](https://img.shields.io/badge/DB-MySQL-4479A1?logo=mysql&logoColor=white)
![MongoDB](https://img.shields.io/badge/Auth-MongoDB-47A248?logo=mongodb&logoColor=white)
![Node](https://img.shields.io/badge/API-Node.js_+_Express-339933?logo=node.js&logoColor=white)
![Expo](https://img.shields.io/badge/App-Expo_SDK_57-000020?logo=expo&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-En_desarrollo-yellow)
![PRs](https://img.shields.io/badge/PRs_a-main-blueviolet)

</p>

## 📑 Índice

- [1. Descripción del proyecto](#1-descripción-del-proyecto)
- [2. Problemática](#2-problemática)
- [3. Alcance y funcionalidades](#3-alcance-y-funcionalidades)
- [4. Usuarios y roles](#4-usuarios-y-roles)
- [5. Tecnologías y arquitectura](#5-tecnologías-y-arquitectura)
- [6. Estructura del proyecto](#6-estructura-del-proyecto)
- [7. Requisitos previos](#7-requisitos-previos)
- [8. Instalación y configuración](#8-instalación-y-configuración)
- [9. Uso del sistema](#9-uso-del-sistema)
- [10. Metas y factores críticos de éxito](#10-metas-y-factores-críticos-de-éxito)
- [11. Cronograma](#11-cronograma)
- [12. Costos](#12-costos)
- [13. Roadmap](#13-roadmap)
- [14. Equipo y contexto académico](#14-equipo-y-contexto-académico)
- [15. Licencia](#15-licencia)
- [16. Flujo de trabajo Git](#16-flujo-de-trabajo-git)
- [17. Documentación adicional](#17-documentación-adicional)

**Leyenda:** 🔴 riesgo o prohibido · 🟡 pendiente o con salvedad · 🟢 seguro u opcional

---

## 1. Descripción del proyecto

🏫 Actualmente el control de asistencia en la institución se realiza mayormente **en papel** 📝, lo que genera desorganización, riesgo de pérdida de datos, errores humanos y demora en los reportes.

✨ Este proyecto desarrolla un **sistema integral de gestión de asistencia escolar** compuesto por:

| Módulo | Carpeta | Descripción |
|---|---|---|
| 🖥️ **Aplicativo de escritorio** | `Escritorio/` | Gestión institucional: alumnos, profesores, preceptores, cursos, materias, dictados, inscripciones y usuarios |
| 🔌 **API REST** | `Api/` | Expone los datos a la app, emite eventos en tiempo real (SSE) y gestiona clases con token QR |
| 📱 **App móvil** | `App/` | Registro de asistencia desde el celular (escaneo QR o código corto) |

🎯 **Objetivo:** digitalizar el registro diario, mejorar la disponibilidad de la información y automatizar reportes en una plataforma segura y organizada.

## 2. Problemática

**😞 Puntos débiles del sistema actual:**
- 📝 Registro en papel, con riesgo de pérdida y deterioro
- 🔍 Dificultad para consultar historial de asistencias
- 🐌 Procesos administrativos lentos
- ✍️ Errores en la carga manual de datos
- 📊 Sin validaciones automáticas ni reportes inmediatos
- 🗂️ Dependencia total de documentación física

**💪 Puntos fuertes que se conservan:**
- 🧑‍🏫 Experiencia de preceptores y docentes en la toma de asistencia
- 🏛️ Estructura organizacional claramente definida
- 📏 Reglas institucionales de asistencia/inasistencias ya conocidas
- 🧱 Metodología de trabajo establecida como base del nuevo sistema

## 3. Alcance y funcionalidades

### 🖥️ Escritorio (WinForms)

| Módulo | Descripción |
|---|---|
| 🔐 Autenticación | Login de usuarios con control de sesión |
| 🆕 Primer usuario | Creación del primer Administrador si no existen usuarios |
| 👥 Usuarios y perfiles | Alta, baja, modificación y activación/desactivación |
| 🎒 Alumnos | ABM completo de alumnos |
| 👨‍🏫 Profesores | ABM completo de profesores |
| 📋 Preceptores | ABM completo (contraseña bcrypt compatible con la API) |
| 🏫 Cursos / Especialidades | Administración de cursos y especialidades |
| 📚 Materias | ABM con asignación de especialidad |
| 🗓️ Dictados | Gestión de dictados (materia + profesor + preceptor) |
| ✏️ Inscripciones | Inscripción de alumnos a dictados |
| 🛡️ Permisos | Control de acceso según rol (menú filtrado en `FrmPrincipal`) |

### 🔌 API (`Api/`, puerto `3000`)

| Endpoint | Descripción |
|---|---|
| `GET /api/health` | 💚 Verifica que el servidor responde |
| `GET /api/alumnos` | 🎒 Lista alumnos (MySQL) |
| `POST /api/login` | 🔐 Autenticación por rol: preceptor, profesor o alumno |
| `GET /api/dictados` (+ `/:id/alumnos`, `/alumno/:idAlumno`) | 🗓️ Dictados e inscriptos |
| `GET /api/asistencia` · `POST /api/asistencia` · `POST /api/asistencia/lote` | ✅ Consulta y alta de asistencias |
| `GET /api/clases?fecha=` · `POST /api/clases` · `PATCH /api/clases/:id` | 🏫 Apertura y estados de clase |
| `POST /api/clases/:id/token` · `.../escanear` · `POST /api/clases/ingresar` | 📷 Token QR, escaneo y código corto |
| `GET /api/eventos` | 📡 Eventos en tiempo real (SSE, autenticado) |

### 📱 App móvil (`App/`)

| Pantalla | Rol |
|---|---|
| 📋 `PreceptorPrincipal` | Preceptor: clases y asistencia |
| 👨‍🏫 `ProfesorPrincipal` | Profesor: sus dictados y clases |
| 🎒 `AlumnoPrincipal` | Alumno: escaneo QR e ingreso con código |

## 4. Usuarios y roles

| Rol | Permisos |
|---|---|
| ⭐ **Administrador** | Configuración general, gestión de usuarios y mantenimiento (solo escritorio) |
| 🏛️ **Directivo** | Datos institucionales y consultas generales |
| 📋 **Preceptor** | Registro y seguimiento de asistencias (escritorio + app) |
| 👨‍🏫 **Profesor** | Carga de asistencia de sus clases (escritorio + app) |
| 🎒 **Alumno** | Registra su asistencia escaneando el QR (app) |

> 🟡 El menú principal (`FrmPrincipal`) aplica permisos automáticamente: el módulo de usuarios solo es visible para el Administrador. El login de la API solo contempla preceptor, profesor y alumno (no hay rol administrador en la API).

## 5. Tecnologías y arquitectura

**🖥️ Escritorio (`Escritorio/`):**
- 💬 **Lenguaje:** C# .NET Framework 4.7.2
- 🪟 **Interfaz:** Windows Forms + MaterialSkin.2
- 🗄️ **Base relacional:** MySQL `gestion_asistencia_eest`
- 🍃 **Base documental:** MongoDB Atlas (usuarios y autenticación del escritorio)
- 📦 **Drivers:** `MySql.Data` + `MongoDB.Driver` (+ `CryptSharpOfficial` **2.1.0.0** para bcrypt)
- 🧰 **IDE:** Visual Studio (workload .NET desktop development)
- 🧱 **Arquitectura:** en capas tipo MVC

**🔌 API (`Api/`):**
- 🟢 Node.js + Express 5, `mysql2`, `bcryptjs`, `cors`, `dotenv`
- Lee/escribe el mismo MySQL que el escritorio (única fuente de verdad compartida)

**📱 App (`App/`):**
- ⚛️ React Native con Expo SDK 57, React 19
- 📷 Cámara (`expo-camera`) para escaneo QR, eventos en tiempo real (SSE)

**🧱 Capas del escritorio:**

```text
Vista (Forms) <-> Controlador (lógica) <-> Modelo (Entidades + DAO + Conexión)
```

- 🧬 **Entidades:** `Alumno`, `Profesor`, `Preceptor`, `Materia`, `Especialidad`, `Dictado`, `Inscripcion`, `Asistencia`, `Usuario`, `Rol`
- 🗃️ **DAO:** `AlumnoDAO`, `ProfesorDAO`, `PreceptorDAO`, `MateriaDAO`, `EspecialidadDAO`, `DictadoDAO`, `InscripcionDAO` (MySQL) y `UsuarioDAO` (MongoDB)
- 🔌 **Conexión:** `conexionBD.cs` (MySQL), `ConexionMongo.cs` (Atlas) y `Credenciales.cs`, que lee el archivo de credenciales ignorado por git
- 🎮 **Controlador:** `Alumno`, `Profesor`, `Preceptor`, `Materia`, `Especialidad`, `Dictado`, `Inscripcion`, `Usuario`
- 🪟 **Vista:** `FrmLogin`, `FrmPrincipal`, `FrmInicio`, `FrmAlumnos`, `FrmProfesores`, `FrmPreceptores`, `FrmMaterias`, `FrmEspecialidades`, `FrmDictados`, `FrmInscripcion`, `FrmUsuarios`, `FrmPrimerUsuario`, `FrmConfirmarEliminar`, más los helpers `UIHelper.cs` y `CtrlTelefono.cs`
- 🧰 **Utilidades:** `Sesion` (usuario actual), `Logger` (errores en `bin/**/logs/log_*.txt`), `Ejecutor`, `DatosException`, `Tema`, `TelefonoHelper`

**🔑 Contraseñas:** las de preceptor/profesor en MySQL usan bcrypt (costo 10, prefijo `$2a$` o `$2b$` indistintamente), interoperable entre el escritorio (CryptSharp) y la API (bcryptjs).

**🔒 Credenciales:** ninguna cadena de conexión está en el código. Ver [§8.1](#81-escritorio-net) y [§8.3](#83-api-node).

## 6. Estructura del proyecto

```text
Sistema_Asistencia/
├── 📖 README.md                              # este documento
├── 📖 context.md                             # contexto técnico para humanos y agentes de IA
├── 📖 AGENTS.md                              # reglas de trabajo del agente: Git, credenciales y estilo
├── .gitignore
├── 🖥️ Escritorio/                             # módulo escritorio
│   └── SistemaAsistencia/
│       ├── SistemaAsistencia.slnx            # abrir en Visual Studio
│       ├── BD/
│       │   └── 2026-09-26_reconstruccion_definitiva.sql
│       ├── packages/                         # NuGet (se restaura, no se versiona contenido)
│       └── SistemaAsistencia/                # raíz del proyecto C#
│           ├── Program.cs
│           ├── App.config                    # solo placeholders de conexión
│           ├── packages.config
│           ├── credenciales.env.example      # plantilla versionada
│           ├── Controlador/
│           ├── Modelo/
│           │   ├── Conexion/                 # conexionBD.cs, ConexionMongo.cs, Credenciales.cs
│           │   ├── DAO/
│           │   └── Entidades/
│           ├── Vista/
│           └── Utilidades/
├── 🔌 Api/                                   # módulo API (Node/Express)
│   ├── index.js                              # bootstrap + índice de endpoints
│   ├── package.json / package-lock.json
│   ├── .env.example                          # plantilla versionada
│   ├── config/db.js                          # pool de mysql2
│   ├── rutas/                                # login, clases, dictados, asistencias, eventos
│   └── utilidades/                           # autenticacion, eventos, asistencia
├── 📱 App/                                   # módulo móvil (Expo)
│   ├── App.js
│   ├── app.json
│   ├── index.js
│   ├── package.json / package-lock.json
│   ├── .env                                  # 🔒 local, gitignored
│   ├── assets/
│   └── src/
│       ├── api.js
│       └── pantallas/                        # Alumno, Preceptor, Profesor
├── 📘 Documentacion/                         # documentación de la EACP
│   └── documentacion_munafo/
│       ├── documentacion-tecnica-munafo.md
│       └── diagramas/                        # .drawio editables + PNG
│           ├── punto_12/
│           └── punto_14/
└── .vscode/launch.json                       # debug compuesto API + App
```

> 🔒 Archivos **que no están en git** porque contienen datos locales o secretos:
> `Escritorio/SistemaAsistencia/SistemaAsistencia/credenciales.env` · `Api/.env` · `App/.env`

## 7. Requisitos previos

**🔧 Hardware:**
- 🖥️ PC con Windows 10+ (personal directivo / administrativo)
- 📱 Celular con Expo Go + PC en la misma red (app móvil)
- 🗄️ Acceso a MySQL (Railway en producción) y a MongoDB Atlas

**💿 Software:**
- 🧰 Visual Studio 2022+ (workload .NET desktop development)
- 🏗️ .NET Framework 4.7.2 Developer Pack
- 🟢 Node.js 20+ (para `Api/` y `App/`)
- 📲 Expo Go en el celular (para `App/`)
- 🐬 Cliente MySQL (Workbench o `mysql` CLI) para restaurar el script

**☁️ Para trabajar contra producción:**
- 🟡 Acceso al proyecto de Railway (API + MySQL) y a MongoDB Atlas
- 🟡 Variables de entorno configuradas en el servicio de la API (ver [§8.3](#83-api-node))

## 8. Instalación y configuración

### 8.1 Escritorio (.NET)

1. **Clonar el repositorio** en tu branch de trabajo (ver [§16](#16-flujo-de-trabajo-git)):
   ```bash
   git clone -b Juan-Torres https://github.com/JuanI19T/Sistema_Asistencia.git
   ```

2. **Abrir la solución:** `Escritorio/SistemaAsistencia/SistemaAsistencia.slnx` en Visual Studio.

3. **Restaurar paquetes NuGet** (VS lo hace automático; si no: clic derecho en la solución → *Restaurar paquetes NuGet*). Incluye `MySql.Data`, `MongoDB.Driver`, `MaterialSkin.2` y `CryptSharpOfficial` (**2.1.0.0**, fijo en `packages.config`).

4. 🔴 **Crear el archivo de credenciales.** Este paso es **obligatorio**: sin él el escritorio no arranca, y no viene en el repo.
   ```bash
   cd Escritorio/SistemaAsistencia/SistemaAsistencia
   copy credenciales.env.example credenciales.env
   ```
   Editá `credenciales.env` y completá las dos líneas con tus cadenas reales:
   ```
   MYSQL=Server=<host>;Port=<puerto>;Database=gestion_asistencia_eest;Uid=<user>;Pwd=<password>;
   MONGO=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
   ```
   El formato tiene que ser exacto, sin espacios de más y con `=` como separador.

5. **Compilar y ejecutar (F5).** Si no existen usuarios, se abre `FrmPrimerUsuario` para crear el primer Administrador; después se accede con `FrmLogin`.

> 🔴 `App.config` conserva **solo placeholders** (`PLACEHOLDER_PASSWORD`, `TU_CLUSTER`) como respaldo. Nunca pongas ahí una cadena real: ese archivo sí se versiona.
>
> 🔴 **Build por consola:** usá el MSBuild de Visual Studio 18
> (`C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe`).
> `dotnet msbuild` falla con MSB3822/3823 en este proyecto clásico de .NET Framework.

### 8.2 Base de datos MySQL

El script definitivo reconstruye todo el esquema, **borra los datos anteriores** e incluye catálogo y datos de prueba:

```bash
mysql -u usuario -p < Escritorio/SistemaAsistencia/BD/2026-09-26_reconstruccion_definitiva.sql
```

🟢 No hace falta ningún script de carga de datos aparte: el dataset de prueba ya viene incluido en el script definitivo, y la contraseña inicial de cada usuario es su DNI (ver [§9](#9-uso-del-sistema)).

> ⚠️ Corrélo **una sola vez** y contra la base que quieras dejar como definitiva. Es destructivo.

### 8.3 API (Node)

1. Crear el `.env` y completar los valores:
   ```bash
   cd Api
   copy .env.example .env
   npm install
   ```
   Variables que lee la API:

   | Variable | Para qué |
   |---|---|
   | `DB_HOST` | Host de MySQL. En Railway, el de la **red privada** (`mysql.railway.internal`), no el proxy TCP público |
   | `DB_PORT` | Puerto de MySQL (por defecto `3306`) |
   | `DB_NAME` | Nombre de la base (por defecto `gestion_asistencia_eest`) |
   | `DB_USER` / `DB_PASS` | Credenciales de MySQL |
   | `SESSION_SECRET` | Clave para firmar los tokens |
   | `PORT` | Puerto HTTP. Opcional: si no lo definís, escucha en `3000` |

2. Levantar la API:
   ```bash
   npm start          # o: npm run dev  (con recarga automática)
   ```
   💚 Queda en `http://localhost:3000`. Verificá con `GET /api/health`.

> 🔴 **`SESSION_SECRET` es obligatoria en producción.** Si no la definís, la API genera una clave
> aleatoria en cada arranque y **todos los tokens emitidos quedan inválidos**. En Railway eso
> significa que cada redeploy desloguea a todos los usuarios.
>
> 🔴 El `.env` está en `.gitignore`. Solo editá `.env.example`, que sí se versiona y solo tiene placeholders.

### 8.4 App móvil (Expo)

1. Apuntar la app a la API. Definí `App/.env` (está gitignored) con la URL **incluyendo `https://`**:
   ```bash
   cd App
   # contra la API de Railway:
   echo EXPO_PUBLIC_API_URL=https://sistemaasistencia-production.up.railway.app > .env
   ```
   Para usar la API local en vez de la de Railway, poné la IP de tu PC en la LAN: `http://192.168.x.x:3000`.
   Si no definís la variable, la app la deduce sola con `Constants.expoConfig.hostUri`.

2. Instalar dependencias e iniciar:
   ```bash
   npm install
   npx expo start
   ```
3. 📲 Escanear el QR con **Expo Go** (misma WiFi que la PC).

> 🟡 `App/.env` y cualquier variable `EXPO_PUBLIC_*` viajan **dentro del bundle** de la app. Solo
> poné URLs públicas ahí, nunca un secreto.

### 8.5 API local: base de datos desechable 🧪

Por defecto `Api/.env` apunta a `localhost:3306`, que es una base **distinta** de la de producción.

| | Producción | Local |
|---|---|---|
| **Host** | red privada de Railway | `localhost:3306` |
| **Datos** | 🟢 los reales | 🟡 los del script definitivo |
| **Sirve para** | operar el sistema | 🟢 probar migraciones y restaurar el esquema sin riesgo |

🔴 **La API local no tiene los datos reales.** Si probás algo contra ella y falla, el error puede no ser
el mismo que verás en Railway. Y si funciona en local, tampoco garantiza que funcione en producción.

🟢 **El riesgo real es de datos, no de configuración:** el script definitivo borra todo, así que
probá migraciones contra la base local justamente para no tocar producción.

> 📌 ¿Querés que la API local trabaje contra producción? Cambiá `DB_HOST` y `DB_PORT` en `Api/.env` por los
> del proxy TCP. Tené en cuenta que el bus de eventos SSE es **por proceso**: si el profesor y el
> preceptor apuntan a instancias distintas de la API, no se ven en tiempo real.

## 9. Uso del sistema

**🖥️ Escritorio:**
1. ▶️ Iniciar la app, crear el primer Administrador si es la primera vez.
2. 🔐 Iniciar sesión con usuario y contraseña.
3. 🧭 Desde el menú principal:
   - ⭐ **Administrador:** usuarios, alumnos, profesores, preceptores y materias.
   - 🏛️ **Directivo:** datos institucionales y consultas.
   - 📋 **Profesor / Preceptor:** dictados, inscripciones y datos.
4. 👤 La sesión muestra nombre y rol en `FrmPrincipal`. Los errores de arranque quedan en `bin/**/logs/log_*.txt`.

**🔌📱 API + App:**
1. Levantar MySQL y la API (`npm start`).
2. El profesor abre su clase desde la app (la API genera el token QR).
3. El alumno escanea el QR (o ingresa el código corto) y su asistencia se registra en tiempo real. ⚡

**🧪 Datos de prueba (contraseña = DNI):**

| Rol | Nombre | DNI |
|---|---|---|
| 👨‍🏫 Profesor | Carlos Gutierrez | `30111222` |
| 👩‍🏫 Profesora | María Fernández | `31222333` |
| 📋 Preceptora | Laura Martínez | `34555666` |
| 🎒 Alumno | Juan Pérez | `45222001` |
| 🎒 Alumna | Ana Gómez | `45222002` |
| 🎒 Alumno | Luis Díaz | `45222003` |

## 10. Metas y factores críticos de éxito

**🎯 Metas:**
- ✅ Digitalizar 100% el control de asistencia
- 📉 Reducir el uso de papel
- 📡 Mejorar disponibilidad de la información
- 🗂️ Facilitar administración de alumnos, profesores y cursos
- 🤖 Automatizar reportes de asistencia

**🔑 Factores críticos:**
- 🔐 Autenticación segura y funcional
- 🛡️ Permisos correctos por rol
- 🟢 Disponibilidad permanente de la BD
- ✨ Interfaz simple e intuitiva
- ⚡ Registro rápido de asistencias
- 🧱 Integridad y seguridad de los datos
- 🔌 Código extensible (API + app)

## 11. Cronograma

| Etapa | Período estimado |
|---|---|
| 🔍 Estudio de factibilidad | 29 de abril – primera semana |
| 📝 Análisis de requisitos | Mayo |
| 🎨 Diseño del sistema | Junio – Julio |
| 💻 Desarrollo de la aplicación | Agosto – Octubre |
| 🧪 Implementación y pruebas | Noviembre |
| 🎓 Presentación EACP | Fin del ciclo lectivo |

**⏳ Tiempo total:** ~7 meses.

## 12. Costos

💰 Proyecto académico sin costo de mano de obra.

| Concepto | Costo estimado |
|---|---|
| 💻 Desarrollo de software | Sin costo (proyecto académico) |
| 🐬 MySQL Community Edition | $0 |
| 🧰 Visual Studio Community | $0 |
| 🟢 Node.js / Express / Expo | $0 |
| 🖥️ Equipamiento existente | Sin costo adicional |
| 🧑‍🏫 Capacitación de usuarios | Mínima |
| 🛠️ Mantenimiento anual | Bajo |

El principal costo futuro será el mantenimiento correctivo y evolutivo.

## 13. Roadmap

**✅ Hecho:**
- [x] 🔐 Login y primer usuario admin (escritorio)
- [x] 🗂️ ABM Alumnos, Profesores, Preceptores, Materias, Especialidades, Dictados, Inscripciones, Usuarios
- [x] 🛡️ Permisos por rol
- [x] 🗑️ Baja lógica (`activo`) + script SQL
- [x] 🔒 Credenciales del escritorio movidas a `credenciales.env` (ignorado por git), con `App.config` en placeholders
- [x] 🔑 Rotación de las credenciales de MySQL y MongoDB que estaban versionadas en el historial
- [x] 🔌 API REST: login, dictados, asistencias, clases con QR, health
- [x] 📡 SSE API → app en tiempo real
- [x] 📱 App móvil con 3 roles + QR + código corto
- [x] 🔤 Queries normalizadas a minúscula (crítico: Railway corre Linux)

**🚧 Pendiente:**
- [ ] 🔄 Refresco automático en la app ante cambios del escritorio
- [ ] 🔗 Unificar joins de dictados (INNER vs LEFT) entre escritorio y API
- [ ] 🗑️ Filtrar `activo` en todos los listados de la API
- [ ] 📋 Exponer `id_preceptor` en `GET /api/dictados`
- [ ] ✏️ Endpoints de escritura para dictados (`POST`, `PATCH`)
- [ ] ⭐ Rol administrador en la API / unificar identidad
- [ ] 🔑 Definir `SESSION_SECRET` como variable fija en Railway
- [ ] 👤 Usuario de MySQL con menos privilegios (hoy se usa `root`)
- [ ] 💾 Backup/restauración de MySQL y Mongo
- [ ] 📴 Cola offline en la app para marcar asistencia sin conexión
- [ ] 🚫 Bloqueo por intentos fallidos, auditoría, tests

## 14. Equipo y contexto académico

🎓 Proyecto escolar desarrollado como Evaluación Anual de Capacidades Profesionales (EACP). Migrado desde carpeta compartida de Drive a GitHub para control de versiones y trabajo colaborativo.

| Integrante | Branch de trabajo |
|---|---|
| 👨‍💻 Juan Torres | [`Juan-Torres`](https://github.com/JuanI19T/Sistema_Asistencia/tree/Juan-Torres) |
| 👩‍💻 Isa Vecco | [`Isa-Vecco`](https://github.com/JuanI19T/Sistema_Asistencia/tree/Isa-Vecco) |

## 15. Licencia

📜 Proyecto académico sin licencia definida por el momento.

## 16. Flujo de trabajo Git

```mermaid
graph LR
    JT["🌿 Juan-Torres"] --> PR["🔀 Pull Request"] --> M["⭐ main"]
    IV["🌿 Isa-Vecco"] --> PR
```

**Reglas:**

1. 🌿 Cada uno trabaja **solo en su branch**: `Juan-Torres` e `Isa-Vecco`. Nunca en `main` ni en la del otro.
2. 🔀 Todo cambio llega a `main` **únicamente vía Pull Request**, previa revisión y aprobación del otro. **Nunca** commit/push/merge directo a `main`.
3. 🔄 Para traer lo último de `main` a tu branch: `git fetch origin` + `git merge origin/main` (nunca al revés).
4. 🔒 **No commitear secretos ni generados** (ver `.gitignore`):
   - credenciales: `credenciales.env`, `Api/.env`, `App/.env`
   - claves: `*.pem`, `*.key`
   - generados: `node_modules/`, `.expo/`, `bin/`, `obj/`, `packages/`, `.vs/`, `*.zip`
5. 🔴 **Nunca pongas una credencial real en un archivo versionado.** Si tocás una credencial, rotala en el proveedor (Atlas / Railway), no solo en el código.

> 🛡️ Recomendado: activar branch protection en `main` (requiere PR + prohíbe pushes directos) para que la regla 2 se cumpla sola.

## 17. Documentación adicional

| Documento | Contenido |
|---|---|
| 📘 [`Documentacion/documentacion_munafo/documentacion-tecnica-munafo.md`](Documentacion/documentacion_munafo/documentacion-tecnica-munafo.md) | Documentación técnica y análisis de requerimientos (EACP): problema real, objetivos, marco teórico, alcance, impacto, perfiles, metodología, división de módulos, requerimientos, reglas de negocio, arquitectura, plan de pruebas, diagramas, manual de instalación y conclusiones |
| 📖 [`context.md`](context.md) | Contexto técnico: arquitectura, cómo levantar cada módulo, reglas del proyecto y mapa de archivos |
| 📖 [`AGENTS.md`](AGENTS.md) | Reglas de trabajo del agente: identidad por rama, seguridad con Git, credenciales y estilo |
| 🗺️ `Api/index.js` | Índice vivo de endpoints: `GET /` en la API devuelve la lista completa |

---
<p align="center">Hecho con 💚 para la EEST · EACP 2026</p>
