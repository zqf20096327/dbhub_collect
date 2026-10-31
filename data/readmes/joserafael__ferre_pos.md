# FerrePOS - Sistema POS, Inventario Fraccionado y Facturacion Bimonetaria (USD / VES)

Sistema integral de Punto de Venta (POS), control de inventario con soporte de unidades fraccionadas y facturacion bimonetaria (Dolares USD y Bolivares VES) disenado para ferreterias en Venezuela. El proyecto implementa una arquitectura desacoplada conformada por un Backend RESTful API en CodeIgniter 4, base de datos relacional en MySQL 8.0 y un Frontend SPA en Vue 3, todo orquestado mediante Docker Compose.

## Arquitectura y Stack Tecnologico

1. **Separacion Estricta**:
   - Backend y Frontend operan de forma independiente comunicandose exclusivamente mediante JSON sobre HTTP REST.
2. **Backend (`ferre_pos_api` - CodeIgniter 4 / PHP 8.4-FPM)**:
   - Controladores RESTful basados en `ResourceController` y `ResponseTrait`.
   - Autenticacion stateless mediante tokens JWT (HS256) a traves de filtro dedicado (`JwtAuthFilter`) y soporte CORS (`CorsFilter`).
   - Estandarizacion de respuestas JSON con la estructura `{"status": 200, "error": null, "messages": "...", "data": {...}}`.
   - Gestion de esquema y datos iniciales mediante Migraciones y Seeders de CodeIgniter 4.
3. **Base de Datos (MySQL 8.0 / InnoDB)**:
   - Prohibicion estricta de tipos `FLOAT` o `DOUBLE` para evitar errores de redondeo.
   - Montos monetarios (`costo_usd`, `precio_venta_usd`, subtotales, impuestos y totales): `DECIMAL(14,2)`.
   - Tasas de cambio (`tasa_ves`, `tasa_aplicada`): `DECIMAL(12,4)`.
   - Cantidades e inventario (`stock_actual`, `stock_minimo`, `factor_conversion`, `cantidad`): `DECIMAL(12,3)` para soportar ventas fraccionadas (metros, kilogramos, litros).
   - Transacciones ACID (`$db->transStart()` / `$db->transComplete()`) con bloqueo pesimista (`FOR UPDATE`) en operaciones de inventario, compras, ajustes y ventas.
4. **Frontend (`ferre_pos_web` - Vue 3 + Vite)**:
   - Vue 3 con Composition API (`<script setup>`), Pinia para gestion de estado reactivo, Vue Router y Axios.
   - Visualizacion simultanea de precios, subtotales, impuestos, pagos mixtos y vueltos en USD y VES calculados en tiempo real segun la tasa de cambio activa.

## Reglas de Negocio Principales

### 1. Gestion Bimonetaria (USD / VES)
- **Moneda ancla**: Dolar estadounidense (USD).
- Las compras o entradas de inventario pueden registrarse en USD o en VES, almacenando siempre el costo convertido a USD y congelando la tasa de cambio aplicada en el documento.
- El precio en Bolivares se calcula dinamicamente (`precio_venta_usd * tasa_activa`) en el POS, y cada factura emitida congela los montos en ambas monedas junto con el `tasa_cambio_id` y la `tasa_aplicada` del momento exacto de la transaccion.

### 2. Categorias, Unidades de Medida y Factor de Conversion
- Catalogo de categorias de ferreteria (Electricidad, Plomeria, Tornilleria y Fijacion, Construccion, Herramientas, Pinturas y Quimicos).
- Catalogo de unidades de medida (`UND`, `M`, `KG`, `L`, `CAJA`, `ROLLO`) con el indicador booleano `permite_decimales`.
- Soporte de `factor_conversion` en productos para transformar automaticamente las unidades de compra a unidades de venta al registrar facturas de proveedor (por ejemplo, compra de 1 `ROLLO` equivalente a `100.000 M` para la venta al detal por metro).

### 3. Kardex Inmutable
- Ninguna existencia en `productos.stock_actual` se modifica directamente sin generar un registro auditable en la tabla `movimientos_inventario`.
- Tipos de movimiento soportados:
  - `ENTRADA_COMPRA`
  - `SALIDA_VENTA`
  - `ANULACION_VENTA`
  - `AJUSTE_POSITIVO`
  - `AJUSTE_NEGATIVO`

### 4. Facturacion y Multipago Mixto (`venta_pagos`)
- Metodos de pago preconfigurados:
  - `EFECTIVO_VES` (VES - sin referencia obligatoria)
  - `EFECTIVO_USD` (USD - sin referencia obligatoria)
  - `PUNTO_DEBITO` (VES - requiere referencia/lote)
  - `PUNTO_CREDITO` (VES - requiere referencia/lote)
  - `BINANCE` (USD - requiere referencia/Order ID)
  - `ZELLE` (USD - requiere referencia)
  - `PAGO_MOVIL` (VES - requiere referencia)
