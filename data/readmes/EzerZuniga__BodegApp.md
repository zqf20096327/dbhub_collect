<!-- README profesional en Markdown con estructura clara y elementos visuales -->

# Doña Rosa — Sistema Integral de Gestión Comercial

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen)]()

<p align="center">
	<!-- Si tienes un logo, colócalo en `assets/icons/images/logo.png` -->
	<img src="https://e7.pngegg.com/pngimages/707/566/png-clipart-computer-icons-inventory-management-software-order-management-system-business-process-stool-text-logo.png" alt="Doña Rosa logo" width="180" />
</p>

## Resumen ejecutivo

Doña Rosa es una aplicación de escritorio, desarrollada en Python, orientada a la gestión completa de bodegas y comercios minoristas. Su objetivo es centralizar operaciones (inventario, ventas, compras, proveedores, empleados y reportes) para mejorar la eficiencia operativa y reducir pérdidas por control deficiente de stock.

Este README ofrece instrucciones técnicas y operativas pensadas tanto para administradores de la solución como para desarrolladores que contribuyan al código.

---

## Contenido (rápido)

- Instalación y ejecución (Windows / Linux / macOS)
- Configuración y variables de entorno
- Inicialización de la base de datos y seeds
- Guía de desarrollo: linters, tests y hooks
- Empaquetado y creación de instalador (Windows)
- Seguridad, backup y recuperación

---

## Índice

