# 🌐 The Good Taste - Web Platform

Plataforma web de comercio electrónico y gestión comercial gastronómica desarrollada en **Laravel** con motor de plantillas **Blade**, empaquetada mediante contenedores **Docker**, con base de datos distribuida en la nube (**TiDB Cloud**) y desplegada en **Render**.

![PHP](https://img.shields.io/badge/PHP-8.4-777BB4?logo=php&logoColor=white)
![Laravel](https://img.shields.io/badge/Laravel-11.x-FF2D20?logo=laravel&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![TiDB](https://img.shields.io/badge/Database-TiDB%20Cloud%20(MySQL)-005571)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7)

---

## 📌 Descripción del Proyecto

**The Good Taste Web** es una solución integral para la digitalización de un negocio gastronómico artesanal. Proporciona a los clientes un catálogo interactivo con carrito de compras, gestión de pedidos y seguimiento de envíos, además de contar con un panel administrativo con control de acceso basado en roles (**RBAC**) para la gestión de productos, stock y métricas comerciales.

---

## ✨ Características Principales

* **Control de Acceso Basado en Roles (RBAC):** Separación de permisos entre Clientes, Administradores y Gerencia.
* **Catálogo Dinámico & Stock:** Visualización de productos categorizados con control de stock mínimo y disponibilidad en tiempo real.
* **Gestión de Pedidos & Checkout:** Carrito de compras reactivo, registro de direcciones de envío, métodos de pago y estados del pedido (pendiente, en preparación, enviado).
* **Canal de Consultas:** Formulario de contacto directo con panel interno de respuestas y seguimiento de mensajes.
* **Seguridad:** Cifrado de contraseñas mediante `bcrypt`, protección contra inyecciones SQL, tokens CSRF nativos de Laravel y conexiones seguras a bases de datos en la nube mediante certificados TLS/SSL (`cacert.pem`).

---

## 🛠️ Stack Tecnológico

* **Backend:** PHP 8.4, Laravel Framework.
* **Frontend:** Blade Templating Engine, Vite, JavaScript, CSS3 / Tailwind CSS.
* **Base de Datos:** TiDB Cloud Serverless (compatible con protocolo MySQL).
* **Contenedores & Despliegue:** Docker (imagen base Alpine con Nginx + PHP-FPM) desplegado en Render.
* **Herramientas de desarrollo:** Composer, NPM, Git.

---

## 🏗️ Arquitectura y Estructura

El sistema implementa el patrón de diseño **MVC (Modelo-Vista-Controlador)**:

```text
The-good-taste/
├── app/
│   ├── Http/Controllers/    # Lógica de controladores de negocio y rutas
│   └── Models/               # Modelos Eloquent ORM (User, Producto, Orden, etc.)
├── database/
│   ├── migrations/           # Esquemas DDL versionados de base de datos
│   └── seeders/              # Datos de prueba controlados
├── resources/
│   └── views/                # Plantillas y componentes modulares en Blade
├── Dockerfile                # Configuración de contenedor PHP 8.4 Alpine + Nginx
├── cacert.pem                # Bundle de certificados de CA para conexión TLS a TiDB
└── routes/                   # Definición de endpoints web y middleware de autenticación
```

👨‍💻 Desarrolladores

Tiziano Perone – Estudiante de Licenciatura en Sistemas de Información (FaCENA - UNNE)

    GitHub: @tiziperone

Obregón Adrián - Estudiante de Licenciatura en Sistemas de Información (FaCENA - UNNE)

    GitHub: @adrianobregon2
