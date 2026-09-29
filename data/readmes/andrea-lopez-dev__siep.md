# 🛒 SIEP - Sistema de Información E-commerce para Papelería ISA&CRIS

<p align="center">
  <img src="docs/media/logo_siep.png" alt="Logo SIEP" width="180" style="border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin-bottom: 20px;">
</p>

<p align="center">
  <em>Automatizando la gestión de inventario y ventas para el emprendimiento venezolano.</em>
</p>

<div align="center">

[![SIEP](https://img.shields.io/badge/SIEP-Sistema%20E--commerce-brightgreen)](https://github.com/tu-usuario/siep)
[![PHP](https://img.shields.io/badge/PHP-8.2-777BB4?style=flat-square&logo=php&logoColor=white)](https://www.php.net/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![jQuery](https://img.shields.io/badge/jQuery-3.7-0769AD?style=flat-square&logo=jquery&logoColor=white)](https://jquery.com/)
[![Ajax](https://img.shields.io/badge/Ajax-Async%20Requests-blue?style=flat-square)](https://developer.mozilla.org/es/docs/Web/Guide/AJAX)
[![TCPDF](https://img.shields.io/badge/TCPDF-Reportes%20PDF-red?style=flat-square)](https://tcpdf.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

</div>

<p align="center">
  <img src="docs/media/siep_demo.gif" 
       alt="Demostración del sistema SIEP" 
       width="900" 
       style="border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
</p>

---

## 📑 Índice

- [📖 Descripción General](#-descripción-general)
- [🚀 Stack Tecnológico](#-stack-tecnológico)
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)
- [⚙️ Características Clave](#️-características-clave)
- [📄 Documentos Generados con TCPDF](#-documentos-generados-con-tcpdf)
- [📊 Progreso del Proyecto](#-progreso-del-proyecto)
- [🎯 Impacto del Sistema](#-impacto-del-sistema)
- [📚 Documentación](#-documentación)
- [🛠️ Instalación y Configuración](#️-instalación-y-configuración)
- [📜 Licencia](#-licencia)

---

## 📖 Descripción General

**SIEP** es un sistema de información web diseñado e implementado para modernizar y optimizar los procesos de venta y gestión de inventario de la **Papelería ISA&CRIS**, ubicada en Maracaibo, Estado Zulia, Venezuela. Este sistema surge como respuesta a las limitaciones de la gestión manual y la falta de visibilidad digital, ofreciendo una plataforma centralizada, segura y escalable que automatiza tareas críticas como la gestión de productos, categorías, clientes, proveedores, ventas, compras y la generación de documentos oficiales en PDF y Excel.

---

## 🚀 Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Backend** | PHP 8.2 (Arquitectura MVC nativa) |
| **Frontend** | HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3, jQuery, Ajax |
| **Base de Datos** | MySQL 8.0 (Relacional, Normalizada) |
| **Generación de Reportes** | TCPDF / FPDF (Documentos PDF) y Exportación a Excel/CSV |
| **Arquitectura** | Cliente-Servidor + MVC |
| **Metodología** | Extreme Programming (XP), TDD (Test Driven Development) |
| **Seguridad** | Autenticación por Sesiones, Gestión de Usuarios y Permisos |

---

## 📂 Estructura del Proyecto

```text
/
├── ajax/                         # Peticiones asíncronas (JavaScript/AJAX)
├── Animated Product Card/        # Animaciones y recursos gráficos
├── assets/                       # Recursos estáticos (imágenes, íconos)
├── config/                       # Configuración del sistema (Conexión BD)
├── css/                          # Hojas de estilo personalizadas
├── files/                        # Archivos subidos por el sistema
├── fpdf181/                      # Librería FPDF (Generación de PDF)
├── img/                          # Imágenes generales de la interfaz
├── js/                           # Scripts de JavaScript personalizados
├── modelos/                      # Modelos de datos (MVC)
├── public/                       # Archivos públicos accesibles
├── reportes/                     # Lógica de generación de reportes (TCPDF)
├── vistas/                       # Vistas (HTML, PHP, CSS, JS)
├── index.php                     # Punto de entrada principal
├── login.html                    # Vista de inicio de sesión
├── siep.sql                      # Script de la base de datos MySQL
├── docs/
│   ├── media/
│   │   ├── logo_siep.png         # Logo del proyecto
│   │   └── siep_demo.gif         # GIF de demostración
│   └── manuals/
│       ├── MANUAL_DE_USUARIO_FINAL.pdf
├── .gitignore                    # Archivos ignorados por Git (seguridad y limpieza)
├── LICENSE                       # Licencia MIT del proyecto
└── README.md                     # Documentación del proyecto
```

## ⚙️ Características Clave

## 🔐 Módulos Administrativos (Dashboard)
<table align="center"> <thead> <tr> <th>Módulo</th> <th>Descripción</th> <th>Funcionalidades</th> </tr> </thead> <tbody> <tr> <td><strong>Escritorio</strong></td> <td>Panel de control principal</td> <td>Métricas de compras/ventas, gráficos de los últimos 10 días y 12 meses</td> </tr> <tr> <td><strong>Productos</strong></td> <td>Gestión del catálogo de productos</td> <td>CRUD completo, generador de códigos de barras, control de stock, precios e imágenes</td> </tr> <tr> <td><strong>Categorías</strong></td> <td>Clasificación de productos</td> <td>CRUD, descripción, estado activo/inactivo</td> </tr> <tr> <td><strong>Proveedores</strong></td> <td>Gestión de suministradores</td> <td>CRUD, datos fiscales, contacto, estado activo/inactivo</td> </tr> <tr> <td><strong>Ingresos (Compras)</strong></td> <td>Registro de mercancía comprada</td> <td>CRUD, análisis de costos, <strong>cálculo de IVA</strong>, impuestos, control de documentos fiscales (boleta, factura, ticket)</td> </tr> <tr> <td><strong>Clientes</strong></td> <td>Gestión de compradores</td> <td>CRUD, tipos de documento, dirección, teléfono, email</td> </tr> <tr> <td><strong>Ventas</strong></td> <td>Gestión de transacciones</td> <td>CRUD, análisis de descuentos, <strong>cálculo de IVA</strong>, impuestos, asociación a clientes</td> </tr> <tr> <td><strong>Usuarios</strong></td> <td>Gestión de administradores</td> <td>CRUD, asignación de permisos, control de accesos a módulos</td> </tr> <tr> <td><strong>Permisos</strong></td> <td>Control de roles y accesos</td> <td>CRUD, asignación de permisos específicos a cada usuario (RBAC)</td> </tr> <tr> <td><strong>Consultas de Compras</strong></td> <td>Reportes de compras</td> <td>Filtrado por fechas, exportación a PDF/Excel, reportes de ingresos</td> </tr> <tr> <td><strong>Consultas de Ventas</strong></td> <td>Reportes de ventas</td> <td>Filtrado por fechas y clientes, exportación a PDF/Excel</td> </tr> </tbody> </table>

## 🛍️ Módulo Cliente (E-commerce)

*  **Interfaz Intuitiva:** Catálogo de productos con imágenes, precios en Bolívares (Bs) y disponibilidad.
*  **Menú Categorizado:** Navegación por Lapiceros, Borradores, Sacapuntas, Libretas y Carpetas.
*  **Registro e Inicio de Sesión:** Autenticación de clientes.
*  **Contacto Directo:** Enlace a WhatsApp para consultas y compras.


## 📄 Documentos Generados con TCPDF

El sistema cuenta con un módulo de reportes robusto que utiliza la librería TCPDF para generar documentos oficiales y de gestión:

*   **Reportes PDF:** Reportes de productos, categorías, ventas, compras, clientes y proveedores.
*   **Códigos de Barras:** Generación automática de códigos para etiquetado.
*   **Reportes Excel:** Exportación de datos para análisis externo y contable.
*   **Impresión de Tickets de Compra y Venta:** Opciones de impresión desde el navegador para los reportes generados.

## 📊 Progreso del Proyecto

| Módulo | Estado | Avance |
|--------|--------|--------|
| **Análisis de Requisitos** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Diseño del Sistema (Base de Datos)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Diseño de Interfaz (Wireframes)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Usuarios (CRUD + Permisos)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Categorías (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Productos (CRUD + Códigos de Barras)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Proveedores (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Clientes (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Ventas (CRUD + Análisis de Costos)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Compras / Ingresos (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Generación de Reportes PDF (TCPDF)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Dashboard y Estadísticas (Gráficos)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo Cliente (E-commerce)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Implementación y Despliegue** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Capacitación del Personal** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Mantenimiento y Soporte** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |

## 🎯 Impacto del Sistema
<table align="center"> <thead> <tr> <th>Métrica</th> <th>Antes (Manual)</th> <th>Después (SIEP)</th> <th>Mejora</th> </tr> </thead> <tbody> <tr> <td><strong>Tiempo de registro</strong></td> <td>Horas/Días</td> <td>~2 segundos/consulta</td> <td><strong>-90%</strong></td> </tr> <tr> <td><strong>Errores humanos</strong></td> <td>Alta incidencia</td> <td>Validación automática</td> <td><strong>-85%</strong></td> </tr> <tr> <td><strong>Control de inventario</strong></td> <td>Inexacto</td> <td>Tiempo real</td> <td><strong>Exactitud total</strong></td> </tr> <tr> <td><strong>Generación de reportes</strong></td> <td>Manual (No existía)</td> <td>Automática (PDF/Excel)</td> <td><strong>Optimización total</strong></td> </tr> </tbody> </table>

## 📚 Documentación

Puedes consultar los manuales del sistema en la carpeta **`docs/manuals/`**:

*   📄 [Manual de Usuario](docs/manuals/MANUAL_DE_USUARIO_FINAL.pdf)
  

## 🛠️ Instalación y Configuración

<table align="center"> <thead> <tr> <th>Requisito</th> <th>Versión</th> </tr> </thead> <tbody> <tr> <td><strong>PHP</strong></td> <td>8.2 o superior</td> </tr> <tr> <td><strong>MySQL</strong></td> <td>8.0 o superior</td> </tr> <tr> <td><strong>Servidor Web</strong></td> <td>Apache (XAMPP, WAMP o Laragon recomendados)</td> </tr> </tbody> </table>

## Pasos de Instalación

**1. Clonar el repositorio**

```bash
git clone https://github.com/<tu-usuario>/siep.git
```

```bash
cd siep
```

**2. Configurar el entorno (Base de Datos)**

Edita el archivo **config/Conexion.php (o config/global.php)** con las credenciales de MySQL:

```bash
ini
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=mi_tienda
DB_USERNAME=root
DB_PASSWORD=
```

**3. Importar la base de datos**

Importa el archivo **siep.sql** (ubicado en la raíz del proyecto) usando phpMyAdmin o la línea de comandos:

```bash
mysql -u root -p mi_tienda < "siep.sql"
```

**4. Ejecutar el servidor local**

Coloca la carpeta del proyecto en htdocs **(XAMPP) o www (WAMP)** y accede desde el navegador:

```bash
http://localhost/siep/
```

📄 **Ver archivo [LICENSE](LICENSE) para más detalles.**
