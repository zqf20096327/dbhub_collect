# Carrito PWA

Tienda instalable en el celular: catálogo, carrito que persiste sin conexión
y pedidos que llegan a tu WhatsApp. Funciona sobre **Vercel** y **TiDB Cloud**.

- `public/` → aplicación (HTML/CSS/JS sin frameworks, service worker, manifest)
- `api/` → funciones serverless (Node, CommonJS) contra TiDB
- `db/` → esquema y datos de ejemplo para TiDB Cloud

---

## 1. Estado actual

Funciona sin base de datos en **modo demo** (catálogo local de `public/config.js`).
Al configurar `DATABASE_URL`, el catálogo y los pedidos se guardan en TiDB.

| Pieza | Archivo |
|---|---|
| Nombre de la tienda, WhatsApp, moneda | `public/config.js` |
| Catálogo real | tabla `producto` en TiDB |
| Pedidos | tablas `pedido` y `pedido_item` |
| Versión de la app | `public/version.json`, `public/sw.js`, `package.json`, meta en `index.html` |

---

## 2. Probar en la computadora

```powershell
cd C:\Users\Cristopher\Desktop\carrito-pwa
npm install
npm run dev
```

Abre `http://localhost:3000`. Sin `DATABASE_URL` verás el catálogo demo.

> El service worker sólo se registra en `localhost` o HTTPS. En `localhost` sí funciona.

---

## 3. Crear la base de datos en TiDB Cloud

1. Entra a <https://tidbcloud.com> → **Create Cluster** → plan **Serverless** (gratis).
2. Cuando esté listo, abre **Connect** y copia:
   - `Host`, `Port` (4000), `User` (termina en `.root`), `Password`.
3. En **SQL Editor**, pega y ejecuta `db/schema.sql` y luego `db/seed.sql`.
4. Arma tu cadena de conexión:

```
mysql://USUARIO.root:CONTRASEÑA@HOST:4000/carrito
```

> Si la contraseña tiene caracteres especiales (`@ # / ?`), codifícalos: `@` → `%40`, `#` → `%23`.

---

## 4. Subir a GitHub

```powershell
cd C:\Users\Cristopher\Desktop\carrito-pwa
git remote add origin https://github.com/TU-USUARIO/carrito-pwa.git
git branch -M main
git push -u origin main
```

(Crea antes el repositorio vacío `carrito-pwa` en GitHub, sin README.)

---

## 5. Desplegar en Vercel

1. <https://vercel.com/new> → **Import Git Repository** → elige `carrito-pwa`.
2. Framework Preset: **Other**. Build Command: *(vacío)*. Output Directory: **`public`**.
3. Antes de dar Deploy, en **Environment Variables** agrega:

| Variable | Valor |
|---|---|
| `DATABASE_URL` | la cadena `mysql://…` de TiDB |
| `WHATSAPP_NUMERO` | *(opcional, ya está en config.js)* |

4. **Deploy**. La URL queda tipo `https://carrito-pwa.vercel.app`.

Cada `git push` a `main` redespliega solo.

---

## 6. Instalar en el celular

**Android (Chrome):** abre la URL → menú ⋮ → *Instalar aplicación* (o el botón **Instalar** del header).
**iPhone (Safari):** abre la URL → botón Compartir → *Añadir a pantalla de inicio*.

Requisitos ya cumplidos: HTTPS, manifest con iconos 192/512 + maskable, service worker activo.

---

## 7. Publicar una nueva versión (y que el celular lo detecte)

Sube **los cuatro** números de versión juntos:

| Archivo | Qué cambiar |
|---|---|
| `public/version.json` | `"version": "1.2.0"` |
| `public/sw.js` | `const VERSION = '1.2.0';` |
| `public/index.html` | `<meta name="app-version" content="1.2.0">` |
| `package.json` | `"version": "1.2.0"` |

Luego `git push`. En el celular, al abrir o volver a la app:

1. Aparece la barra **“Nueva versión 1.2.0 disponible”**.
2. Al tocar **Actualizar**: se fuerza `reg.update()`, el service worker nuevo toma
   control (`skipWaiting`) y la página se recarga con los archivos nuevos.
3. El `activate` del service worker borra las cachés viejas (`carrito-<versión>`).

Si no quieres cambiar el número, basta con tocar `sw.js` (Vercel no lo cachea),
pero conviene llevar versión explícita para que el aviso sea visible.

---

## 8. Estructura de la API

| Endpoint | Método | Respuesta |
|---|---|---|
| `/api/productos` | GET | `{ fuente, productos[] }` |
| `/api/pedidos` | POST | `{ guardado, codigo, total }` |

Sin base de datos nunca falla: responde `fuente: "demo"` y el front usa el catálogo local.
El pedido siempre se envía por WhatsApp aunque el guardado en TiDB falle.

---

## 9. Notas

- Los iconos se regeneran con `npm run icons`.
- `Foto` en `producto` es `LONGBLOB`; si prefieres URLs, guarda la URL como texto y el
  front la usa tal cual (acepta `https://…`, `/ruta` o base64).
- Nunca subas `.env` al repositorio: ya está en `.gitignore`.