- Una misma factura admite multiples pagos combinando USD y VES, calculando el monto equivalente en USD de cada abono y registrando el vuelto entregado en USD y/o VES.

## Capturas de Pantalla e Interfaz del Sistema

### 1. Punto de Venta (POS) Bimonetario
Interfaz ágil de caja y mostrador diseñada para ventas rápidas con doble visualización de precios (USD y VES) calculados en tiempo real según la tasa activa. Incluye botones de fraccionamiento rápido para artículos vendidos por metro o kilogramo (`+0.25`, `+0.50`, `+2.50`), filtrado por categorías y ticket de venta interactivo.

![Punto de Venta (POS) Bimonetario](./imagenes/2.png)

---

### 2. Cobro Multipago Mixto (USD / VES) y Vueltos
Modal de liquidación que congela la tasa de cambio de la factura. Permite combinar múltiples métodos de pago (Efectivo USD/VES, Punto Débito, Punto Crédito, Pago Móvil, Zelle, Binance) en una sola transacción, calculando equivalencias en dólares y saldos de vuelto o excedente en tiempo real.

![Cobro Multipago Mixto](./imagenes/3.png)

---

### 3. Dashboard Operativo Bimonetario
Panel de control con métricas en tiempo real: ventas del día en USD y VES, facturación acumulada, valorización total del inventario al costo, tasa de cambio BCV aplicada, recaudación desglosada por método de pago y panel de alertas de productos en stock mínimo.

![Dashboard Operativo Bimonetario](./imagenes/5.png)

---

### 4. Actualización y Registro Histórico de Tasa de Cambio
Ventana de control de la Tasa Oficial BCV activa que rige todo el sistema. Mantiene un registro histórico auditable de cada tasa fijada con fecha, hora exacta y el usuario que realizó la actualización.

![Actualización de Tasa de Cambio](./imagenes/1.png)

---

### 5. Kardex Inmutable y Trazabilidad de Inventario
Consulta detallada de todos los movimientos de stock (`ENTRADA_COMPRA`, `SALIDA_VENTA`, ajustes) con precisión de 3 decimales para unidades fraccionadas (metros, litros, kilos), balance anterior vs. resultante, costos unitarios bimonetarios y vinculación con documentos o facturas.

![Kardex de Inventario](./imagenes/4.png)

## Estructura del Proyecto

```text
ferre_pos/
├── docker/
│   └── nginx/
│       └── default.conf        # Configuracion de Nginx para el Backend API
├── ferre_pos_api/              # Backend RESTful API en CodeIgniter 4
│   ├── app/
│   │   ├── Controllers/Api/    # Controladores REST (Auth, TasaCambio, Producto, Inventario, Venta, etc.)
│   │   ├── Database/
│   │   │   ├── Migrations/     # Esquema completo MySQL 8 InnoDB (CreateFerrePosSchema)
│   │   │   └── Seeds/          # Datos iniciales (InitialFerrePosSeeder)
│   │   ├── Filters/            # Filtros JWT y CORS
│   │   ├── Libraries/          # Libreria JwtLib (HS256)
│   │   └── Models/             # Modelos de datos
│   └── .env                    # Variables de entorno del Backend
├── ferre_pos_web/              # Frontend SPA en Vue 3 + Vite + Pinia
│   ├── src/
│   │   ├── layouts/            # Layout principal con barra superior de tasa BCV activa
│   │   ├── router/             # Rutas protegidas de la aplicacion
│   │   ├── services/           # Cliente HTTP Axios con interceptores JWT
│   │   ├── stores/             # Stores de Pinia (auth, tasa, catalogos)
│   │   └── views/              # Vistas: PosView, ProductosView, InventarioView, VentasView, TasasView, etc.
│   └── vite.config.js          # Configuracion de Vite y proxy hacia el API
├── Dockerfile.php              # Imagen PHP 8.4-FPM con extensiones mysqli, pdo_mysql, redis, intl, bcmath, gd
├── Dockerfile.web              # Imagen Node 20 Alpine para el servidor de desarrollo de Vue 3
└── docker-compose.yml          # Orquestacion completa de contenedores
```

## Esquema de Base de Datos

El esquema relacional en `ferre_pos_db` esta compuesto por las siguientes tablas:

- `usuarios`: Operadores del sistema con roles `ADMIN` y `CAJERO`.
- `tasas_cambio`: Historial de tasas USD/VES con indicador de tasa `activa`.
- `categorias`: Clasificacion del catalogo de productos.
- `unidades_medida`: Unidades enteras y fraccionadas (`permite_decimales`).
- `metodos_pago`: Formas de cobro en `USD` y `VES` y exigencia de numero de referencia.
- `productos`: Catalogo con `unidad_compra_id`, `unidad_venta_id`, `factor_conversion`, costos/precios en USD, alicuota de IVA y stock fraccionado.
- `entradas_inventario` y `entrada_detalles`: Cabecera y renglones de compras a proveedores en USD o VES.
- `movimientos_inventario`: Kardex inmutable con saldo anterior, cantidad, saldo resultante y costos unitarios en ambas monedas.
- `ventas`, `venta_detalles` y `venta_pagos`: Facturas emitidas, detalle de articulos vendidos y desglose de pagos mixtos recibidos.