1. [Requisitos](#requisitos)
2. [Instalación y ejecución](#instalaci%C3%B3n-y-ejecuci%C3%B3n)
3. [Configuración](#configuraci%C3%B3n)
4. [Inicialización de la base de datos](#inicializaci%C3%B3n-de-la-base-de-datos)
5. [Uso rápido](#uso-r%C3%A1pido)
6. [Estructura del proyecto](#estructura-del-proyecto)
7. [Desarrollo y pruebas](#desarrollo-y-pruebas)
8. [Empaquetado y distribución](#empaquetado-y-distribuci%C3%B3n)
9. [Seguridad](#seguridad)
10. [Contribuir](#contribuir)
11. [FAQ y troubleshooting](#faq-y-troubleshooting)
12. [Licencia y contacto](#licencia-y-contacto)

---

## Requisitos

- Python 3.8+ (recomendado 3.10/3.11)
- pip
- MySQL (opcional — para despliegues centralizados)
- Windows / macOS / Linux

## Instalación y ejecución

Instrucciones pensadas para desarrollo local.

Windows (PowerShell):

```powershell
# Activar entorno virtual (si existe)
& "C:/Users/jose/Desktop/PROYECTOS GIT/Sistema-Integral-de-Gesti-n-Comercial/.venv/Scripts/Activate.ps1"

# Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# (Opcional) Inicializar base de datos y cargar seeds
python scripts/setup_mysql_and_seeds.py

# Ejecutar la aplicación
python main.py
```

Linux / macOS (bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/setup_mysql_and_seeds.py
python main.py
```

### Modo debug y logging

- Activa `DEBUG=True` en `.env` o `config/environment.py` para logging más detallado.
- Revisa `core/logger.py` para la configuración del logger y niveles.

---

## Configuración

Crea un archivo `.env` en la raíz o ajusta `config/environment.py` con los valores de conexión y entorno.

Ejemplo mínimo:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=secret
DB_NAME=dona_rosa
DEBUG=True
SECRET_KEY=clave_segura
```

Revisa `config/settings.py` para opciones adicionales: rutas de datos, políticas de backup y parámetros de la UI.

---

## Inicialización de la base de datos

- Si usas MySQL: crea la base de datos y el usuario antes de correr los scripts.
- Ejecuta `python scripts/setup_mysql_and_seeds.py` para crear tablas y cargar datos iniciales.
- El directorio `data/seeds/` contiene ejemplos de usuarios y productos; puedes editarlos antes de cargar.

Comandos útiles:

```powershell
python scripts/test_mysql_connection.py
python scripts/setup_mysql_and_seeds.py
```

---

## Uso rápido

1. `python main.py` — inicia la aplicación.
2. Login con credenciales de seed (revisar `data/seeds`).
3. Módulos principales: Inventario, Proveedores, Compras, Ventas, Trabajadores.

### Flujo ejemplo — registrar una venta

1. Navega a `Procesos → Venta`.
2. Selecciona o crea cliente, agrega ítems desde inventario.
3. Finaliza venta y genera ticket (guardar copia en `data/backups/tickets/`).

---

## Estructura del proyecto 

```
.
├── app/
│   ├── app_context.py      # Inicializa contexto de la app, DI y singletons
│   ├── controller.py       # Controlador principal / orquestación de flujos
│   └── router.py           # Registro de rutas/vistas entre módulos
├── assets/
│   ├── icons/              # Iconos SVG/PNG usados en la UI
│   └── images/             # Capturas, logos y recursos estáticos
├── build/
│   ├── installer.iss       # Plantilla Inno Setup (Windows installer)
│   └── build.ps1           # Script PowerShell para generar instalador
├── config/
│   ├── database.py         # Conexiones y adaptadores a BD
│   ├── environment.py      # Lectura de variables de entorno / .env
│   └── settings.py         # Ajustes generales (paths, constantes)
├── core/
│   ├── auth.py             # Lógica de autenticación y sesiones
│   ├── authorization.py    # Reglas / roles / permisos
│   ├── logger.py           # Configuración del logging central
│   ├── security.py         # Funciones de seguridad (hash, salt)
│   └── utils.py            # Utilidades generales reutilizables
├── data/
│   ├── backups/            # Backups automáticos y manuales
│   ├── logs/               # Logs generados por la app
│   └── seeds/              # Datos de ejemplo y scripts de seed
├── models/
│   ├── producto.py         # Modelo Producto
│   ├── proveedor.py        # Modelo Proveedor
│   ├── venta.py            # Modelo Venta / Ticket
│   └── ...                 # Otros modelos del dominio
├── modules/
│   ├── inicio/             # Dashboard, vistas iniciales
│   ├── inventario/         # Vistas y lógica de inventario
│   └── procesos/           # Compras, ventas, emisión de tickets
├── services/
│   ├── producto_service.py # Operaciones del dominio (CRUD, validaciones)
│   ├── venta_service.py
│   └── ...
├── scripts/
│   ├── setup_mysql_and_seeds.py
│   ├── test_mysql_connection.py
│   └── tools/               # Scripts auxiliares (export, backup)
├── ui/
│   ├── components/         # Botones, tablas, modales reutilizables
│   │   ├── button.py
│   │   └── table.py
│   ├── login/              # Login view + controller
│   └── styles/             # Temas CSS/Python para la UI
├── requirements.txt
├── build.ps1
└── main.py                 # Punto de entrada de la aplicación
```

Descripción y convenciones útiles
- `app/`: punto donde se inicializan dependencias y se monta la aplicación. Si añades un nuevo módulo, registra su ruta en `router.py`.
- `config/`: mantiene la configuración por ambiente. No guardar credenciales en texto; usa variables de entorno o un gestor de secretos.
- `core/`: lógica transversal (auth, logging, seguridad). Evita introducir lógica de negocio aquí; usa `services/`.
- `modules/` + `ui/`: la UI se organiza por módulos; cada módulo debe contener sus vistas y controladores locales. Sigue la convención `modules/<nombre>/ <nombre>_view.py`.
- `services/` y `models/`: los `services` implementan reglas de negocio usando `models` como entidad; los controladores deben invocar a los services.
- `scripts/`: scripts de ayuda (migrations, seeds, export/import). Son utilitarios y no forman parte del runtime normal.
- `data/`: carpeta para backups y seeds; configúrala en `.gitignore` según tu política de backups.

Buenas prácticas recomendadas
- Añade tests en una carpeta `tests/` (unidad y/o integración) y usa `pytest`.
- Usa `pre-commit` con `black`, `isort` y `flake8` para mantener consistencia.
- Documenta nuevas rutas y comandos en `README.md` o en `docs/` si creas un conjunto mayor de documentación.

Si quieres, puedo:
- Generar automáticamente un `ARCHITECTURE.md` con diagramas y responsabilidades por módulo.
- Crear la carpeta `tests/` con un ejemplo de prueba y configurar `pytest` en `requirements-dev.txt`.
- Añadir un fichero `CODE_CONVENTIONS.md` con reglas de commit, style y estructura.


---

## Desarrollo y pruebas

Recomendaciones para colaboradores:

1. Crea un entorno virtual.
2. Instala dependencias: `pip install -r requirements.txt`.
3. Ejecuta linters y formateadores antes de commitear.

Instalación de herramientas de calidad:

```powershell
python -m pip install pre-commit black flake8 isort
pre-commit install
```

Ejecutar tests:

```powershell
python -m pip install pytest
pytest -q
```

PR checklist (sugerido):

- [ ] Tests añadidos/actualizados
- [ ] Documentación actualizada
- [ ] Código formateado (`black`) y revisado (`flake8`)

---

## Empaquetado y distribución

El repositorio incluye `build/installer.iss` y `build.ps1` para crear instaladores en Windows.

Flujo recomendado:

1. Generar ejecutable con PyInstaller (opcional):

```powershell
pyinstaller --onefile main.py
```

2. Crear instalador con Inno Setup usando `build/installer.iss`.

3. Probar instalador en máquinas objetivo y validar permisos y dependencias.

---

## Seguridad

- No subir credenciales a VCS. Usa `.env` o variables de entorno.
- Limita privilegios de la cuenta DB usada por la app.
- Valida y sanitiza entradas de usuario en puntos de persistencia.
- Respaldos regulares: `data/backups/` — automatiza con tareas programadas.

Si quieres, añado una guía de hardening y rotación de secrets.

---

## Contribuir

1. Fork del repositorio.
2. Crea una rama: `feature/<descripcion>` o `fix/<descripcion>`.
3. Incluye tests y documentación si aplican.
4. Abre un PR con descripción, cambios y pasos para probar.

Suggested commit message format:

```
type(scope): short description

body (optional)

footer (issue reference)
```

Ejemplo:

```
docs(readme): mejorar documentación de instalación Windows
```

---

## FAQ y troubleshooting

Q: No arranca la aplicación después de instalar dependencias.

A: Verifica la versión de Python, activa el entorno virtual y revisa `core/logger.py` para la traza. Ejecuta `python -m pip install -r requirements.txt` de nuevo.

Q: Error de conexión a MySQL.

A: Comprueba `config/environment.py` y ejecuta `python scripts/test_mysql_connection.py`.

---

## Licencia y contacto

Revisa `LICENSE` para detalles legales. Mantenedor: **Ezer Zúñiga** — abre un issue para soporte o propuestas de mejora.

---