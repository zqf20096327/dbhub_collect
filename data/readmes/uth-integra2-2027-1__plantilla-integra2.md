# Nombre del proyecto (EDITAR)

> Proyecto Integrador II · UTH · ciclo 2027-1 · Plataforma: **Django + TiDB Cloud (MySQL) + Render** · Dispositivos: **lector QR, cámara e impresora**

| | |
|---|---|
| **Equipo** | Grupo 5-_ · Equipo _ · Código Integra2: `I2-…` |
| **Problemática** | (EDITAR) |
| **Organización** | (EDITAR) |
| **App publicada** | https://(tu-app).onrender.com |
| **Seguimiento** | https://integra2.sistemasprado.mx (portal personal de cada integrante) |

## Integrantes y módulos

Cada integrante es **dueño de un módulo independiente** (su propia app de Django). Integra2 califica tu módulo de forma individual con base en tus commits dentro de su carpeta.

| Integrante | GitHub | Módulo | Carpeta | Dispositivo |
|---|---|---|---|---|
| (nombre) | @usuario | QR · registro por escaneo | `mod_qr/` | Lector QR USB / cámara |
| (nombre) | @usuario | Cámara · evidencia fotográfica | `mod_camara/` | Webcam / celular |
| (nombre) | @usuario | Impresión · etiquetas y tickets | `mod_impresion/` | Impresora térmica o de hoja |
| (nombre o «compartido») | @usuario | Análisis · instrumento y tablero | `mod_analisis/` | — |

El **núcleo** (`nucleo/`: modelo `Elemento` con su folio y la bitácora `EventoDispositivo`) es lo único compartido; cámbialo sólo de acuerdo con todo el equipo.

## Reglas que revisa Integra2 (léelas)

1. **Tu propia cuenta de GitHub** y `git config --global user.email "correo-de-tu-cuenta"`. Commits sin cuenta vinculada no cuentan.
2. **Haz commit y push el mismo día**, en **días distintos**. Si subes un commit más de 36 h después de hacerlo, cuenta el día en que llegó a GitHub.
3. **Mensajes que describan el cambio** (mínimo 12 caracteres; nada de «update», «cambios», «avance»).
4. **Zona roja**: las últimas 48 h antes de cada cierre (24 h en U1 y U4) no suman días y concentrar ahí tu trabajo resta puntos.
5. **Prohibido el force-push.** Protege `main`: Settings → Branches → Add rule → *Do not allow force pushes* y *Require status checks* (`revisar`).
6. **Fotos** (`foto_*.jpg`): con la **tarjeta de evidencia** impresa (portal → Imprimir tarjeta) visible, tomadas en la unidad y subidas **originales** (no por WhatsApp) para conservar la fecha EXIF. **Capturas** (`captura_*.png`): sin contraseñas. Mínimo 25 KB y 800 px. Usa **exactamente** los nombres de abajo.
7. La clave `INTEGRA2_CLAVE` va **sólo** en Render (Environment). **Nunca** en el repositorio.

Antes de cada push puedes revisar tus evidencias con `python tools/verificar_evidencias.py`.

## Cómo ejecutar

```bash
python -m venv .venv && .venv\Scripts\activate      # Windows
pip install -r requirements.txt
set DEBUG=1 && python manage.py migrate && python manage.py createsuperuser
python manage.py runserver
python manage.py test                                # pruebas del núcleo, integración y módulos
```

**Render**: New → Blueprint → este repositorio (usa `render.yaml`). Variables: `DATABASE_URL` (TiDB Cloud → Connect → `mysql://USUARIO:CLAVE@HOST:4000/BD`), `INTEGRA2_EQUIPO`, `INTEGRA2_CLAVE` y, la primera vez, `DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD`.

---

## Unidad 1. Introducción al desarrollo de proyectos de investigación y planteamiento del problema

**Periodo:** 11 ene 2027 → cierre **17 ene 2027, 23:59** · zona roja 24 h · mínimo **3 días** con commit válido por integrante.

### Entregables

- [ ] [Informe de la Unidad 1](docs/u1/informe_u1.pdf)

### Evidencias fotográficas

#### Equipo completo
📷 Foto con tarjeta U1 · Todos los integrantes con la tarjeta de evidencia U1.

![Equipo completo](evidencias/u1/foto_equipo.jpg)

#### Dispositivos del proyecto
📷 Foto con tarjeta U1 · Lector QR, cámara e impresora que usará el equipo, junto a la tarjeta U1.

![Dispositivos del proyecto](evidencias/u1/foto_dispositivos.jpg)

#### Clúster en TiDB Cloud
🖥️ Captura de pantalla · Clúster creado y base de datos del proyecto (sin mostrar contraseñas).

![Clúster en TiDB Cloud](evidencias/u1/captura_tidb.png)

#### Servicio en Render
🖥️ Captura de pantalla · Despliegue exitoso (Deploy live) del servicio web.

![Servicio en Render](evidencias/u1/captura_render.png)

#### Sitio publicado
🖥️ Captura de pantalla · Página inicial con el título, propósito y justificación de la investigación.

![Sitio publicado](evidencias/u1/captura_sitio.png)

### Bitácora del equipo

| Fecha | Integrante | Avance |
|---|---|---|
| | | |

---

## Unidad 2. Diseño y Metodología del proyecto de investigación