## Ejecucion con Docker

### Requisitos Previos
- Docker
- Docker Compose

### 1. Construir y levantar los contenedores
Desde la raiz del proyecto, ejecute:

```bash
docker compose up -d --build
```

### 2. Ejecutar migraciones y datos semilla (primera vez)
Si la base de datos esta vacia, inicialice las tablas y los catalogos base ejecutando:

```bash
docker exec ferre_pos_app php spark migrate --all
docker exec ferre_pos_app php spark db:seed InitialFerrePosSeeder
```

### 3. Servicios y Puertos Disponibles

| Servicio | Contenedor | URL / Puerto en Host | Descripcion |
| :--- | :--- | :--- | :--- |
| Frontend SPA (Vue 3) | `ferre_pos_web` | `http://localhost:5173` | Interfaz grafica de usuario (POS y Administracion) |
| Backend API (Nginx + PHP) | `ferre_pos_nginx` / `ferre_pos_app` | `http://localhost:8080/api` | API RESTful en CodeIgniter 4 |
| MySQL 8.0 | `ferre_pos_mysql` | `127.0.0.1:33061` | Base de datos `ferre_pos_db` (usuario: `user` / clave: `password`) |
| Redis | `ferre_pos_redis` | `127.0.0.1:63791` | Motor de cache en memoria |
| Redis Commander | `ferre_pos_redis_commander` | `http://localhost:8081` | Interfaz web para inspeccionar Redis |
| MailHog | `ferre_pos_mailhog` | `http://localhost:8025` | Interfaz web de pruebas de correo (SMTP en puerto `1025`) |

## Credenciales de Prueba

Una vez ejecutado el seeder `InitialFerrePosSeeder`, puede iniciar sesion en `http://localhost:5173` con cualquiera de las siguientes cuentas:

- **Administrador**:
  - Usuario: `admin`
  - Contrasena: `admin123`
- **Cajero**:
  - Usuario: `cajero`
  - Contrasena: `cajero123`

## Endpoints Principales de la API (`/api`)

- `POST /api/auth/login`: Autenticacion de usuario y emision de token JWT junto con la tasa activa.
- `GET /api/auth/me`: Datos del usuario autenticado.
- `GET /api/dashboard`: Resumen de indicadores (ventas del dia en USD/VES, alertas de stock bajo, tasa actual y ultimas facturas).
- `GET /api/tasas/activa`: Consulta publica de la tasa de cambio vigente.
- `GET /api/tasas` | `POST /api/tasas`: Historial y publicacion de nueva tasa de cambio USD/VES.
- `GET /api/categorias` | `POST /api/categorias` | `PUT /api/categorias/{id}` | `DELETE /api/categorias/{id}`: CRUD de categorias.
- `GET /api/unidades-medida` | `POST /api/unidades-medida`: Catalogo de unidades de medida.
- `GET /api/metodos-pago`: Catalogo de metodos de pago activos.
- `GET /api/productos` | `GET /api/productos/{id}` | `POST /api/productos` | `PUT /api/productos/{id}` | `DELETE /api/productos/{id}`: Gestion de productos.
- `GET /api/inventario/entradas` | `GET /api/inventario/entradas/{id}` | `POST /api/inventario/entradas`: Registro y consulta de compras a proveedores con conversion de unidades.
- `POST /api/inventario/ajustes`: Ajustes positivos y negativos de inventario.
- `GET /api/inventario/kardex`: Consulta del Kardex inmutable con filtros por producto y tipo de movimiento.
- `GET /api/ventas` | `GET /api/ventas/{id}` | `POST /api/ventas` | `POST /api/ventas/{id}/anular`: Emision de facturas POS bimonetarias con multipago y anulacion con reverso automatico de stock en el Kardex.

## Comandos Utiles de Mantenimiento

```bash
# Ver el estado de todos los contenedores
docker compose ps

# Consultar logs en tiempo real
docker compose logs -f

# Ejecutar comandos de CodeIgniter Spark dentro del contenedor PHP
docker exec ferre_pos_app php spark routes

# Detener los contenedores conservando los datos de MySQL y Redis
docker compose down

# Detener los contenedores y eliminar los volumenes de datos
docker compose down -v
```

## Pruebas Automatizadas (Testing)

### Backend (PHPUnit 10)
```bash
# Ejecutar en Docker:
docker exec -t ferre_pos_app ./vendor/bin/phpunit

# O en local:
cd ferre_pos_api && ./vendor/bin/phpunit
```

### Frontend (Vitest & Vue Test Utils)
```bash
# Ejecutar en Docker:
docker exec -t ferre_pos_web npm run test

# O en local:
cd ferre_pos_web && npm run test
```
