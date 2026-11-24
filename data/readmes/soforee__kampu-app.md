<p align="center">
  <img src="kampu-backend/src/main/resources/boleta/logo-kampu.png" alt="Kampu Tour Manager" width="300" />
</p>

<h3 align="center">Plataforma integral de gestión operativa y comercial<br />para agencias de turismo y operadores de viajes</h3>

<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.16.0/icons/angular/angular-original.svg" alt="Angular" height="40" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.16.0/icons/java/java-original.svg" alt="Java" height="40" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.16.0/icons/spring/spring-original.svg" alt="Spring Boot" height="40" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.16.0/icons/oracle/oracle-original.svg" alt="Oracle" height="40" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.16.0/icons/tailwindcss/tailwindcss-original.svg" alt="Tailwind CSS" height="40" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Angular-18-DD0031?style=flat-square&logo=angular&logoColor=white" alt="Angular 18" />
  <img src="https://img.shields.io/badge/Spring_Boot-3.4-6DB33F?style=flat-square&logo=springboot&logoColor=white" alt="Spring Boot 3.4" />
  <img src="https://img.shields.io/badge/Java-21-ED8B00?style=flat-square&logo=openjdk&logoColor=white" alt="Java 21" />
  <img src="https://img.shields.io/badge/Oracle-21c_XE-F80000?style=flat-square&logo=oracle&logoColor=white" alt="Oracle 21c XE" />
  <img src="https://img.shields.io/badge/Seguridad-Spring_Security_+_JWT-1F2937?style=flat-square&logo=springsecurity&logoColor=white" alt="Spring Security + JWT" />
</p>

<p align="center">
  <a href="#descripción-general">Descripción</a> &nbsp;·&nbsp;
  <a href="#módulos-principales">Módulos</a> &nbsp;·&nbsp;
  <a href="#roles-y-permisos">Roles</a> &nbsp;·&nbsp;
  <a href="#arquitectura">Arquitectura</a> &nbsp;·&nbsp;
  <a href="#instalación">Instalación</a> &nbsp;·&nbsp;
  <a href="#equipo">Equipo</a>
</p>

---

## Descripción general

**Kampu** es una solución *Full Stack* que centraliza la operación completa de una agencia de viajes en una sola plataforma:

- **Lo comercial:** catálogo de paquetes, cotizaciones en línea, reservas, pagos multimoneda y la boleta por correo.
- **La logística:** salidas programadas, traslados, flota, personal de campo y proveedores.
- **La atención al viajero:** portal del cliente y gestión de la reserva sin crear cuenta.

Cada usuario ve solo lo que le corresponde: administración, ventas, guías, conductores y clientes trabajan sobre los mismos datos con permisos distintos. La base de datos Oracle aplica las reglas de negocio y la auditoría de cada cambio.

<table>
  <tr>
    <td align="center" width="25%"><b>5</b><br /><sub>roles con permisos propios</sub></td>
    <td align="center" width="25%"><b>Cotización</b><br /><sub>en línea sin crear cuenta</sub></td>
    <td align="center" width="25%"><b>Multimoneda</b><br /><sub>pagos con tipo de cambio</sub></td>
    <td align="center" width="25%"><b>Auditoría</b><br /><sub>de cada operación</sub></td>
  </tr>
</table>

---

## Módulos principales

<details>
<summary><b>Página principal y catálogo público</b></summary>
<br />

- Secciones a pantalla completa, un buscador de destinos y un catálogo de tours con la próxima fecha reservable.
- Cada tour ofrece **Reservar** (con cuenta) o **Cotizar** (sin cuenta).
</details>

<details>
<summary><b>Cotizador en línea sin cuenta</b></summary>
<br />

- El visitante elige la fecha, los pasajeros, los servicios adicionales y la habitación de hotel. El precio lo calcula el servidor.
- Al guardar recibe un **código y una clave** con los que puede:
  - volver a abrir la cotización y descargarla en PDF;
  - solicitar la reserva y seguir su estado en `/seguimiento`;
  - una vez confirmada, gestionar su reserva (pasajeros, pagos y anulación) sin registrarse.
</details>

<details>
<summary><b>Portal del cliente</b></summary>
<br />

