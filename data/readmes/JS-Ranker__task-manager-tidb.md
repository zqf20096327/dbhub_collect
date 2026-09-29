# 🚀 Sistema de Gestión de Tareas

Aplicación full-stack para gestionar tareas usando **React**, **Node.js**, **Express** y **TiDB Cloud** (MySQL).

![Stack](https://img.shields.io/badge/React-18.3-61dafb?logo=react)
![Stack](https://img.shields.io/badge/Node.js-20+-339933?logo=node.js)
![Stack](https://img.shields.io/badge/Express-5.1-000000?logo=express)
![Stack](https://img.shields.io/badge/TiDB_Cloud-MySQL-FF6B00)

---

## 📋 Características

✅ **CRUD Completo** - Crear, leer, actualizar y eliminar tareas  
✅ **Filtros Inteligentes** - Ver todas, pendientes o completadas  
✅ **Interfaz Moderna** - Diseño oscuro con animaciones suaves  
✅ **Responsive** - Funciona en desktop y móvil  
✅ **TiDB Cloud** - Base de datos MySQL distribuida y escalable  
✅ **API REST** - Backend bien estructurado y documentado

---

## 🗂️ Estructura del Proyecto

```
Test/
├── Back/                      # Backend (Node.js + Express)
│   ├── src/
│   │   ├── config/
│   │   │   └── database.js    # Configuración de TiDB Cloud
│   │   ├── controllers/
│   │   │   └── task.controller.js
│   │   ├── models/
│   │   │   └── task.model.js
│   │   └── routes/
│   │       └── task.routes.js
│   ├── .env.example           # Ejemplo de variables de entorno
│   ├── database.sql           # Script SQL para TiDB Cloud
│   ├── index.js               # Punto de entrada
│   ├── package.json
│   └── README_API.md          # Documentación de la API
│
└── Front/                     # Frontend (React + Vite)
    ├── src/
    │   ├── components/
    │   │   ├── TaskForm.jsx
    │   │   ├── TaskList.jsx
    │   │   └── TaskItem.jsx
    │   ├── services/
    │   │   └── taskService.js
    │   ├── App.jsx
    │   ├── App.css
    │   └── main.jsx
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Node.js** 16+ y **npm**
- Cuenta en [TiDB Cloud](https://tidbcloud.com) (gratis)

### Paso 1: Configurar TiDB Cloud

1. Crea una cuenta en [TiDB Cloud](https://tidbcloud.com)
2. Crea un nuevo cluster (Developer Tier es gratis)
3. Espera a que el cluster esté listo
4. Ve a **SQL Editor** y ejecuta el script `Back/database.sql`
5. Copia las credenciales de conexión (host, puerto, usuario, contraseña)

### Paso 2: Configurar el Backend

```bash
# Navegar a la carpeta del backend
cd Back

# Instalar dependencias
npm install

# Crear archivo .env con tus credenciales
# Copia .env.example y renómbralo a .env
# Luego edita el archivo con tus credenciales de TiDB Cloud
```

**Archivo `.env` (ejemplo):**
```env
PORT=3000
NODE_ENV=development

DB_HOST=gateway01.us-west-2.prod.aws.tidbcloud.com
DB_PORT=4000
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=tasks_db
DB_SSL=true
```

```bash
# Iniciar el servidor backend
npm run dev
```

El servidor estará corriendo en `http://localhost:3000`

### Paso 3: Configurar el Frontend

Abre una **nueva terminal** y ejecuta:

```bash
# Navegar a la carpeta del frontend
cd Front

# Instalar dependencias
npm install

# Iniciar el servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

---

## 🎯 Uso de la Aplicación

### Crear una Tarea
1. Escribe el título (obligatorio)
2. Agrega una descripción (opcional)
3. Haz clic en "✅ Crear Tarea"

### Marcar como Completada
- Haz clic en el checkbox junto a la tarea

### Filtrar Tareas
- **📋 Todas**: Muestra todas las tareas
- **⏳ Pendientes**: Solo tareas sin completar
- **✅ Completadas**: Solo tareas completadas

### Eliminar una Tarea
- Haz clic en el icono 🗑️ y confirma

---

## 📡 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks` | Obtener todas las tareas |
| GET | `/api/tasks?status=completed` | Tareas completadas |
| GET | `/api/tasks?status=pending` | Tareas pendientes |
| GET | `/api/tasks/:id` | Obtener una tarea |
| POST | `/api/tasks` | Crear nueva tarea |
| PUT | `/api/tasks/:id` | Actualizar tarea |
| PATCH | `/api/tasks/:id/toggle` | Cambiar estado |
| DELETE | `/api/tasks/:id` | Eliminar tarea |

Ver documentación completa en `Back/README_API.md`

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Node.js** - Runtime de JavaScript
- **Express** - Framework web
- **mysql2** - Cliente MySQL para Node.js
- **dotenv** - Gestión de variables de entorno
- **cors** - Middleware para CORS
- **nodemon** - Auto-reload en desarrollo

### Frontend
- **React 18** - Librería UI
- **Vite** - Build tool y dev server
- **CSS3** - Estilos personalizados

### Base de Datos
- **TiDB Cloud** - Base de datos MySQL compatible, distribuida y escalable

---

## 🎨 Características del Diseño

- 🌙 **Tema Oscuro Moderno** - Diseño elegante y profesional
- ✨ **Animaciones Suaves** - Transiciones y efectos visuales
- 📱 **Responsive** - Adaptado para móviles y tablets
- 🎯 **UX Intuitiva** - Interfaz fácil de usar
- 🚀 **Performance** - Carga rápida y fluida

---

## 🔧 Scripts Disponibles

### Backend (`Back/`)
```bash
npm start       # Iniciar en producción
npm run dev     # Iniciar con nodemon (desarrollo)
```

### Frontend (`Front/`)
```bash
npm run dev     # Servidor de desarrollo
npm run build   # Build para producción
npm run preview # Preview del build
```

---

## 🐛 Troubleshooting

### Error: "Cannot connect to TiDB Cloud"
- ✅ Verifica las credenciales en `.env`
- ✅ Asegúrate de que el cluster esté activo
- ✅ Verifica que tu IP esté en la whitelist de TiDB Cloud

### Error: "Table 'tasks' doesn't exist"
- ✅ Ejecuta el script `database.sql` en TiDB Cloud

### Error: "Port already in use"
- ✅ Cambia el puerto en `.env` (backend) o `vite.config.js` (frontend)

### Frontend no se conecta al backend
- ✅ Verifica que el backend esté corriendo en `http://localhost:3000`
- ✅ Revisa la consola del navegador para errores CORS

---

## 📚 Próximos Pasos (Mejoras Futuras)

- [ ] Autenticación de usuarios
- [ ] Categorías y etiquetas para tareas
- [ ] Fechas de vencimiento
- [ ] Prioridades (alta, media, baja)
- [ ] Búsqueda de tareas
- [ ] Modo claro/oscuro toggle
- [ ] Exportar tareas a PDF
- [ ] Notificaciones push

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 👨‍💻 Autor

Desarrollado como proyecto de demostración para TiDB Cloud.

---

## 🙏 Agradecimientos

- [TiDB Cloud](https://tidbcloud.com) - Por proporcionar una base de datos MySQL escalable
- [React](https://react.dev) - Por la increíble librería UI
- [Vite](https://vitejs.dev) - Por el rápido build tool
- [Express](https://expressjs.com) - Por el framework web minimalista

---

**¡Disfruta gestionando tus tareas! 🎉**
