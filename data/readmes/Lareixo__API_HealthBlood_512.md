# API HealthBlood 512 (Gluapi)

API REST de glucosa construida con **Java 21 + Jersey + Tomcat 11 + MySQL**.
El proyecto conserva las rutas originales con el contexto
`/API_HealthBlood_512`, las rutas cortas para navegador y las validaciones
existentes.

## Stack

- Java 21
- Jakarta REST (Jersey 4)
- Tomcat 11
- MySQL 8 en local / TiDB Cloud Starter en la nube
- Ant + NetBeans para el desarrollo local
- Docker para desplegar en Render

## Estructura

```
src/java/org/lasalle/       Codigo Java (controladores, modelos y REST)
web/                        index.html y WEB-INF/web.xml
web/swagger/                API Tester con Swagger UI y openapi.json
db/gluco_api.sql            Esquema y datos para MySQL local
db/gluco_api_tidb.sql       Esquema y datos para TiDB Cloud
Dockerfile                  Imagen de Tomcat con el WAR compilado
render.yaml                 Blueprint de Render
pruebas-endpoints.ps1       Suite de 34 pruebas de endpoints
bruno/API_HealthBlood_512/  Coleccion Bruno con el CRUD completo
```

## Ejecucion local

Requisitos: JDK 21+, MySQL 8, Tomcat 11 y NetBeans/Ant.

1. Crear la base local:

   ```powershell
   & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < db\gluco_api.sql
   ```

2. Compilar el WAR:

   ```powershell
   & "C:\Program Files\NetBeans-25\netbeans\extide\ant\bin\ant.bat" dist
   ```

3. Desplegar `dist\API_HealthBlood_512.war` en Tomcat o usar el script:

   ```powershell
   .\iniciar-proyecto.ps1
   ```

4. Abrir:

   ```text
   http://localhost:8080/API_HealthBlood_512
   ```

La guia detallada de ejecucion local esta en `COMO_EJECUTAR.md`.

## Variables de entorno

`ConnectionMysql` conserva los valores locales por defecto. En la nube se
configuran variables de entorno; nunca se guardan credenciales en el
repositorio.

| Variable      | Valor local por defecto | Uso en produccion                         |
|---------------|-------------------------|-------------------------------------------|
| `DB_HOST`     | `127.0.0.1`             | Host de TiDB Cloud                        |
| `DB_PORT`     | `3306`                  | `4000` en TiDB Cloud                      |
| `DB_NAME`     | `gluco_api`             | `gluco_api`                               |
| `DB_USER`     | `root`                  | Usuario de TiDB (incluye prefijo)         |
| `DB_PASSWORD` | `admin`                 | Contrasena de TiDB                        |
| `DB_PARAMS`   | Conexion local sin TLS  | `?sslMode=REQUIRED&...` para TiDB         |
| `DB_URL`      | vacio                   | Opcional: URL JDBC completa               |

Si se define `DB_URL`, se usa tal cual y no se arman `DB_HOST`, `DB_PORT`,
`DB_NAME` ni `DB_PARAMS`.

## Docker

```powershell
docker build -t api-healthblood-512 .
docker run --rm -p 8080:8080 `
  -e DB_HOST=host.docker.internal `
  -e DB_PORT=3306 `
  -e DB_NAME=gluco_api `
  -e DB_USER=root `
  -e DB_PASSWORD=admin `
  api-healthblood-512
```

La aplicacion queda en `http://localhost:8080/API_HealthBlood_512`.

El `entrypoint` lee la variable `PORT` que entrega Render y ajusta el conector
de Tomcat antes de arrancar. En local, si `PORT` no existe, usa `8080`.

## Despliegue en Render + TiDB Cloud

### 1. Crear la base en TiDB Cloud

1. Entrar a <https://tidbcloud.com/free-trial> y crear una instancia
   **Starter / MySQL Compatible**.
2. Elegir la region **AWS us-west-2 (Oregon)** para que quede cerca de Render.
3. Dejar el **spending limit en 0** para permanecer en el plan gratuito.
4. Crear la contrasena del usuario y copiar host, puerto `4000`, usuario y
   contrasena.
5. Importar el esquema y los datos:

   ```powershell
   mysql --host=<HOST> --port=4000 --user=<USUARIO> --ssl-mode=REQUIRED `
     --default-character-set=utf8mb4 < db\gluco_api_tidb.sql
   ```

TiDB es compatible con MySQL, pero usa `utf8mb4_general_ci` en lugar de
`utf8mb4_0900_ai_ci`. El script `db/gluco_api_tidb.sql` ya tiene ese ajuste.

### 2. Subir el repositorio a GitHub

```powershell
git init -b main
git add .
git commit -m "Deploy API HealthBlood 512"
git remote add origin https://github.com/<USUARIO>/API_HealthBlood_512.git
git push -u origin main
```

### 3. Crear el servicio en Render

1. En Render, elegir **New > Blueprint** y conectar el repositorio.
2. Render lee `render.yaml` y crea el servicio web gratuito en Oregon.
3. Completar las variables que Render solicita:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
4. Desplegar. El health check es
   `/API_HealthBlood_512/saludar`.

Al terminar, la API queda en:

```text
https://<NOMBRE-DEL-SERVICIO>.onrender.com/API_HealthBlood_512
```

### 4. Probar la API en la nube

```powershell
powershell -ExecutionPolicy Bypass -File .\pruebas-endpoints.ps1 `
  -BaseUrl "https://<NOMBRE-DEL-SERVICIO>.onrender.com/API_HealthBlood_512/api/glucosa" `
  -ShortBaseUrl "https://<NOMBRE-DEL-SERVICIO>.onrender.com/API_HealthBlood_512" `
  -TimeoutSec 120
```

