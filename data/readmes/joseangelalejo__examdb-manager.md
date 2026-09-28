# 📝 ExamDB Manager — Generador Automático de Entornos de Examen

Plataforma full-stack para que profesores generen automáticamente entornos de examen personalizados. Crea bases de datos, usuarios y credenciales en minutos. Incluye autenticación JWT, validación de conexiones y exportación de resultados.

🌐 **[examdb-manager.joseangelinfra.dev](https://examdb-manager.joseangelinfra.dev)**

<div align="center">

![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=for-the-badge&logo=next.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![TiDB Cloud](https://img.shields.io/badge/TiDB-Cloud-00D988?style=for-the-badge&logo=tidb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-E2A107?style=for-the-badge&logo=playwright&logoColor=white)

</div>

## ✨ Características principales

✅ **Generación automática** — Crea entornos de examen masivamente  
✅ **CSV de alumnos** — Importa lista de estudiantes y genera BD por cada uno  
✅ **Usuarios únicos** — Password seguro generado para cada estudiante  
✅ **Scripts DDL/DML** — Personaliza schema y datos del examen  
✅ **Validación BD** — Verifica conexión antes de ejecutar scripts  
✅ **Exportación** — Descarga credenciales en CSV  
✅ **JWT Auth** — Autenticación segura para profesores  

## 🛠️ Stack técnico

| Capa         | Tecnología                                    |
|--------------|-----------------------------------------------|
| **Frontend** | Next.js 15 + React 19 + TypeScript + Tailwind |
| **Backend**  | Next.js App Router API Routes                 |
| **BD**       | TiDB Cloud (MySQL compatible)                 |
| **Auth**     | JWT (jsonwebtoken) + bcrypt                   |
| **Deploy**   | Vercel + Docker                               |
| **Testing**  | Playwright E2E                                |
| **CI/CD**    | GitHub Actions                                |

## 🚀 Quick Start

```bash
# Clonar repositorio
git clone https://github.com/joseangelalejo/examdb-manager.git
cd examdb-manager

# Instalar dependencias
npm install

# Configurar variables
cp .env.example .env.local
# Edita con credenciales TiDB, JWT_SECRET, TEACHERS_JSON

# Desarrollo
npm run dev

# Build
npm run build
npm start
```

## 🐳 Docker

```bash
# Build
docker build -t examdb-manager .

# Run
docker-compose up -d
```

## 📋 Flujo de uso

1. **Login** — Profesor ingresa con JWT
2. **Subir CSV** — Lista de alumnos (nombre, email, DNI)
3. **Configurar BD** — Nombre de BD, usuario, contraseña base
4. **Script SQL** — DDL personalizado (CREATE TABLE, etc.)
5. **Generar** — Sistema crea BD para cada alumno
6. **Exportar** — Descarga CSV con credenciales

## 📚 Documentación

→ **[joseangelalejo.github.io/examdb-manager](https://joseangelalejo.github.io/examdb-manager/)**

## 🔗 Enlaces

- 🌐 [Sitio en vivo](https://examdbmanager.vercel.app)
- 📖 [Documentación](https://joseangelalejo.github.io/examdb-manager/)
- ♻️ [GitHub Repo](https://github.com/joseangelalejo/examdb-manager)
- 🐛 [Reportar bugs](https://github.com/joseangelalejo/examdb-manager/issues)

```text
examdb-manager/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth/login/route.ts        ← POST /api/auth/login
│   │   │   ├── db/test-connection/route.ts ← POST /api/db/test-connection
│   │   │   ├── exam/generate/route.ts      ← POST /api/exam/generate ★
│   │   │   ├── exam/cleanup/route.ts       ← POST /api/exam/cleanup
│   │   │   └── health/route.ts             ← GET  /api/health
│   │   ├── layout.tsx
│   │   ├── page.tsx                        ← Wizard de 4 pasos
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/
│   │   │   ├── StepIndicator.tsx
│   │   │   └── SqlEditor.tsx
│   │   └── exam/
│   │       └── ResultsTable.tsx
│   ├── lib/
│   │   ├── db.ts                           ← Conexión MySQL/TiDB
│   │   ├── auth.ts                         ← JWT helpers
│   │   └── userGenerator.ts               ← Genera usuarios/BD/passwords
│   └── types/
│       └── index.ts                        ← Tipos TypeScript centralizados
├── tests/e2e/                              ← Tests Playwright
├── .github/workflows/
│   ├── ci.yml                              ← Lint + Build + Test + Docker
│   └── deploy.yml                          ← Deploy automático a Vercel
├── Dockerfile                              ← Multistage build
├── docker-compose.yml                      ← App + Nginx
├── nginx.conf
└── vercel.json
```

---

## Instalación Local

```bash
# 1. Clonar
git clone https://github.com/joseangelalejo/examdb-manager.git
cd examdb-manager

# 2. Instalar dependencias
npm install

# 3. Configurar entorno
cp .env.example .env.local

# 4. Generar hash de contraseña de profesor
npm run hash-password tu_contraseña
# → Copia el hash en TEACHERS_JSON dentro de .env.local

# 5. Arrancar en desarrollo
npm run dev
# → http://localhost:3000
```

**Credenciales de desarrollo** (sin configurar nada):

- Usuario: `profesor`
- Contraseña: `password123`

---

## Docker

```bash
# Desarrollo rápido
cp .env.example .env
# Editar .env con JWT_SECRET y TEACHERS_JSON
docker compose up --build

# → Disponible en http://localhost (nginx en puerto 80)
```

```bash
# Solo la app (sin nginx)
docker build -t examdb-manager .
docker run -p 3000:3000 \
  -e JWT_SECRET=tu_clave_secreta \
  -e TEACHERS_JSON='[{"username":"prof","passwordHash":"$2a$10$..."}]' \
  examdb-manager
```

---

## Deploy en Vercel

### Opción A: Deploy manual (primera vez)

```bash
npm install -g vercel
vercel login
vercel                   # Modo interactivo, configura el proyecto
vercel --prod            # Deploy a producción
```

### Opción B: Deploy automático via GitHub Actions

1. Conecta el repo a Vercel en el Dashboard
2. Añade estos **GitHub Secrets** en `Settings → Secrets → Actions`:

   | Secret              | Valor                                        |
   |---------------------|----------------------------------------------|
   | `VERCEL_TOKEN`      | Token en vercel.com/account/tokens           |
   | `VERCEL_ORG_ID`     | En `.vercel/project.json` tras `vercel link` |
   | `VERCEL_PROJECT_ID` | En `.vercel/project.json`                    |
   | `JWT_SECRET`        | Tu clave secreta (64+ chars)                 |

3. Cada push a `main` → deploy automático

### Variables de entorno en Vercel

Ve a **Project → Settings → Environment Variables** y añade:

| Variable        | Descripción                         |
|-----------------|-------------------------------------|
| `JWT_SECRET`    | Clave JWT larga y aleatoria         |
| `TEACHERS_JSON` | Array JSON con hashes de profesores |

---

## Flujo de la Aplicación

```text
PASO 1 — Login
  → Profesor introduce usuario + contraseña
  → Se emite JWT (8h de validez)

PASO 2 — Conexión al Servidor
  → Profesor introduce host/puerto/usuario/contraseña del admin TiDB
  → Se verifica la conexión en tiempo real

PASO 3 — Panel de Examen
  ┌─────────────────────────────────────┐
  │ ① Script CREATE TABLE              │
  │ ② Script INSERT INTO               │
  │ ③ Enunciado del examen             │
  │ ④ Lista de alumnos (CSV)           │
  └─────────────────────────────────────┘
  → Botón "GENERAR ENTORNO DE EXAMEN"

PASO 4 — Resultados
  → Tabla con: alumno | usuario | contraseña | base de datos
  → Descarga CSV / Copia al portapapeles
```

---

## Formato CSV de Alumnos

```csv
nombre,apellido1,apellido2,ciclo
Juan,Perez,Lopez,DAW
Marta,Garcia,Ruiz,DAM
```

**Usuarios generados:**

```text
Juan Pérez López  (DAW) → usuario: juanperezlopez_daw   | BD: exam_daw_juanperezlopez
Marta García Ruiz (DAM) → usuario: martagarciaruiz_dam  | BD: exam_dam_martagarciaruiz
```

---

## Seguridad

- Cada alumno tiene su propio usuario MySQL y SOLO puede acceder a su base de datos
- Las BDs usan `utf8mb4_unicode_ci` → case insensitive
- Contraseñas de alumnos generadas aleatoriamente (12 chars, mayúsculas + dígitos + símbolos)
- Contraseñas de profesores hasheadas con bcrypt (10 rounds)
- JWT con expiración de 8 horas
- Las credenciales de BD admin nunca se almacenan en servidor; viajan en el body cifrado por HTTPS

---

## Tests

```bash
# E2E con Playwright
npm run test:e2e

# Con UI interactiva
npm run test:e2e:ui

# Solo type check
npm run type-check

# Lint
npm run lint
```

---

## Licencia

Uso educativo. Consulta el archivo `LICENSE.md` para más detalles.