- Registro de la cuenta web e inicio de sesión con correo o documento.
- Reservas, pasajeros, pagos informados, solicitudes de anulación y seguimiento de cada paquete.
</details>

<details>
<summary><b>Panel de control (Dashboard)</b></summary>
<br />
Resumen de métricas operativas, ocupación de salidas, alertas de operación y estado general de la agencia.
</details>

<details>
<summary><b>Catálogo de paquetes y servicios adicionales</b></summary>
<br />
Tours con itinerario por día, tarifas, días de operación, hora de inicio, puntos de recojo, fotos y servicios adicionales que se cobran por persona o por grupo.
</details>

<details>
<summary><b>Salidas, reservas y pasajeros</b></summary>
<br />

- **Salidas:** fecha, cupos y guía asignado.
- **Reservas:** registro, manifiesto de pasajeros y punto de recojo, con anulaciones y reembolsos.
- **Solicitudes de anulación:** las que envía el cliente las aprueba o rechaza el área de ventas.
</details>

<details>
<summary><b>Cotizaciones recibidas</b></summary>
<br />
Bandeja de solicitudes que llegan desde el cotizador público. Ventas las convierte en reservas o las rechaza.
</details>

<details>
<summary><b>Pagos multimoneda y boleta</b></summary>
<br />

- Registro y validación de pagos en soles o en otra moneda, con conversión automática.
- Al aprobar un pago, la **boleta informativa** se envía por correo.
</details>

<details>
<summary><b>Tráfico y traslados</b></summary>
<br />

- Traslados agrupados por salida, con la asignación de vehículo y conductor.
- La duración se estima por carretera con **OpenStreetMap (OSRM)**.
- Estados del traslado: programado → asignado → embarque → en ruta → finalizado.
</details>

<details>
<summary><b>Logística: personal, flota y proveedores</b></summary>
<br />

- **Personal y flota propios:** guías, conductores y vehículos de la agencia. Para la flota se registran el mantenimiento, el SOAT y la revisión técnica.
- **Proveedores externos:** su personal, sus vehículos y sus habitaciones de hotel.
- **Lugares:** se buscan en el mapa (Photon / OpenStreetMap).
</details>

<details>
<summary><b>Panel de campo: guías y conductores</b></summary>
<br />

**Conductor:**
- Avanza cada traslado y marca qué pasajeros abordaron.
- Abre la ruta en Google Maps o Waze.
- Registra el kilometraje y el combustible de su vehículo, y consulta su historial de viajes.

**Guía:**
- Inicia y finaliza el tour, y marca la asistencia de los pasajeros por día.
- Ve el transporte de cada salida y descarga el manifiesto en PDF.
- Registra sus certificaciones (carné e idiomas).

**Ambos:**
- Reportan novedades en ruta y bloquean horarios en los que no están disponibles.
- Reciben avisos cuando les asignan, cambian o cancelan un trabajo.
</details>

<details>
<summary><b>Usuarios y auditoría</b></summary>
<br />
Alta de cuentas internas con su rol y bitácora completa de altas, cambios campo por campo, bajas, inicios de sesión e intentos fallidos. La bitácora tiene filtros y se puede exportar.
</details>

<details>
<summary><b>Autenticación y seguridad</b></summary>
<br />

- **Spring Security + JWT:** el login entrega un token que el frontend envía en cada petición como `Authorization: Bearer`.
- **Contraseñas** guardadas con **BCrypt**. La cuenta se bloquea tras 5 intentos fallidos, y el mensaje de error es el mismo exista o no el usuario.
- **Permisos por endpoint** con `@PreAuthorize`. Sin sesión se responde **401** y sin permiso **403**, siempre en JSON.
- **En cada petición** se vuelve a comprobar que la cuenta siga activa y con su rol actual.
- **En el frontend**, *guards* de Angular protegen cada ruta según el permiso del usuario.
</details>

---

## Roles y permisos

| Rol | Usuario de prueba | Accede a |
|---|---|---|
| **Administrador** | `kadmin` | Todo el panel: usuarios, auditoría, tráfico, personal, vehículos y proveedores |
| **Ventas** | `kventas` | Reservas, pagos, clientes, cotizaciones y catálogo |
| **Guía** | `kguia` | Sus salidas asignadas, la asistencia, su historial de tours y su disponibilidad |
| **Conductor** | `kconductor` | Sus traslados, su vehículo, su historial de viajes y su disponibilidad |
| **Cliente** | `maria.rios@example.com` | Portal *Mi cuenta*: sus paquetes, pasajeros y pagos |

