# Studio IDE — Editor de Código Web para iPadOS y Escritorio

<p align="center">
  <img src="./docs/screenshots/01-studio-ide-overview.png" alt="Studio IDE — Vista General de las 3 Islas (Explorador, Editor CodeMirror 6 y Asistente IA)" width="100%">
</p>

**Studio IDE** es un entorno de desarrollo web ligero, modular y 100% offline-first sin servidores intermedios, diseñado específicamente para programar con fluidez desde un **iPad** (instalado como PWA a pantalla completa en Safari y adaptable a ventanas de **Stage Manager**) así como desde una **PC de escritorio**.

- **Versión actual:** `1.4.0`
- **Aplicación web (GitHub Pages):** https://mbouso420-spec.github.io/ide-ipad/
- **Manual de Usuario paso a paso:** [Ver Manual de Usuario completo (`MANUAL_DE_USUARIO.md`)](./MANUAL_DE_USUARIO.md)
- **Suite de pruebas automáticas:** 749 pruebas automatizadas en 181 suites (`npm --prefix tests test`: 1/1 ESLint + 748 pruebas unitarias y de QA en `test:unit`) + suites E2E en Chromium (`npm --prefix tests run test:e2e`) y WebKit/Safari (`npm --prefix tests run test:e2e:webkit`) (tests unitarios, 10 temas WCAG 2.1 AA y motor `themeManager`, rastreo y simulador de cuotas IA sin contaminación de estado, carga integral de imágenes en Live Preview HTML y DX de imágenes en editor, bundler de módulos ES offline, diagnósticos táctiles y linting JS/TS/TSX/JSON/HTML/CSS, lazy loading de runtimes, integridad PWA SW v36 con fix `mode: "navigate"` y poda LRU con pines protegidos, endurecimiento de sandbox/CSP/nonce en previews, concurrencia multi-pestaña, *Soak & Endurance*, *AppSec Auth Hardening* y pruebas E2E en navegadores reales, 0 fallos en la suite completa).

---

## Características principales

### 1. Interfaz de 3 islas optimizada para iPadOS y Escritorio
- **Isla izquierda (Explorador):**
  - Gestión de múltiples proyectos locales (con **5 plantillas iniciales** desde el modal de nuevo proyecto) o vinculados a repositorios de GitHub.
  - Árbol jerárquico de carpetas y archivos con creación, renombrado y borrado inline accesible (sin popups que bloqueen Safari ni pérdida de posición de scroll).
  - **Menú contextual táctil (`Long-Press` ~500ms y clic derecho):** menú flotante para renombrar, duplicar inteligentemente (ej. `archivo.copia.js`, `archivo.copia 2.js`), descargar y eliminar.
  - **Trampa de foco accesible:** navegación fluida con `Tab` / `Shift+Tab` dentro de los formularios inline.
  - **Exportación e importación segura:** descarga del proyecto completo en formato `.zip` estándar (PKZIP 2.0 nativo 100% offline) y límite de seguridad de 5 MB en importaciones con detección de codificación.
  - **Monitor de almacenamiento persistente:** indicador en vivo de cuota y uso (`navigator.storage.estimate`) y respaldo en Gist privado en la barra superior del explorador.