**Periodo:** 18 ene 2027 → cierre **31 ene 2027, 23:59** · zona roja 48 h · mínimo **5 días** con commit válido por integrante.

### Entregables

- [ ] [Informe de la Unidad 2](docs/u2/informe_u2.pdf)
- [ ] [Diagrama entidad-relación (PDF)](docs/u2/diagrama_er.pdf)
- [ ] [Borrador del instrumento de recolección](docs/u2/instrumento.pdf)

### Evidencias fotográficas

#### Visita o entrevista
📷 Foto con tarjeta U2 · Visita o entrevista con la organización de la problemática, con la tarjeta U2.

![Visita o entrevista](evidencias/u2/foto_visita.jpg)

#### Lector QR funcionando
📷 Foto con tarjeta U2 · Lector QR (USB o cámara) leyendo una etiqueta del sistema, con la tarjeta U2.

![Lector QR funcionando](evidencias/u2/foto_lector_qr.jpg)

#### Diagrama entidad-relación
🖥️ Captura de pantalla · Modelo de datos de las variables de la investigación.

![Diagrama entidad-relación](evidencias/u2/captura_er.png)

#### Panel de administración
🖥️ Captura de pantalla · Admin de Django en Render con los modelos migrados en TiDB Cloud.

![Panel de administración](evidencias/u2/captura_admin.png)

#### Escaneos registrados
🖥️ Captura de pantalla · Listado de lecturas QR guardadas en la base de datos.

![Escaneos registrados](evidencias/u2/captura_escaneos.png)

#### Aviso de privacidad
🖥️ Captura de pantalla · Aviso de privacidad publicado en la aplicación.

![Aviso de privacidad](evidencias/u2/captura_aviso.png)

### Bitácora del equipo

| Fecha | Integrante | Avance |
|---|---|---|
| | | |

---

## Unidad 3. Recopilación, análisis e interpretación de datos

**Periodo:** 1 feb 2027 → cierre **21 feb 2027, 23:59** · zona roja 48 h · mínimo **7 días** con commit válido por integrante.

### Entregables

- [ ] [Informe de la Unidad 3](docs/u3/informe_u3.pdf)
- [ ] [Reporte de la prueba piloto del instrumento](docs/u3/prueba_piloto.pdf)
- [ ] [Datos recopilados (anonimizados)](data/u3/datos_anonimizados.csv)

### Evidencias fotográficas

#### Cámara capturando
📷 Foto con tarjeta U3 · La cámara del sistema tomando la foto de un registro, con la tarjeta U3.

![Cámara capturando](evidencias/u3/foto_camara.jpg)

#### Impresora en uso
📷 Foto con tarjeta U3 · La impresora imprimiendo una etiqueta o ticket con QR, con la tarjeta U3.

![Impresora en uso](evidencias/u3/foto_impresora.jpg)

#### Etiqueta escaneada
📷 Foto con tarjeta U3 · Etiqueta impresa siendo leída por el lector QR, con la tarjeta U3.

![Etiqueta escaneada](evidencias/u3/foto_etiqueta.jpg)

#### Recolección en campo
📷 Foto con tarjeta U3 · Aplicación del instrumento o uso real del sistema con la población, con la tarjeta U3.

![Recolección en campo](evidencias/u3/foto_campo.jpg)

#### Registro con foto
🖥️ Captura de pantalla · Registro con la foto tomada por la cámara y su marca de agua.

![Registro con foto](evidencias/u3/captura_registro_foto.png)

#### Instrumento publicado
🖥️ Captura de pantalla · Encuesta o instrumento de recolección en la app.

![Instrumento publicado](evidencias/u3/captura_encuesta.png)

#### Tablero de resultados
🖥️ Captura de pantalla · Gráficas de los datos recopilados.

![Tablero de resultados](evidencias/u3/captura_tablero.png)

### Bitácora del equipo

| Fecha | Integrante | Avance |
|---|---|---|
| | | |

---

## Unidad 4. Elaboración de informe final, presentación y divulgación

**Periodo:** 22 feb 2027 → cierre **1 mar 2027, 23:59** · zona roja 24 h · mínimo **3 días** con commit válido por integrante.

### Entregables

- [ ] [Informe final de investigación](docs/u4/informe_final.pdf)
- [ ] [Cartel](docs/u4/cartel.pdf)
- [ ] [Propuesta de artículo](docs/u4/articulo.pdf)
- [ ] Etiqueta (tag) v1.0 en el repositorio (`git tag v1.0 && git push --tags`, y crear el Release en GitHub)

### Evidencias fotográficas

#### Cartel impreso
📷 Foto con tarjeta U4 · El cartel impreso con la tarjeta U4.

![Cartel impreso](evidencias/u4/foto_cartel.jpg)

#### Ensayo de la presentación
📷 Foto con tarjeta U4 · El equipo ensayando la presentación con la tarjeta U4.

![Ensayo de la presentación](evidencias/u4/foto_ensayo.jpg)

#### Micrositio de divulgación
🖥️ Captura de pantalla · Página /divulgacion/ publicada en Render.

![Micrositio de divulgación](evidencias/u4/captura_micrositio.png)

#### Release v1.0
🖥️ Captura de pantalla · Release v1.0 publicado en GitHub.

![Release v1.0](evidencias/u4/captura_release.png)

### Bitácora del equipo

| Fecha | Integrante | Avance |
|---|---|---|
| | | |

---