> La clave de todos los usuarios de prueba es `Kampu2026*`.
> Cotizaciones de visitante de prueba: `KC-<año>-000001` (clave `DEMO-2026-KAMP`) y `KC-<año>-000002` (clave `SOLI-2026-KAMP`).

---

## Arquitectura

```text
 ┌───────────────────────┐   HTTP + JWT   ┌──────────────────────────┐   JDBC    ┌──────────────────────────┐
 │  Angular 18 (SPA)     │ ─────────────► │  Spring Boot 3.4 (API)   │ ────────► │  Oracle Database 21c XE  │
 │  Tailwind · Signals   │ ◄───────────── │  Spring Security · JPA   │ ◄──────── │  Tablas · Vistas · PL/SQL│
 │  Guards · Interceptor │      JSON      │  JdbcTemplate · Swagger  │           │  Triggers · Auditoría    │
 └───────────────────────┘                └──────────────────────────┘           └──────────────────────────┘
        :4200                                    :8082/kampu                            :1521/xe
```

Monorepo desacoplado en dos aplicaciones:

<details open>
<summary><b>Estructura del proyecto</b></summary>

```text
kampu-tour-manager/
├── docs/                          # Atribuciones y licencias de las fotos
├── kampu-frontend/                # Single Page Application (Angular 18)
│   ├── public/                    # Fotos de destinos y banderas
│   └── src/app/
│       ├── core/                  # Modelos, servicios HTTP, sesión, guards, interceptor y utilidades
│       ├── features/              # Una carpeta por módulo (landing, cotizar, portal, reservas, pagos, campo...)
│       ├── layout/                # Contenedor del panel y navegación
│       └── shared/                # Componentes reutilizables (modal, íconos, logo, buscador...)
│
└── kampu-backend/                 # API REST (Java 21 / Spring Boot 3.4)
    └── src/main/
        ├── java/pe/edu/upeu/kampu/
        │   ├── auditoria/         # Bitácora de cambios y su consulta
        │   ├── config/            # Spring Security, CORS, OpenAPI y usuarios iniciales
        │   ├── controller/        # Controladores REST
        │   ├── dto/               # Objetos de transferencia y validaciones
        │   ├── entity/            # Entidades JPA
        │   ├── exception/         # Manejador global de excepciones y respuestas 401 / 403
        │   ├── repository/        # Spring Data JPA y acceso a paquetes PL/SQL
        │   ├── seguridad/         # JWT, filtro de autenticación y sesión actual
        │   └── services/          # Lógica de negocio, PDF, correo, mapas y moneda
        └── resources/
            ├── application.yaml   # Configuración
            └── db/kampu_bd.sql    # Script único de Oracle (esquema, PL/SQL y datos de demostración)
```

</details>

<details>
<summary><b>Tecnologías</b></summary>
<br />

| Capa | Tecnología |
|---|---|
| Frontend | Angular 18 (standalone, signals), Tailwind CSS 3, SweetAlert2 |
| Backend | Java 21, Spring Boot 3.4, Spring Data JPA, Spring Security, JWT (jjwt 0.11.5), Bean Validation |
| Base de datos | Oracle Database 21c XE: tablas, vistas, paquetes PL/SQL, triggers y roles |
| Documentos | OpenPDF (cotización y manifiesto), JavaMail (boleta) |
| Mapas | OpenStreetMap: Photon (búsqueda de lugares) y OSRM (rutas por carretera) |
| Documentación de la API | Swagger / OpenAPI (springdoc) |
</details>

---

## Instalación

### Requisitos previos

* **Java JDK 21**
* **Node.js 18+** y **npm**
* **Oracle Database 21c XE** (también funciona con Oracle 23 Free) y **SQL Developer**

> Orden de arranque: **Oracle → backend → frontend**.

### 1. Clonar el repositorio

```bash
git clone https://github.com/soforee/kampu-tour-manager.git
```

```bash
cd kampu-tour-manager
```

### 2. Base de datos

<details>
<summary><b>Ver pasos de la base de datos</b></summary>
<br />

