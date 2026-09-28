# ETC Vallenas

![Laravel](https://img.shields.io/badge/Laravel-10-FF2D20?style=for-the-badge&logo=laravel&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-8.1+-777BB4?style=for-the-badge&logo=php&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-38B2AC?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-yellow?style=for-the-badge)

Sistema integral de gestión para **ETC Vallenas**, empresa líder en alquiler de maquinaria pesada con más de 8 años de experiencia en Cusco, Perú. La plataforma está construida con Laravel 10, componentes de UI con Blade Templates y Alpine.js, Tailwind CSS y persistencia mediante MySQL.

La aplicación prioriza la seguridad, el rendimiento, una experiencia de usuario responsive y una arquitectura mantenible para gestionar de forma escalable el catálogo de equipos, proyectos de construcción, base de clientes y el panel administrativo.

---

## Tabla de contenidos

1. [Características clave](#características-clave)
2. [Arquitectura y stack](#arquitectura-y-stack)
3. [Comenzar](#comenzar)
4. [Variables de entorno](#variables-de-entorno)
5. [Scripts disponibles](#scripts-disponibles)
6. [Estructura del proyecto](#estructura-del-proyecto)
7. [Base de datos y roles](#base-de-datos-y-roles)
8. [Calidad y buenas prácticas](#calidad-y-buenas-prácticas)
9. [Despliegue](#despliegue)
10. [Roadmap](#roadmap)
11. [Licencia y contacto](#licencia-y-contacto)

---

## Características clave

- **Gestión integral de maquinaria**: Catálogo completo de más de 85 equipos, control de estados (disponible, en uso, mantenimiento), historial técnico y galería de imágenes.
- **Proyectos y servicios**: Planificación de obras, asignación de recursos, control de presupuestos y gestión de alquileres y transportes.
- **Sistema de cotizaciones inteligente**: Formularios interactivos con cálculo automático de precios, envío por correo, seguimiento de estados y panel de historial.
- **Panel administrativo centralizado**: Dashboard de estadísticas con Chart.js, gestión de usuarios, auditoría de actividad y generación de reportes exportables.
- **Identidad corporativa e interfaz UI**: Diseño basado en los tokens de marca (`#1565C0`, `#FFC107`), mobile-first, accesible (WCAG 2.1) y preparado para PWA.
- **Estrategia SEO & Rendimiento**: Implementación de meta tags avanzados, Open Graph, Sitemap XML, robots.txt, lazy loading y caché de assets optimizada.

## Arquitectura y stack

| Capa | Tecnologías | Descripción |
| --- | --- | --- |
| Framework | Laravel 10, PHP 8.1+ | Ruteo web/API, controladores, Eloquent ORM, middleware y migraciones. |
| UI & Interacción | Blade, Alpine.js | Renderizado SSR eficiente e interacciones declarativas en el frontend. |
| Estilos | Tailwind CSS 3, Bootstrap 5 | Sistema visual utilitario híbrido enfocado en desarrollo rápido y diseño responsive. |
| Autenticación | Sanctum, Sesiones | Manejo de sesión por cookies para web y tokens API para integraciones móviles. |
| Datos | MySQL 8.0+ | Esquema relacional estructurado, integridad referencial y alto rendimiento. |
| Build Tools | Vite 5, PostCSS | HMR (Hot Module Replacement) ultrarrápido y bundling optimizado. |
| Testing | PHPUnit | Cobertura de pruebas unitarias, de integración y evaluación de endpoints RESTful. |

## Comenzar

### Requisitos previos

- PHP 8.1 LTS o superior.
- Composer 2.x.
- Node.js 18 LTS o superior.
- MySQL 8.0+.
- npm o Yarn.

### Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/EzerZuniga/vallenas-rental-system.git
cd vallenas-rental-system

# 2. Instala dependencias del backend
composer install

# 3. Instala dependencias del frontend
npm install

# 4. Configura variables de entorno y clave de app
cp .env.example .env
php artisan key:generate

# 5. Levanta la base de datos (Ejecuta migraciones y seeders)
php artisan migrate --seed

# 6. Levanta los servidores de desarrollo
npm run dev
php artisan serve
```

La aplicación queda disponible por defecto en `http://localhost:8000`.

## Variables de entorno

El archivo `.env` documenta las variables de entorno principales. Algunas de las más críticas son:

| Variable | Uso |
| --- | --- |
| `APP_URL` | URL pública usada para generación de enlaces y rutas estáticas. |
| `DB_CONNECTION` | Driver relacional de base de datos (ej. `mysql`). |
| `DB_HOST`, `DB_PORT` | Credenciales de conexión de la BD local o productiva. |
| `DB_DATABASE` | Nombre de la base de datos (ej. `etc_vallenas`). |
| `MAIL_MAILER` | Configuración SMTP para notificaciones por correo electrónico de cotizaciones. |

Nunca subas valores reales de secretos o credenciales de base de datos productivas al repositorio.

## Scripts disponibles

| Comando / Script | Descripción |
| --- | --- |
| `npm run dev` | Inicia el servidor de Vite con HMR para desarrollo en el frontend. |
| `npm run build` | Genera la build optimizada de assets (CSS/JS) en `public/build/`. |
| `php artisan serve` | Inicia el servidor de desarrollo nativo de PHP para probar la aplicación. |
| `php artisan test` | Ejecuta la suite de pruebas automatizadas (unitarias y de características). |
| `npm run format` | Estandariza el formato del código fuente usando Prettier. |

## Estructura del proyecto

```text
vallenas-rental-system/
├── app/
│   ├── Http/                  # Controladores, Middleware y Requests (Lógica de entrada)
│   └── Models/                # Modelos Eloquent de la lógica de negocio y persistencia
├── config/                    # Configuración centralizada de la plataforma
├── database/
│   ├── migrations/            # Versionado y control del esquema relacional de BD
│   └── seeders/               # Población inicial de catálogos y cuentas de usuarios
├── public/
│   ├── build/                 # Assets procesados y minificados por Vite (No versionados)
│   └── assets/                # Imágenes corporativas, vectores, fuentes e iconos
├── resources/
│   ├── css/app.css            # Archivo raíz de hojas de estilo y directivas Tailwind
│   └── views/                 # Interfaces Blade estructuradas (auth, admin, catálogo)
├── routes/
│   ├── web.php                # Rutas públicas y protegidas de la aplicación web
│   └── api.php                # Endpoints RESTful para consumo e integraciones externas
├── tests/                     # Suite de pruebas automatizadas (Feature & Unit)
├── tailwind.config.js         # Configuración de variables visuales y tokens de diseño
└── vite.config.js             # Parámetros de compilación y empaquetado de assets
```

## Base de datos y roles

El sistema cuenta con un esquema de base de datos relacional altamente estructurado, administrado a través de políticas de acceso y roles granulares:

| Rol | Permisos y alcance operativo |
| --- | --- |
| **Super Admin** | Acceso total al sistema, configuración global, gestión de permisos y auditoría. |
| **Admin** | Administración operativa general: catálogo, altas de proyectos y validación de cotizaciones. |
| **Operador** | Gestión de campo técnica: reportes de mantenimiento, horas de trabajo y operatividad. |
| **Cliente** | Cuenta de uso estándar: visualización de cotizaciones propias y tracking de proyectos contratados. |

Comandos de mantenimiento de la estructura de datos:
```bash
# Limpiar y regenerar la base de datos con información de catálogos base para pruebas
php artisan migrate:fresh --seed
```

## Calidad y buenas prácticas

Antes de abrir pull requests o realizar un despliegue, verifica la integridad estructural del sistema con las siguientes herramientas de validación:

```bash
php artisan test --coverage
npm run format
npm run build
```

**Estándares de seguridad rigurosamente implementados:**
- Autenticación de múltiples factores (2FA) en panel administrativo.
- Prevención activa contra inyecciones SQL y vulnerabilidades Cross-Site Scripting (XSS).
- Protección de estado de sesión a través de tokens CSRF en todos los formularios de la plataforma.
- Estrategias de Rate Limiting en endpoints API críticos para mitigar vectores de ataques DDoS.
- Políticas programadas para copias de seguridad de la base de datos (Backups automáticos).

## Despliegue

La solución está completamente arquitectada para operar en infraestructuras VPS tradicionales, plataformas en la nube o soluciones gestionadas como Laravel Forge/Vapor.

Pasos estandarizados para un despliegue fiable en producción:

1. **Resolver dependencias base**: `composer install --optimize-autoloader --no-dev`
2. **Generar el caché de configuración**: `php artisan config:cache`
3. **Optimizar el mapeo de rutas**: `php artisan route:cache`
4. **Pre-compilar el caché de vistas**: `php artisan view:cache`
5. **Generar assets empaquetados finales**: `npm run build`
6. **Asegurar los privilegios de entorno**: `chmod -R 775 storage bootstrap/cache`

## Roadmap

### Versión 1.0 (Actual)
- Base sólida de roles y autenticación multicapa.
- Catálogo digital interactivo e inventario de maquinaria.
- Motor de cálculos y aprobaciones de cotizaciones corporativas.
- Panel de control y reportería operativa.

### Versión 1.1 (Próximamente)
- Aplicación móvil nativa en React Native para acceso ubicuo.
- Módulos integrados con pasarela de transacciones digitales (pagos online).
- Suscripción y firma digital certificada de contratos de alquiler.
- Integración en tiempo real con dispositivos telemétricos GPS para tracking de flotilla.

### Versión 2.0 (Futuro)
- Sensores IoT de amplio espectro para biometría y telemetría avanzada de maquinarias.
- Modelos predictivos basados en Machine Learning enfocados a mantenimientos técnicos.
- Garantía de trazabilidad inmutable de operaciones logísticas apalancado en Blockchain.

## Licencia y contacto

**Propiedad, Uso y Licencia**
Este software es propiedad intelectual de carácter privado y exclusivo de la entidad corporativa **E.T.C Vallenas**. Queda estrictamente restringido su uso, distribución y copia, amparado por normativas de protección de derechos de autor.
Copyright © 2025 - "Fernando Alonso Vallenas Saraya". Todos los derechos reservados.

---

**Desarrollado y mantenido por:**
[**Ezer B. Zuñiga Chura**](https://www.instagram.com/ezerzuniga.oficial16/) | ezerzuniga@gmail.com

**Contacto Corporativo ETC Vallenas:**
- **Web:** [etcvallenas.com](https://www.etcvallenas.com)
- **Email:** vallenasfernando43@gmail.com
- **Teléfono:** +51 984 123 456
- **Dirección:** Av. La cultura control, Cusco, Perú (Horario: Lun-Sab 8:00-18:00)

**ETC Vallenas - Construyendo el futuro del Perú 🚜🇵🇪**