- **Isla central (Editor CodeMirror 6 con fallback resiliente):**
  - Soporte de pestañas múltiples con liberación inmediata de memoria (`dropFileState`) al cerrarlas y poda automática de estados inactivos cuando la pestaña pasa a segundo plano (`document.hidden`).
  - **Atajos de cierre rápido:** `Alt + W`, `Cmd + W`, `Ctrl + W` o clic central del mouse/trackpad (`auxclick`).
  - **Protección contra pérdida de datos:** diálogo modal de confirmación accesible (`#confirm-dialog`) si se intenta cerrar una pestaña con cambios pendientes frente al repositorio.
  - **Barra táctil de símbolos con Auto-Wrap:** al seleccionar texto y tocar delimitadores (`( )`, `{ }`, `[ ]`, `" "`, `' '`, ```` ``` ````), el contenido seleccionado se envuelve automáticamente conservando la selección interna.
  - **Paleta de apertura rápida (`Cmd + P` / `Ctrl + P`) y comandos (`Cmd + K` / `>`):** filtrado instantáneo de archivos con debounce, salto directo a línea mediante la sintaxis `:número` (ej. `app.js:140` o `:45`) y ejecución de acciones del IDE.
  - **Linting en vivo y Panel táctil de Diagnósticos (`diagnosticsPanel.js`):** análisis automático en vivo para **JavaScript, TypeScript/TSX (offline), JSON, HTML y CSS** (tanto en CodeMirror 6 como en el editor de respaldo), incluyendo **detección 100% offline de rutas de imágenes rotas, escapes `../` o discrepancias de mayúsculas/minúsculas** en HTML/CSS, con indicador interactivo en la barra de estado (`#status-diagnostics-btn`), regla visual en el scrollbar (`#editor-error-ruler`) y panel táctil deslizable (`#diagnostics-panel`) para saltar a cada error o advertencia con un toque.
  - **Soporte y gestión integral de imágenes y DX en editor:** visualización de imágenes (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, `.ico`) con cuadrícula de transparencia, dimensiones naturales (`ancho × alto px`) y tamaño; carga y reemplazo vía botón, Drag & Drop o portapapeles (`Ctrl+V` / `Cmd+V`); **autocompletado de rutas relativas de imágenes del proyecto** dentro de `<img src>`, `<source srcset>`, CSS `url(...)` y Markdown `![]()`; y **arrastrar/pegar imágenes directo sobre el editor** para importarlas de forma segura en `assets/` e insertar la referencia relativa en el cursor. Incrustación completa offline en Live Preview HTML (`<img>`, `<picture>`, `srcset`, favicons, posters, SVG `<image>`, `style.backgroundImage` dinámico vía JS, `import img from "./..."`, SVGs de Illustrator/Inkscape con `<![CDATA[...]]>` y fondos CSS hasta 5 MB sin agotar el presupuesto de hojas de estilo) y documentos Markdown (`![alt](...)`).
  - **10 Temas Visuales WCAG 2.1 AA (`themeManager.js`):** 8 temas oscuros (`Studio Dark`, `Dracula`, `Nord`, `Monokai`, `Tokyo Night`, `Catppuccin Mocha`, `Gruvbox Dark`, `OLED Negro Puro`) y 2 temas claros (`Studio Light`, `Solarized Light`), con tarjetas de muestra de colores (`#settings-theme-grid`) en Configuración → Apariencia y en la Paleta de Comandos (`Cmd + K`), sincronización de `<meta name="theme-color">`, `BroadcastChannel` multi-pestaña, reconfiguración dinámica de CodeMirror 6 (`{ dark: !isLight }`) y minimapa sensible al tema.
  - Resaltado de sintaxis para **Python, C, C++, HTML, CSS, JavaScript/TypeScript, JSON, Markdown y SQL**, autocompletado inteligente, vista dividida (*Split View*), minimapa lateral optimizado (con pausa de `ResizeObserver` en pestaña oculta), búsqueda/reemplazo y control de tamaño tipográfico.
- **Adaptación a Stage Manager y teclado virtual:**
  - Control dinámico de `visualViewport`, aislamiento de scroll (`overscroll-behavior: none` / `contain` + `contain: layout style`) y optimizaciones de composición/GPU en iPadOS.
  - Re-clamp dinámico e instantáneo de dimensiones de paneles ante cambios de orientación de pantalla (`orientationchange`, `screen.orientation`) o redimensionamiento de ventanas en Stage Manager.

### 2. Asistente de IA integrado (APIs gratuitas y seguras)

<p align="center">
  <img src="./docs/screenshots/04-ai-assistant.png" alt="Asistente de IA Integrado con Presupuesto de Contexto y Contador de Tokens en Vivo" width="100%">
</p>

- Conexión directa desde el navegador con niveles gratuitos de **Groq** (`openai/gpt-oss-120b`), **Google Gemini** (`AI Studio`), **OpenRouter** (`openrouter/free`) y **Mistral** (`La Plateforme`), con sincronización automática de modelos, **rastreo en vivo de cuota y restablecimiento** (cabeceras `x-ratelimit-*` de Groq/Mistral/OpenRouter, `retryDelay` de Gemini en `429`, cuenta regresiva en vivo de 1 s en Configuración → Modelos y visualización de cadencia aún sin API key) y **Modo Simulación visual** (`Simular cuota`) estrictamente en memoria para probar todos los estados (`Listo`, `Activo`, `Advertencia`, `Limitado`, `Restablecido`) sin alterar credenciales ni `localStorage`.
- **Menciones `@archivo` y planes multi-archivo:** autocompletado `@archivo` para adjuntar hasta 8 archivos adicionales del workspace al contexto y aplicación multi-archivo con **Visor de Diferencias (Diff)** selectivo y rollback atómico ante fallos.
- **Presupuesto y truncamiento inteligente de contexto:** preserva cabecera y pie del código advirtiendo líneas omitidas para evitar agotar la ventana de contexto de modelos gratuitos, con suspensión automática de cálculos de tokens cuando el panel de chat está oculto o en Modo Zen.
- **Contador de tokens en tiempo real:** estimador visual (~4 caracteres por token) en el compositor del chat sin clonar todo el proyecto.
- **Regeneración rápida de respuestas:** botón dedicado para reintentar la última consulta con un solo toque.
- **Saneamiento automático del historial y rutas:** limpia notas de interrupción y bloquea caracteres de control C0/C1 o BiDi en rutas detectadas dentro de bloques de código.
- **Enlaces Markdown seguros:** renderizado sanitizado con `target="_blank"` y `rel="noopener noreferrer"`, bloqueando esquemas no seguros (`javascript:`, `data:`).
- **Acciones directas en bloques de código:** *En cursor*, *Reemplazar código* (reemplaza limpiamente el archivo completo si no hay selección o el fragmento seleccionado si lo hay, evitando sobrescrituras accidentales en el cursor), *Copiar* y *Aplicar archivo* con apertura previa del **Visor de Diferencias (Diff)** visual en verde y rojo.

### 3. Vista previa contextual en vivo, Consola, Multi-Página, SQLite y C/C++

<p align="center">
  <img src="./docs/screenshots/02-live-preview-responsive.png" alt="Vista Previa Web Multi-Página con Selector Responsivo de Dispositivos (Móvil, Tablet y Escritorio)" width="100%">
</p>

- **Resolución inteligente de punto de entrada:** al presionar *Vista previa* estando parado en un `.js` o `.css`, el motor busca en el workspace el `.html` que lo referencia directamente o el `index.html` principal, ensayando la aplicación web completa en lugar de correr scripts aislados.
- **Navegación multi-página e Historial web:** Total Interceptor en el iframe que captura enlaces locales relativos (`<a href="contacto.html">`), envíos de `<form>` y llamadas de navegación programática (`location.assign`), ofreciendo botones de **Atrás / Adelante** y un selector desplegable de páginas HTML en la barra superior.
- **Precarga y descarga bajo demanda inteligente (GitHub Lazy):** en repositorios remotos donde los archivos no están descargados previamente (`contentLoaded: false`), el motor de vista previa descarga automáticamente el HTML destino y todos los assets CSS y JS vinculados antes de compilar el iframe, evitando pantallas en blanco y estilos rotos.
- **Inlining recursivo de `@import url(...)` en CSS y Bundler ES Modules 100% Offline (`moduleBundler.js`):** empaqueta hojas de estilo modulares con `@import`, transpila archivos `.ts`/`.tsx`/`.jsx` y compila grafos locales de `import`/`export` (incluyendo barril `index.ts`, ciclos, `.json`, `.css` e `import type`) dentro de un registro virtual compatible con la CSP estricta (sin depender de `blob:` URLs ni red en `<iframe srcdoc sandbox>`).
- **Selector de páginas HTML optimizado y sin duplicados:** exclusión de carpetas de dependencias y artefactos de empaquetado (`node_modules`, `.git`, `dist`, `build`, `.next`, `.cache`, `out`, etc.), deduplicación por ruta normalizada y desambiguación automática de nombres con rutas relativas para evitar opciones triplicadas.
- **Bases de datos SQLite en vivo (.sql):** ejecución directa de sentencias DDL/DML mediante WebAssembly en memoria (`sql.js`), tablas interactivas con paginación fluida de 50 filas por página (`PAGE_SIZE = 50`) y controles accesibles, contador de filas afectadas, editor de consultas rápidas y exportación segura a `.csv` o `.json` vía canal autenticado `postMessage` con tope de seguridad por filas.

<p align="center">
  <img src="./docs/screenshots/03-c-runner-interactive.png" alt="Runner C/C++ Nativo con Terminal Interactiva Paso a Paso y Detección de Errores GCC" width="100%">
</p>

- **Aislamiento y Runner nativo de C y C++ (.c, .cpp, .h) con fallback Clang WASM offline:** ejecución en un shell nativo del modal con **Terminal Interactiva Paso a Paso** (con línea de comando `>`, historial con flechas Arriba/Abajo, entrada por lotes `batch stdin`), compilación multi-archivo online en Wandbox (GCC 14 C17/C++20) y **fallback automático/manual 100% offline con `@yowasp/clang` WASM + runtime WASI preview1** en Web Worker (`-O1` por defecto para menor uso de RAM en iPadOS).
- **Detección y señalización de errores GCC (Línea roja y Tooltip):** parseo automático de las líneas de error del compilador (`file:line:col: error: ...`), marcación visual con fondo rojo en CodeMirror 6 (`addErrorMarker`) y tooltip flotante con el mensaje del compilador, más salto interactivo al hacer clic sobre el error en la terminal.
- **Optimización para repositorios gigantes e iPadOS:** empaquetado perezoso con filtrado de directorios pesados (`node_modules`, `.git`, `dist`, `build`, etc.), umbral máximo por archivo (512 KB), presupuesto adaptativo de assets en runtime (`8 MB` táctil / `32 MB` escritorio) y terminación automática de Web Workers de Pyodide (TTL inactivo 75 s) y Clang al pasar la pestaña a segundo plano (`document.hidden`) o cerrar la vista previa.
- **Selector de medidas responsivas (Device Switcher):** botones de alternancia en la cabecera del visor para probar el diseño en **Móvil (390px)**, **Tablet / iPad (820px)** y **Escritorio (100%)**.
- **Protección contra bucles infinitos (Loop Guard):**
  - **JavaScript / HTML / REPL:** instrumentación de bucles vía AST (Acorn) que interrumpe bucles infinitos a los 2,5 s indicando el número de línea exacto para proteger la memoria del iPad.
  - **Python 3:** ejecución aislada en un **Web Worker** en segundo plano (Pyodide WebAssembly) con botón de **Detener** inmediato que aborta bucles infinitos sin congelar la interfaz.
- **Consola integrada:** captura de `console.log`, `warn`, `error`, trazas de Python con `input()` inline y Mini-REPL JS/TS autenticado.

### 4. Persistencia offline y Sincronización avanzada con GitHub

<p align="center">
  <img src="./docs/screenshots/05-github-branches-sync.png" alt="Sincronización con GitHub, Gestión de Ramas y Commits Atómicos" width="100%">
</p>

- Autoguardado continuo en **`IndexedDB`** con respaldo síncrono de emergencia (`localStorage`) ante suspensiones repentinas de Safari.
- **Cliente nativo `fetch` para GitHub REST API v3 (sin dependencia CDN de `@octokit/core`):**
  - **Apertura instantánea sin clonar todo:** visualización del árbol de directorios con descarga perezosa (*lazy*) de archivos bajo demanda.
  - **Gestión de Ramas (Branches):** selector de rama activa y creación/bifurcación de nuevas ramas directamente desde el IDE.
  - **Pre-commit selectivo, Diff y Merge 3-way resiliente:** selección granular de archivos a incluir en el commit, descarte individual de cambios locales, detección de divergencias remotas (`RemoteAheadError`) y colisiones archivo-vs-carpeta antes de escribir en IndexedDB.
  - **Commits atómicos:** creación de árbol Git completo (altas, modificaciones y bajas en una sola transacción) preservando modos ejecutables (`100755`) y protección contra blobs binarios vacíos.
  - **Modo Offline:** descarga completa del repositorio (`[Offline]`) para trabajar en aviones o zonas sin conectividad.

---

## Seguridad y Arquitectura Offline

1. **Content Security Policy (CSP) Estricta y Sandbox Dinámico de Previews:**
   - `index.html` declara una directiva CSP restrictiva que autoriza únicamente las APIs oficiales de GitHub y proveedores de IA (`api.github.com`, `gist.githubusercontent.com`, `generativelanguage.googleapis.com`, `api.groq.com`, `openrouter.ai`, `api.mistral.ai`), el compilador de C/C++ (`https://wandbox.org`), CDNs certificados para ESM y librerías WebAssembly (`esm.sh`, `cdn.jsdelivr.net`) y orígenes de fuentes seguros (`fonts.googleapis.com`, `fonts.gstatic.com`).
   - `#preview-iframe` inicia con `sandbox="allow-scripts"` y ajusta permisos dinámicamente por modo (`""` en Markdown, `"allow-scripts"` en Imagen/SQL/Python y `"allow-scripts allow-popups allow-popups-to-escape-sandbox"` en HTML/JS/TS, eliminando `allow-modals` y `allow-downloads`), inyecta `<meta http-equiv="Content-Security-Policy">` estricto por modo, excluye rutas sensibles (`.env*`, `*.vault.json`, `*secret*`, `*credential*`, `*.pem`, `*.key`) del bridge de assets y autentica cada canal `postMessage` (preview, REPL, exportaciones SQL y `dispose`) mediante un **nonce criptográfico por sesión** almacenado en closure privada.
2. **Service Worker (`studio-ide-shell-v38` y `studio-ide-runtime-v2`):**
   - Estrategia **Network-First** con timeout acotado para el App Shell propio con reintentos exponenciales en precacheo, manejo estándar de `request.mode === "navigate"` vía `request.url` (evitando `TypeError` en Safari/WebKit y actualizando `./` y `./index.html`), guarda `only-if-cached`, soporte `{ ignoreSearch: true }` y protección contra respuestas HTTP 5xx sobre caché válido.
   - Pre-cacheo completo 1:1 de los 88 módulos y submódulos JS, 7 hojas CSS y 3 iconos PWA vigentes, más Acorn y las 15 dependencias CDN del importmap CodeMirror/Lezer (calentados en segundo plano en `activate` sin bloquear `self.skipWaiting()`, sin `@octokit/core` ni precalentamiento de Pyodide/Clang WASM durante `install`).
   - **Optimización para cuota y memoria en Safari/iPadOS:** poda LRU acotada por entradas (`180`) y bytes (`45 MB`) en `RUNTIME_CACHE` con **protección de pines** (CodeMirror 6 + Acorn nunca se evictan frente a WASM), throttling de poda (`15 s` / cada 5 escrituras), estimación realista para archivos `.zip`/`.whl`/`.bin` (`2 MB`) y `.wasm`/`.tar`/`.data` (`4 MB`), omisión de re-escaneo `.text()` sobre entradas `esm.sh` ya cacheadas y caché bajo demanda de binarios WASM pesados con timeout extendido de 60 s.
3. **Blindaje de Credenciales y Anti-Fuerza Bruta (`js/security/credentialGuard.js` y `js/security/keyVaultCrypto.js`):**
   - **Lockout progresivo y persistente (*Exponential Backoff & Lockout*):** ante intentos fallidos consecutivos (umbral de 4 fallos en `LOCKOUT_THRESHOLD`), bloquea nuevas peticiones/intentos por *scope* aislado (`github`, `ai:<providerId>` y `vault`) con ventanas progresivas de `30s -> 2m -> 5m` (`LOCKOUT_DURATIONS_MS`) persistidas entre recargas (`localStorage` / `sessionStorage`).
   - **Validación pre-vuelo de formato y entropía:** inspecciona localmente longitud, ausencia de espacios internos, prefijos esperados y entropía antes de ejecutar `fetch()` o importar packs de claves (`importKeysBundle`), bloqueando caracteres de control e inyecciones CRLF (`\r`/`\n`) en cabeceras HTTP.
   - **Lista negra de sesión por huella criptográfica:** registra huellas irreversibles de 96 bits (`fp_<24 hex>` sin fuga de longitud, `computeTokenFingerprint`) para credenciales rechazadas (`401`/`403`) y evita su reenvío repetido en la sesión sin almacenar el secreto rechazado.
   - **Higiene y redacción automática de secretos:** sanea mensajes de error, trazas, query strings sensibles y PATs clásicos/modernos mediante `redactSensitiveTokens` y enmascara vistas previas en el DOM con `maskCredentialPreview`.
   - **Bóveda cifrada portátil AES-GCM 256 endurecida (`keyVaultCrypto.js`):** exportación e importación protegida con contraseña maestra de **mínimo 10 caracteres** (≥5 caracteres distintos) y **310.000 iteraciones `PBKDF2-HMAC-SHA256`** + `AES-GCM-256` con AAD vía Web Crypto API (manteniendo retrocompatibilidad de lectura para bóvedas legado), accesible desde Configuración → Almacenamiento y directamente desde el panel del asistente IA.
4. **Privacidad de credenciales:**
   Las API Keys y tokens personales (PAT) de GitHub nunca se envían a servidores intermedios ni a CDNs externos (`githubService.js` usa `fetch` nativo); residen exclusivamente en `localStorage` o `sessionStorage` según la preferencia del usuario.
5. **Empaquetador ZIP Nativo:**
   Implementación pura en JavaScript sin librerías externas para exportar proyectos a `.zip` cumpliendo estrictamente con la CSP y operando 100% fuera de línea.

---

## Estructura del Proyecto

```text
.
├── index.html                        # Shell principal, CSP, importmap (15 módulos CodeMirror/Lezer), diálogos accesibles
├── manifest.json                     # Manifiesto Web App (PWA standalone para iPadOS y escritorio)
├── sw.js                             # Service Worker v36 (App Shell Network-First navigate-safe + Runtime Cache v2 LRU con pines)
├── .github/workflows/ci.yml          # CI en GitHub Actions (lint, Node QA, Chromium E2E y WebKit E2E)
├── .nojekyll                         # Desactiva el procesamiento de Jekyll en GitHub Pages
├── README.md                         # Documentación técnica y arquitectura de la solución
├── MANUAL_DE_USUARIO.md              # Manual exhaustivo para el usuario final (iPad y PC)
├── assets/
│   ├── icon.svg                      # Isotipo vectorial (full-bleed en zona segura para maskable)
│   ├── apple-touch-icon.png          # Icono 180x180 para inicio de iPadOS
│   └── icon-512.png                  # Icono 512x512 para instalación PWA
├── css/
│   ├── tokens.css                    # Tokens de diseño (OKLCH WCAG 2.1 AA en los 10 temas oscuros/claros, tipografía, espaciado)
│   ├── base.css                      # Reset accesible, overscroll-behavior, focus visible y reglas base
│   ├── layout.css                    # 3 islas, drawers para Stage Manager y gestión de visualViewport
│   ├── editor.css                    # Pestañas, CodeMirror 6, diagnósticos táctiles, minimapa y scrollbars
│   ├── chat.css                      # Panel de IA, medidor de tokens, menciones @archivo y Markdown seguro
│   ├── workspace.css                 # Árbol de archivos, menú contextual, ramas, Diff, visor y terminal C/C++
│   └── app.css                       # Importador central, utilidades globales y cascada táctil iOS/iPadOS
├── js/
│   ├── app.js                        # Raíz de composición central del IDE
│   ├── ai/
│   │   ├── chatController.js         # Orquestador del chat IA y guardas de visibilidad/rendimiento
│   │   ├── chatMessageView.js        # Motor DOM incremental SSE, bloques de código y planes multi-archivo
│   │   ├── chatPromptContext.js      # Menciones @archivo, estimación de tokens, prompts y comandos /fix /explain /test
│   │   ├── chatSettingsPanel.js      # Formulario de proveedores/modelos/claves, caché en memoria y acceso a bóveda
│   │   ├── markdownRenderer.js       # Renderizado Markdown seguro y detección endurecida de rutas/bloques
│   │   ├── mentionPopover.js         # Autocompletado `@archivo` (hasta 8 adjuntos) en el chat IA
│   │   └── providers.js              # Adaptadores de proveedores IA y validación/persistencia de credenciales
│   ├── editor/
│   │   ├── autocompleteCatalog.js    # Vocabulario por lenguaje, caché de identificadores y barra táctil
│   │   ├── codeFormatter.js          # Formateador offline determinista (Shift+Alt+F)
│   │   ├── editorManager.js          # Motor CodeMirror 6, auto-wrap, poda en segundo plano y diagnósticos
│   │   ├── errorMarkersController.js # Marcadores de error en gutter/regla lateral y enlace al panel táctil
│   │   ├── fallbackEditor.js         # Editor de respaldo offline con paridad de linting en vivo y minimapa
│   │   ├── languageConfig.js         # Configuración de lenguajes, extensiones y perfiles de sintaxis
│   │   ├── liveLinter.js             # Linting en vivo para JS (Acorn lazy), TS/TSX (offline), JSON, HTML y CSS
│   │   ├── minimap.js                # Minimapa lateral canvas con debounce, ResizeObserver y dpr <= 2
│   │   ├── smartReplace.js           # Reemplazo inteligente de fragmentos IA por similitud estructural
│   │   └── splitEditorController.js  # Vista dividida paralela con redimensionamiento sincronizado
│   ├── github/
│   │   ├── githubController.js       # Interfaz de repositorios, ramas, pre-commit selectivo y resolución de conflictos
│   │   ├── githubLocalBackupPanel.js # Respaldo en Gists privados y publicación segura de repositorios nuevos
│   │   ├── githubMerge.js            # Merge 3-way seguro, detección de colisiones archivo/carpeta y plan de pull
│   │   └── githubService.js          # Cliente nativo `fetch` GitHub REST v3 (sin @octokit/core), árboles y commits atómicos
│   ├── net/
│   │   └── networkErrors.js          # Manejo amigable y categorización de fallas de red
│   ├── preview/
│   │   ├── bundler/
│   │   │   ├── liveBindingsRewriter.js # Reescritura de live bindings ESM
│   │   │   ├── moduleAstScanner.js   # Escáner AST de imports/exports locales
│   │   │   ├── modulePathResolver.js # Resolución de rutas relativas, extensiones y barrels
│   │   │   └── virtualRuntime.js     # Registro virtual ESM compatible con CSP estricta
│   │   ├── html/
│   │   │   ├── assetResolver.js      # Resolución de assets binarios/texto con presupuesto RAM y filtro de secretos
│   │   │   ├── consoleBridge.js      # Puente consola/REPL autenticado con nonce, rate-limit y loop guard
│   │   │   ├── entrypointResolver.js # Detección de entrypoint HTML y navegación multi-página
│   │   │   └── standalonePreviews.js # Plantillas aisladas JS/TS/TSX e imágenes con CSP estricta
│   │   ├── ts/
│   │   │   ├── jsxExpander.js        # Expansión JSX/TSX 100% offline
│   │   │   ├── tsTokenizer.js        # Tokenizador léxico TypeScript/JSX
│   │   │   └── typeStripper.js       # Eliminación determinista de anotaciones de tipo TS
│   │   ├── clangWorker.js            # Web Worker módulo ES bajo demanda con @yowasp/clang WASM (`-O1`)
│   │   ├── cRunner.js                # Compilador C/C++ (Wandbox online + fallback automático/manual a Clang WASM)
│   │   ├── htmlBundler.js            # Fachada de empaquetado HTML/CSS/JS/TS con sanitización meta/base y CSP
│   │   ├── jsTokenUtils.js           # Utilidades compartidas de escaneo léxico JS y emparejamiento de delimitadores
│   │   ├── loopGuard.js              # Protección contra bucles infinitos en JS/HTML/REPL vía AST
│   │   ├── markdownPreview.js        # Renderizado sanitizado de vistas previas Markdown
│   │   ├── moduleBundler.js          # Fachada offline de módulos ES para iframe sandbox
│   │   ├── previewUtils.js           # Utilidades de rutas, sanitización SVG y escape seguro
│   │   ├── pythonRunner.js           # Ejecutor aislado Python 3 (Pyodide Worker con TTL 75s y rAF batching)
│   │   ├── sqlRunner.js              # Motor SQLite interactivo con sql.js (WASM), paginación y exportación por nonce
│   │   ├── tsTranspiler.js           # Fachada del transpilador 100% offline para TypeScript y JSX/TSX
│   │   └── wasiRunner.js             # Runtime WASI preview1 puro en navegador/Worker (stdin/stdout/proc_exit)
│   ├── search/
│   │   └── projectSearch.js          # Búsqueda y reemplazo global en proyecto con protección anti-ReDoS
│   ├── security/
│   │   ├── credentialGuard.js        # Lockout persistente, validación pre-vuelo, huellas 96-bit y redacción
│   │   └── keyVaultCrypto.js         # Bóveda portátil AES-GCM 256 + PBKDF2-SHA256 (310k iteraciones, ≥10 chars)
│   ├── storage/
│   │   ├── db/
│   │   │   ├── dbCore.js             # Inicialización y transacciones base de IndexedDB
│   │   │   ├── projectTemplates.js   # 5 plantillas de proyecto listas para iniciar
│   │   │   ├── workspaceEntries.js   # CRUD de archivos/carpetas y sanitización de rutas
│   │   │   ├── workspaceGithubSync.js # Estado de sincronización, cálculo de diffs y marcas de commit
│   │   │   └── workspaceProjects.js  # Gestión de proyectos locales y repositorios vinculados
│   │   ├── emergencyBackup.js        # Respaldo síncrono ante suspensiones repentinas de Safari
│   │   ├── fileImport.js             # Decodificación segura de archivos con límite de 5 MB
│   │   ├── storageQuota.js           # Monitor de cuota y uso (`navigator.storage.estimate`)
│   │   ├── workspaceDb.js            # Fachada unificada IndexedDB, diferencias locales y descarte de cambios
│   │   └── zipExporter.js            # Exportador ZIP nativo (PKZIP 2.0 y CRC-32)
│   ├── ui/
│   │   ├── binaryPreview.js          # Visor protegido de imágenes y archivos binarios (abort seguro de FileReader)
│   │   ├── confirmDialog.js          # Diálogo modal de confirmación accesible con protección anti-Enter accidental
│   │   ├── diagnosticsPanel.js       # Panel táctil de diagnósticos en vivo enlazado a la barra de estado
│   │   ├── diffModal.js              # Visor de diferencias LCS por archivo y multi-archivo con caché de sesión
│   │   ├── explorerController.js     # Árbol del explorador, long-press, duplicación y listeners pasivos
│   │   ├── globalSearchModal.js      # Modal de búsqueda y reemplazo global en proyecto
│   │   ├── icons.js                  # Iconografía SVG optimizada
│   │   ├── keyboardRouter.js         # Enrutador global de atajos de teclado (Cmd/Ctrl)
│   │   ├── layout.js                 # Re-clamp de paneles, rotación, rAF resize y Stage Manager
│   │   ├── livePreviewModal.js       # Previsualización con sandbox dinámico, nonce postMessage y selector de dispositivos
│   │   ├── projectModal.js           # Modal selector de 5 plantillas al crear proyectos locales nuevos
│   │   ├── quickOpenModal.js         # Paleta unificada: archivos (Cmd+P) y comandos (Cmd+K / >)
│   │   ├── settingsModal.js          # Gestión de 10 temas con tarjetas, cuotas/simulador IA, bóveda AES-GCM y atajos
│   │   ├── statusBarController.js    # Barra de estado: ruta, lenguaje, contador de diagnósticos, cursor y red
│   │   ├── symbolBar.js              # Barra táctil de símbolos dinámicos con Auto-Wrap
│   │   └── themeManager.js           # Motor centralizado de los 10 temas WCAG, meta theme-color, broadcast y toggle claro/oscuro
│   ├── utils/
│   │   ├── dom.js                    # Utilidades seguras de manipulación DOM y descarga de blobs
│   │   ├── encoding.js               # Conversión Base64/UTF-8 segura para archivos y binarios
│   │   └── storage.js                # Acceso tolerante a fallos sobre localStorage/sessionStorage
│   └── workspace/
│       ├── aiApplyBridge.js          # Aplicación de bloques y planes multi-archivo IA con Diff y rollback
│       ├── autosaveManager.js        # Autoguardado debounced en IndexedDB con respaldo ante QuotaExceededError
│       ├── broadcastSync.js          # Sincronización multi-pestaña vía BroadcastChannel
│       ├── commandPaletteRegistry.js # Registro centralizado de acciones para la Paleta de Comandos
│       ├── explorerActions.js        # CRUD del explorador, descargas, exportación ZIP, copia offline y Gist
│       ├── githubBlobCache.js        # Hidratación y caché local de blobs binarios/texto de GitHub
│       ├── githubLazySync.js         # Descarga perezosa (lazy) de archivos remotos bajo demanda
│       ├── projectLifecycle.js       # Cambio, creación y eliminación de proyectos, pestañas y formateador
│       ├── pwaBootstrap.js           # Tema inicial, restauración de credenciales y registro del Service Worker
│       └── tabManager.js             # Gestión del estado y ciclo de vida de pestañas abiertas
└── tests/                            # Suite automatizada con 749 pruebas en 181 suites + E2E Chromium y WebKit
```

---

## Verificación de Calidad y Pruebas

Para ejecutar la suite completa de pruebas unitarias y de integración sobre Node.js:

```bash
node --test tests/lint.test.js
npm --prefix tests test
npm --prefix tests run test:e2e
npm --prefix tests run test:e2e:webkit
```

Resultado actual:
- **1/1 verificación de análisis estático (ESLint)** limpia sobre `js/**/*.js`, `sw.js`, `scripts/*.js` y `tests/*.{js,mjs}` (`no-undef` + `no-unused-vars`).
- **749 pruebas automatizadas en Node** distribuidas en **181 suites** (`npm --prefix tests test` = **1/1 ESLint** + **748 tests unitarios/QA** en `npm --prefix tests run test:unit`: unitarias, regresiones de auditoría, motor de 10 temas WCAG + paridad DOM/CSS, rastreo de cuotas y simulador visual sin efectos secundarios, carga integral de imágenes en HTML preview y DX de imágenes en editor, bundler ES Modules multi-archivo offline, `@archivo` + diff multi-archivo, panel táctil de diagnósticos y linting JS/TS/TSX/JSON/HTML/CSS, WASI + fallback C/C++ WASM, pre-commit selectivo y descarte, 5 plantillas de proyecto, seguridad/rendimiento de previews con nonce y CSP, cliente GitHub sin Octokit, integridad PWA SW v36 con fix `navigate` y poda LRU con pines protegidos, concurrencia multi-pestaña, *Soak & Endurance*, *AppSec Auth Hardening*, bóveda WebCrypto endurecida, merge 3-way, formateador y TS/JSX), **0 fallos, 0 pruebas canceladas**.
- **Suite E2E en navegador real Chromium (`tests/browser.e2e.mjs`):** arranque, SW v36, IndexedDB, formateador + Undo, TSX/ES Modules multi-archivo en `iframe srcdoc` bajo CSP, Mini-REPL, AES-GCM WebCrypto (≥10 caracteres) y rotación iPadOS verificados en Chromium headless.
- **Suite E2E Cross-Engine en WebKit (`tests/webkit.e2e.mjs`):** render táctil iPadOS portrait/landscape sin desbordes, SW v36, IndexedDB, formateador, ES Modules multi-archivo en CSP y WebCrypto verificados en motor WebKit (Playwright, ejecutada en CI fuera de sandbox).

---

## Ejecución Local en Desarrollo

Para probar localmente la aplicación antes de subir cambios a producción:

```bash
# Servidor HTTP estático nativo de Python 3
python -m http.server 8080

# O bien mediante Node.js
npx serve .
```

Abrí `http://localhost:8080` en tu navegador. Para más información, consultá el [**Manual de Usuario (`MANUAL_DE_USUARIO.md`)**](./MANUAL_DE_USUARIO.md).

## Licencia

Este proyecto está bajo la Licencia MIT. Consultá el archivo [`LICENSE`](./LICENSE) para más detalles.  
Copyright (c) 2026 Mateo Bouso.
