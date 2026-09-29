# Clínica San Luis — Sistema de Citas Médicas

Sistema completo de gestión de citas médicas con agendamiento online, panel administrativo, portal del médico y portal del paciente. Construido con **Next.js 15 + React 19 + TypeScript + MySQL/TiDB**.

## 🚀 Stack

- **Framework**: Next.js 15 (App Router) + React 19 + TypeScript
- **Estilos**: Tailwind CSS 3 + CSS modules propios (`styles/app.css`, `styles/admin.css`)
- **Base de datos**: MySQL / TiDB Serverless (driver `mysql2`)
- **Auth**: NextAuth v5 (Credentials + JWT)
- **Email**: Nodemailer (SMTP)
- **Hosting**: Vercel (optimizado para serverless)

## ✨ Funcionalidades

### Portal público
- Hero, especialidades, médicos, FAQ, pasos
- Wizard de agendamiento en 5 pasos (especialidad → médico → fecha → hora → datos)
- Confirmación con token de cancelación
- Cancelación por token

### Portal del paciente
- Registro y login
- Dashboard con próximas citas, búsqueda, notificaciones
- Historial completo
- Reagendar (médico + fecha + hora)
- Comprobante imprimible
- Perfil + cambio de contraseña
- Cancelar cita

### Portal del médico
- Dashboard con citas del día, KPIs, próxima cita
- Cambiar estado de citas (confirmar / atender / cancelar) con notas
- Toggle de disponibilidad
- Agenda completa agrupada por fecha
- Perfil profesional

### Panel administrativo
- Dashboard con KPIs, gráficos (Chart.js), top especialidades/médicos
- Citas con filtros, paginación, cambio de estado AJAX, reasignar médico, exportar CSV
- Especialidades: CRUD (crear auto-genera médico por defecto con horarios)
- Médicos: CRUD, toggle disponibilidad
- Usuarios: CRUD, desbloquear cuentas
- Horarios: bloques semanales por médico, bloqueos por fecha
- Feriados: CRUD, activar/desactivar
- Notificaciones en tiempo real (polling 30s)
- Auditoría con filtros y paginación
- Reportes con estadísticas y gráficos de barras

## 🛠️ Instalación local

```bash
cd web
npm install
cp .env.example .env.local
# Configurar las variables de entorno (ver más abajo)
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000).

## 🔐 Configuración de la base de datos

### Opción A — TiDB Serverless (recomendado para producción)

1. Crear cluster gratuito en [tidbcloud.com](https://tidbcloud.com)
2. Obtener el connection string (formato: `mysql://user:pass@host:4000/dbname?ssl-mode=REQUIRED`)
3. Setear en `.env.local`:
   ```
   DATABASE_URL="mysql://USER:PASS@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/clinica_san_luis?ssl-mode=REQUIRED"
   ```

### Opción B — MySQL local o PlanetScale

Setear las variables individuales `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME`.

### Esquema

Importar `database/schema.tidb.sql` en la base de datos. Contiene todas las tablas, índices, claves foráneas, datos seed y un usuario admin:

- **Email**: `admin@clinicasanluis.com`
- **Contraseña**: hash bcrypt pre-generado (ver archivo SQL)

## 🌐 Deploy en Vercel

1. **Crear repositorio en GitHub** y subir todo el proyecto.
2. **Importar en Vercel** desde el repo.
3. En la configuración del proyecto en Vercel, **setear "Root Directory" = `web`** (porque el código Next.js está dentro de esa carpeta, mientras que el PHP legacy está en la raíz).
4. Configurar las variables de entorno en Vercel (Settings → Environment Variables):
   - `DATABASE_URL` (o `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME`)
   - `AUTH_SECRET` (generar con `openssl rand -base64 32`)
   - `AUTH_TRUST_HOST=true`
   - `APP_URL` (URL de producción, ej: `https://tu-clinica.vercel.app`)
   - `MAIL_*` (opcional, para confirmaciones)
5. Deploy.

> 💡 Alternativa: si querés deployar directamente sin tocar el Root Directory, mové todo el contenido de `web/` a la raíz del repo y agregá el contenido de `web/public/` a `public/`. Pero mantener la estructura es más limpio.

## 📁 Estructura

```
clinica-san-luis/
├── web/                       # App Next.js (deployable)
│   ├── app/
│   │   ├── (public)/          # Portal público + paciente (URLs: /, /agendar, /paciente/...)
│   │   ├── admin/             # Panel admin (protegido)
│   │   ├── medico/            # Portal médico (protegido)
│   │   ├── api/               # API routes
│   │   └── globals.css
│   ├── components/            # Componentes compartidos (cliente)
│   ├── lib/                   # Capa de datos, auth, helpers
│   │   ├── auth.ts            # NextAuth config
│   │   ├── db.ts              # Pool MySQL
│   │   ├── env.ts             # Variables de entorno
│   │   ├── audit.ts           # Logs de auditoría
│   │   ├── notifications.ts   # Notificaciones in-app
│   │   ├── time.ts            # Helpers de zona horaria
│   │   ├── email.ts           # Nodemailer
│   │   ├── email-confirmacion.ts
│   │   └── repos/             # Repositorios (citas, medicos, especialidades, etc.)
│   ├── public/                # Assets estáticos
│   ├── styles/                # CSS global (app + admin)
│   ├── types/                 # TypeScript types
│   ├── middleware.ts          # Auth guard global
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── vercel.json
│   └── package.json
│
├── database/
│   └── schema.tidb.sql        # Esquema completo + datos seed
│
├── controllers/               # PHP legacy (ignorado, referencia)
├── models/                    # PHP legacy
├── views/                     # PHP legacy
├── config/
├── helpers/
├── middleware/                # PHP legacy
├── public/                    # PHP legacy assets
├── routes/
├── scripts/
├── traits/
└── backups/
```

## 🔑 Credenciales iniciales (después de importar el SQL)

- **Admin**: `admin@clinicasanluis.com` / ver hash en `database/schema.tidb.sql`
- **Recepción**: `recepcion@gmail.com` / (ver schema)
- **Paciente seed**: `prueba@gmail.com` / (ver schema)

## 🛡️ Roles y permisos

| Rol | Acceso |
|-----|--------|
| `admin` / `administrador` | Panel completo |
| `recepcion` / `recepcionista` | Citas, dashboard |
| `medico` | Sus propias citas, perfil, disponibilidad |
| `paciente` | Sus propias citas, reagendar, cancelar, perfil |

## 🧪 Scripts

```bash
cd web
npm run dev         # Dev server
npm run build       # Build producción
npm run start       # Servidor producción
npm run typecheck   # TypeScript check
npm run lint        # ESLint
```

## 📝 Notas

- El proyecto mantiene **el mismo diseño visual** que la versión PHP original (mismos colores, tipografías, layouts, animaciones, iconos FontAwesome).
- Toda la lógica de negocio del PHP fue migrada a repositorios TypeScript en `lib/repos/`.
- La zona horaria es configurable vía `TIMEZONE` (default `America/Asuncion`).
- El sistema de auditoría registra automáticamente las acciones administrativas (crear, editar, eliminar, login, etc.) con IP y user-agent.
- Compatible con MySQL 8 y TiDB Serverless.
- La versión PHP original queda intacta en la raíz para referencia histórica.

## 📄 Licencia

Privado.
