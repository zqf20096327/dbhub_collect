# 🎓 SIGENOR - Sistema de Información de Gestión Académica (SGA)

<p align="center">
  <img src="docs/media/logo_sistem.png" alt="Logo SIGENOR" width="180" style="border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin-bottom: 20px;">
</p>

<p align="center">
  <em>Transformando la gestión educativa nocturna a través de la tecnología.</em>
</p>

<div align="center">

[![SIGENOR](https://img.shields.io/badge/SIGENOR-Sistema%20de%20Gesti%C3%B3n%20Acad%C3%A9mica-brightgreen)](https://github.com/tu-usuario/sigenor)
[![PHP](https://img.shields.io/badge/PHP-8.2-777BB4?style=flat-square&logo=php&logoColor=white)](https://www.php.net/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![TCPDF](https://img.shields.io/badge/TCPDF-Reportes%20PDF-red?style=flat-square)](https://tcpdf.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

</div>

<p align="center">
  <img src="docs/media/sigenor_demo.gif" 
       alt="Demostración del sistema SIGENOR" 
       width="900" 
       style="border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
</p>


## 📑 Índice

- [📖 Descripción General](#-descripción-general)
- [🚀 Stack Tecnológico](#-stack-tecnológico)
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)
- [⚙️ Características Clave](#️-características-clave)
- [📊 Progreso del Proyecto](#-progreso-del-proyecto)
- [📚 Documentación](#-documentación-y-manuales)
- [🛠️ Instalación y Configuración](#️-instalación-y-configuración)
- [🧪 Pruebas](#-pruebas)
- [🎯 Impacto Social](#-impacto-social)
- [📜 Licencia](#-licencia)


## 📖 Descripción General

**SIGENOR** es un sistema de información web diseñado e implementado para modernizar y optimizar los procesos académicos y administrativos de la **Unidad Educativa Nocturna "Br. Rafael Rangel"**. Este sistema surge como respuesta a las limitaciones de la gestión manual basada en hojas de cálculo (Excel), ofreciendo una plataforma centralizada, segura y escalable que automatiza tareas críticas como la gestión de estudiantes, docentes, asignaturas, calificaciones, asistencias y la generación de documentos oficiales.


## 🚀 Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Backend** | PHP 8.2 (Arquitectura MVC Clásica) |
| **Frontend** | HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3, jQuery |
| **Base de Datos** | MySQL 8.0 (Relacional, Normalizada) |
| **Generación de Reportes** | TCPDF (Documentos PDF institucionales) |
| **Arquitectura** | Cliente-Servidor + MVC |
| **Metodología** | Waterfall (Modelo en Cascada) |
| **Seguridad** | Autenticación por Sesiones y Control de Roles |


## 📂 Estructura del Proyecto

```text
/
├── Assets/
│   ├── css/                     # Hojas de estilo personalizadas
│   ├── js/                      # Scripts de JavaScript personalizados
│   └── images/                  # Imágenes y logotipos institucionales
├── backup/                      # Archivos de respaldo de la base de datos
├── Config/                      # Configuración del sistema
├── logs/                        # Registros de actividad y errores
├── php/                         # Lógica de negocio en PHP
│   ├── Models/                  # Modelos de datos
│   ├── Controllers/             # Controladores (MVC)
│   └── Views/                   # Vistas (HTML, CSS, JS)
├── Views/                       # Vistas principales del sistema
├── .htaccess                    # Configuración del servidor Apache
├── composer.json                # Dependencias de PHP
├── composer.lock                # Bloqueo de versiones
├── index.php                    # Punto de entrada principal
├── sigenor.sql                  # Script de la base de datos MySQL
├── docs/
│   ├── media/
│   │   ├── logo_sistem.png     # Logo del proyecto
│   │   └── sigenor_demo.gif     # GIF de demostración
│   └── manuals/
│       ├── MANUAL_SIGENOR.pdf
│       └── TRIPTICOS_SIGENOR.pdf
├── LICENSE                      # Licencia MIT del proyecto
└── README.md                    # Documentación del proyecto
```


## ⚙️ Características Clave

### 🔐 Módulos Implementados

<table align="center">
  <thead>
    <tr>
      <th>Módulo</th>
      <th>Descripción</th>
      <th>Funcionalidades</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Usuarios</strong></td>
      <td>Gestión de accesos al sistema</td>
      <td>CRUD completo, control de permisos, autenticación segura</td>
    </tr>
    <tr>
      <td><strong>Estudiantes</strong></td>
      <td>Registro y gestión de alumnos</td>
      <td>CRUD, filtros por cédula/sección/sexo, historial de planteles</td>
    </tr>
    <tr>
      <td><strong>Profesores</strong></td>
      <td>Gestión de docentes</td>
      <td>CRUD, asignación de asignaturas, datos de contacto</td>
    </tr>
    <tr>
      <td><strong>Planteles</strong></td>
      <td>Instituciones educativas asociadas</td>
      <td>CRUD, información de directores y zonas educativas</td>
    </tr>
    <tr>
      <td><strong>Periodos</strong></td>
      <td>Ciclos académicos</td>
      <td>CRUD, control de fechas de inicio/fin</td>
    </tr>
    <tr>
      <td><strong>Secciones</strong></td>
      <td>Grupos escolares</td>
      <td>CRUD, asignación a periodos, control de capacidad</td>
    </tr>
    <tr>
      <td><strong>Asignaturas</strong></td>
      <td>Materias del plan de estudio</td>
      <td>CRUD, asignación a profesores</td>
    </tr>
    <tr>
      <td><strong>Asistencias</strong></td>
      <td>Registro de presencia</td>
      <td>CRUD, control de inasistencias, vinculación a estudiantes</td>
    </tr>
    <tr>
      <td><strong>Calificaciones</strong></td>
      <td>Notas académicas</td>
      <td>CRUD, conversión automática escala 1-20 a 1-5</td>
    </tr>
    <tr>
      <td><strong>Plan Administrativo</strong></td>
      <td>Configuración institucional</td>
      <td>CRUD, tipos de evaluación, estrategias de estudio</td>
    </tr>
    <tr>
      <td><strong>Dashboard</strong></td>
      <td>Panel de control</td>
      <td>Estadísticas, gráficos, indicadores en tiempo real</td>
    </tr>
    <tr>
      <td><strong>Reportes PDF</strong></td>
      <td>Documentos oficiales</td>
      <td>Boletines, certificados, resúmenes curriculares</td>
    </tr>
  </tbody>
</table>


### 📄 Documentos Generados con TCPDF

*   **Boletín de Calificaciones** (Formato EMGMJAA)
*   **Certificado de Calificaciones** (Formato EMGMJAA)
*   **Resumen Curricular** por estudiante
*   **Listado de Estudiantes** por sección/periodo
*   **Reporte de Asistencias e Inasistencias**
*   **Reporte de Profesores** y asignaturas asignadas
*   **Reporte de Asignaturas** del plan de estudio


### 🔒 Validaciones y Seguridad Implementadas

*   **Validación de unicidad de cédula:** Verificación automática en el registro de estudiantes mediante consultas SQL.
*   **Cálculo automático de estados académicos:** Conteo de aprobados, reprobados, inasistentes y no evaluados.
*   **Filtros de búsqueda avanzados:** Búsqueda por cédula, nombres, apellidos, plantel, sección y sexo en tiempo real.
*   **Historial académico enlazado:** Vinculación automática de calificaciones, fechas, periodos y asignaturas al perfil del estudiante.
*   **Control de sesiones:** Autenticación y acceso restringido por roles.


## 📊 Progreso del Proyecto

| Módulo | Estado | Avance |
|--------|--------|--------|
| **Análisis de Requisitos** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Diseño del Sistema (Base de Datos)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Diseño de Interfaz (Wireframes)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Usuarios (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Estudiantes (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Profesores (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Planteles (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Periodos (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Secciones (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Asignaturas (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Asistencias (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Módulo de Calificaciones (CRUD)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Generación de Reportes PDF (TCPDF)** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Dashboard y Estadísticas** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Implementación y Despliegue** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Capacitación del Personal** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
| **Mantenimiento y Soporte** | ✅ Completado | ![100%](https://img.shields.io/badge/-100%25-brightgreen) |
---

## 📚 Documentación y Manuales

Puedes consultar los manuales del sistema en la carpeta `docs/manuals/`:

*   📄 [Manual de Usuario](docs/manuals/MANUAL_SIGENOR.pdf)
*   📄 [Tríptico Informativo](docs/manuals/TRIPTICOS_SIGENOR.pdf)


## 🛠️ Instalación y Configuración

### Requisitos Previos

<table align="center">
  <thead>
    <tr>
      <th>Requisito</th>
      <th>Versión</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>PHP</strong></td>
      <td>8.2 o superior</td>
    </tr>
    <tr>
      <td><strong>Composer</strong></td>
      <td>2.x</td>
    </tr>
    <tr>
      <td><strong>MySQL</strong></td>
      <td>8.0 o superior</td>
    </tr>
    <tr>
      <td><strong>Servidor Web</strong></td>
      <td>Apache/Nginx (XAMPP, WAMP o Laragon recomendados)</td>
    </tr>
  </tbody>
</table>

### Pasos de Instalación

**1. Clonar el repositorio**

```bash
git clone https://github.com/<tu-usuario>/sigenor.git
```

```bash
cd sigenor
```

**2. Instalar dependencias**


```bash
composer install
```

**3. Configurar el entorno**


```bash
cp .env.example .env
```

**4. Configurar la base de datos**


Edita el archivo .env con las credenciales de MySQL:

```bash
ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=sigenor
DB_USERNAME=root
DB_PASSWORD=
```

**5. Importar la base de datos**

```bash
mysql -u root -p sigenor < "sigenor.sql"
```

**6. Ejecutar el servidor de desarrollo**

```bash
php -S localhost:8000
```

## 🧪 Pruebas

El sistema fue sometido a un riguroso proceso de validación:

*  Pruebas Unitarias: Validación de funciones individuales por módulo.

*  Pruebas de Integración: Comunicación entre componentes (Estudiantes, Calificaciones, Asistencias).

*  Pruebas de Sistema: Flujo completo desde el login hasta la generación de reportes.

*  Pruebas de Aceptación: Validación con usuarios reales del personal administrativo.

## 🎯 Impacto Social

La implementación del sistema SIGENOR ha producido una transformación sustancial en la dinámica operativa de la institución:

*  Reducción drástica de los tiempos de espera para la generación de documentos.

*  Trazabilidad digital completa de cada estudiante y su historial académico.

*  Protección de datos sensibles de los estudiantes y personal.

*  Posicionamiento institucional como una instancia moderna, eficiente y ambientalmente responsable (menor uso de papel).

*  Fortalecimiento del Poder Popular al dotar a la comunidad de una herramienta tecnológica de vanguardia.

## 📜 Licencia

📄 **Ver archivo [LICENSE](LICENSE) para más detalles.**