El primer request puede tardar cerca de un minuto porque Render Free duerme
el servicio despues de 15 minutos de inactividad.

## Endpoints principales

| Funcion | Ruta API | Ruta corta |
|---|---|---|
| Salud | `/api/glucosa/saludar` | `/saludar` |
| Estado + base de datos | `/api/glucosa/estado` | `/estado` |
| Saludo personalizado | `/api/glucosa/saludarPersonalizado?nombre=...` | `/saludarPersonalizado?nombre=...` |
| Cuadrado | `/api/glucosa/Numero?numero=...` | `/Numero?numero=...` |
| Listar usuarios | `/api/glucosa/getAllUsuarios` | `/getAllUsuarios` |
| Obtener usuario por id | `/api/glucosa/getUsuarioById/1` | `/getUsuarioById/1` |
| Crear usuario (POST form) | `/api/glucosa/addUsuario` | `/addUsuario` |
| Crear usuario (GET navegador) | `/api/glucosa/addUsuario?...` | `/addUsuario?...` |
| Actualizar usuario (PUT JSON) | `/api/glucosa/updateUsuario/1` | `/updateUsuario/1` |
| Eliminar usuario (DELETE) | `/api/glucosa/deleteUsuario/1` | `/deleteUsuario/1` |
| Eliminar usuario + medidas | `/api/glucosa/deleteUsuario/1?cascade=true` | `/deleteUsuario/1?cascade=true` |
| Listar medidas | `/api/glucosa/getAllMedidas` | `/getAllMedidas` |
| Obtener medida por id | `/api/glucosa/getMedidaById/1` | `/getMedidaById/1` |
| Medidas por usuario | `/api/glucosa/getMedidasUsuario?idUsuario=1` | `/getMedidasUsuario?idUsuario=1` |
| Medidas por usuario (ruta) | `/api/glucosa/getMedidasUsuario/1` | `/getMedidasUsuario/1` |
| Alias por usuario | `/api/glucosa/getByUsuarioId?idUsuario=1` | `/getByUsuarioId?idUsuario=1` |
| Crear medida (POST form) | `/api/glucosa/addMedida` | `/addMedida` |
| Crear medida (GET navegador) | `/api/glucosa/addMedida?...` | `/addMedida?...` |
| Actualizar medida (PUT JSON) | `/api/glucosa/updateMedida/1` | `/updateMedida/1` |
| Eliminar medida (DELETE) | `/api/glucosa/deleteMedida/1` | `/deleteMedida/1` |

Los detalles y ejemplos de cada prueba estan en `PRUEBAS_ENDPOINTS.md`.

## API Tester (Swagger UI)

La aplicacion incluye un tester interactivo propio, servido desde el mismo WAR
(no depende de CDN y no tiene problemas de CORS):

| Entorno | URL |
|---|---|
| Local | `http://localhost:8080/API_HealthBlood_512/swagger/` |
| Render | `https://api-healthblood-512-h39y.onrender.com/API_HealthBlood_512/swagger/` |

Tambien se puede abrir desde el enlace **API Tester** del menu de la pagina
principal.

Para probar un endpoint:

1. Despliega el endpoint que quieras en la lista.
2. Pulsa **Try it out**.
3. Completa los parametros o el body JSON.
4. Pulsa **Execute** y revisa el codigo de respuesta y el cuerpo.

El archivo `web/swagger/openapi.json` describe todos los endpoints del CRUD y
los de sistema.

## CRUD en Bruno

La coleccion Bruno esta en `bruno/API_HealthBlood_512`. Incluye requests para
sistema, usuarios y medidas, con environments para Render y local.

1. Abre Bruno → **Collection** → **Open Collection**.
2. Selecciona `bruno\API_HealthBlood_512`.
3. Elige el environment **Render** o **Local**.
4. Sigue el orden del `README.md` de la coleccion.

Las requests de creacion guardan automaticamente el id generado en las
variables `idUsuario` e `idMedida` para usarlo en actualizar y eliminar.

## Pruebas

La suite contiene **34 pruebas** y valida endpoints, rutas cortas,
validaciones y respuestas de error.

```powershell
powershell -ExecutionPolicy Bypass -File .\pruebas-endpoints.ps1
```

## Notas de costo

- Render Free: 512 MB de RAM, se duerme tras 15 minutos sin trafico.
- TiDB Cloud Starter: 5 GiB de almacenamiento y 50 millones de RU al mes por
  instancia; con el spending limit en 0 no genera cobros.
- Las credenciales de TiDB se configuran en Render, no en GitHub.