1. En SQL Developer conéctate como **`SYSTEM`** al servicio `localhost:1521/xe`.
2. Abre `kampu-backend/src/main/resources/db/kampu_bd.sql` y ejecútalo completo como script (**F5**).
3. El script crea el usuario `KAMPU_BD` (clave `tour1234`), las tablas, las vistas, los paquetes PL/SQL y los datos de demostración.
4. Al final, sus pruebas internas deben mostrar `[OK]`. Los `ORA-` junto a un `[OK]` son pruebas que comprueban que la base **rechace** operaciones indebidas; no son errores.

> ⚠️ Cada ejecución del script **borra y vuelve a crear** todas las tablas de `KAMPU_BD`. No lo ejecutes sobre una base con datos reales.

</details>

### 3. Backend

<details>
<summary><b>Ver pasos del backend</b></summary>
<br />

```bash
cd kampu-backend
```

```bash
./mvnw spring-boot:run
```

- En Windows usa `mvnw.cmd spring-boot:run`, o ejecuta `KampuApplication` desde IntelliJ.
- El servidor arranca en **http://localhost:8082/kampu**.
- La documentación interactiva está en **http://localhost:8082/kampu/swagger-ui/index.html**.

**Configuración opcional (variables de entorno):**

| Variable | Uso |
|---|---|
| `KAMPU_JWT_SECRETO` | Clave en Base64 para firmar los tokens JWT. **Defínela antes de cualquier uso real** |
| `MAIL_USERNAME` / `MAIL_PASSWORD` | Cuenta de correo para enviar la boleta (en Gmail, una contraseña de aplicación). Si están vacías, no se envían correos |
| `KAMPU_CONTACTO_EMAIL`, `KAMPU_CONTACTO_TELEFONO`, `KAMPU_CONTACTO_CIUDAD`, `KAMPU_CONTACTO_INSTAGRAM`, `KAMPU_CONTACTO_FACEBOOK` | Datos de contacto de la agencia para la web, la boleta y el PDF |

Los mapas usan los servidores públicos de OpenStreetMap: solo se necesita internet en la PC del backend. Sin conexión, los lugares se llenan a mano y la duración de los traslados se estima en línea recta.

> Si al arrancar aparece *"no tiene las tablas del sistema"* o `ORA-00942`, el backend se conectó a una base donde no se ejecutó el script. Revisa la `url` de `application.yaml`.

</details>

### 4. Frontend

<details>
<summary><b>Ver pasos del frontend</b></summary>
<br />

En una nueva terminal:

```bash
cd kampu-frontend
```

```bash
npm install
```

```bash
npm start
```

- Abre la aplicación en **http://localhost:4200**.
- El archivo `proxy.config.json` redirige `/api` y `/kampu/images` al backend en el puerto 8082.
- Para producción, ejecuta `npm run build`; el resultado queda en `dist/frontend_kampu`.

</details>

---

## Equipo

<div align="center">
<table>
  <tr>
    <td align="center" width="200">
      <a href="https://github.com/soforee">
        <img src="https://github.com/soforee.png?size=100" width="90" alt="Russell Diaz Nuñez" /><br />
        <sub><b>Russell Diaz Nuñez</b></sub>
      </a><br />
      <sub>@soforee</sub>
    </td>
    <td align="center" width="200">
      <a href="https://github.com/stardolllar">
        <img src="https://github.com/stardolllar.png?size=100" width="90" alt="Doriann Gonzales Navarro" /><br />
        <sub><b>Doriann Gonzales Navarro</b></sub>
      </a><br />
      <sub>@stardolllar</sub>
    </td>
    <td align="center" width="200">
      <a href="https://github.com/ssh4123">
        <img src="https://github.com/ssh4123.png?size=100" width="90" alt="Rodrigo Usuriaga Salas" /><br />
        <sub><b>Rodrigo Usuriaga Salas</b></sub>
      </a><br />
      <sub>@ssh4123</sub>
    </td>
  </tr>
</table>
</div>

<p align="center"><sub>Las fotos de destinos se usan bajo licencia CC BY-SA. Autores y licencias en <a href="docs/ATRIBUCIONES_FOTOS.md">docs/ATRIBUCIONES_FOTOS.md</a>.</sub></p>
