# Spotify Analytics Dashboard

Proyecto de análisis de datos y visualización interactiva basado en canciones y artistas de Spotify utilizando Python, SQL, TiDB Cloud y Streamlit.

---

# Objetivo del proyecto

El objetivo del proyecto es desarrollar un flujo completo de análisis de datos, desde la limpieza y modelado relacional hasta la construcción de un dashboard interactivo.

El análisis se centra en características musicales y métricas de popularidad de canciones y artistas de Spotify.

---

# Tecnologías utilizadas

- Python
- Pandas
- NumPy
- SQL
- TiDB Cloud
- Streamlit
- Plotly
- Matplotlib
- Seaborn

---

# Dataset utilizado

- **Enlace:** https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks
- **Qué hay:** ~600k tracks con features de audio (energy, danceability, valence...) y catálogo de artistas.
- **Buenas preguntas:** ¿cómo ha evolucionado la energía/duración de las canciones por década? ¿qué géneros dominan en cada época? ¿hay correlación entre popularidad y features?
- **Nota:** 600k tracks es mucho — **muestread a 50-100k filas** antes de subir.

El proyecto utiliza dos datasets principales:

## `artists.csv`

Contiene información de artistas:

- id
- name
- followers
- popularity

## `tracks.csv`

Contiene información de canciones:

- id
- name
- popularity
- duration_ms
- explicit
- id_artists
- release_date
- danceability
- energy
- tempo


- **Usar 2 CSV:** `tracks.csv` y `artists.csv`.
- **Relaciones:** `artists` 1—N `tracks` (a través del campo artists/id_artists).
---

# Modelado relacional

Se creó una relación entre canciones y artistas mediante:

```sql
tracks.id_artists → artists.id
```

Utilizando:

- PRIMARY KEY
- FOREIGN KEY
- Tipos de datos adecuados en TiDB Cloud

---

# Flujo del proyecto

## 1. Limpieza de datos

Se realizó limpieza y transformación utilizando Pandas:

- Tratamiento de valores nulos.
- Eliminación de duplicados.
- Conversión de tipos de datos.
- Validación de claves foráneas.
- Filtrado de registros inválidos.

---

## 2. Creación de tablas SQL

Se diseñaron tablas relacionales en TiDB Cloud utilizando SQL.

Ejemplo:

```sql
CREATE TABLE artists (
    id VARCHAR(30) PRIMARY KEY,
    name VARCHAR(255),
    followers BIGINT,
    popularity INT
);

CREATE TABLE tracks (
    id VARCHAR(22) PRIMARY KEY,
    name VARCHAR(600),
    popularity TINYINT,
    duration_ms INT,
    explicit BOOLEAN,
    id_artists VARCHAR(22),
    release_date VARCHAR(10),
    danceability DECIMAL(5,3),
    energy DECIMAL(5,3),
    tempo DECIMAL(6,3),

    FOREIGN KEY (id_artists) REFERENCES artists(id)
);
```

---

## 3. Extracción del dataset analítico

Se construyó un dataset analítico mediante consultas SQL con JOIN.

```sql
SELECT
    t.id AS track_id,
    t.name AS track_name,
    t.popularity AS track_popularity,
    t.duration_ms,
    t.explicit,
    t.release_date,
    t.danceability,
    t.energy,
    t.tempo,
    a.id AS id_artists,
    a.name AS artist_name,
    a.followers,
    a.popularity AS artist_popularity
FROM tracks t
JOIN artists a
ON t.id_artists = a.id;
```

---

## 4. Preprocesamiento

Se realizaron transformaciones adicionales:

- Conversión de fechas a datetime.
- Revisión de nulos.
- Revisión de outliers.
- Creación de columnas derivadas.
- Generación de datasets limpios en formatos Parquet y Pickle.

---

## 5. EDA (Exploratory Data Analysis)

Se desarrolló un análisis exploratorio utilizando:

- Histogramas
- Scatter plots
- Boxplots
- Heatmaps
- Análisis temporal

Principales variables analizadas:

- Popularidad
- Energía
- Danceability
- Tempo
- Seguidores de artistas

---

## 6. Dashboard interactivo con Streamlit

Se desarrolló un dashboard con diseño inspirado en Spotify.

### Funcionalidades

- Métricas principales.
- Filtros interactivos.
- Visualizaciones dinámicas.
- Análisis temporal.
- Relación entre variables musicales.
- Top artistas por seguidores.

---

# Principales hallazgos

- La popularidad de canciones se concentra principalmente en valores bajos y medios.
- La cantidad de canciones aumenta en años recientes.
- No se observa una correlación lineal fuerte entre energía y popularidad.
- Los seguidores se concentran en pocos artistas principales.

---

# Estructura del proyecto

```text
spotify-project/
│
├── dashboard/
    ├── app.py
├── data/
│   ├── artists_limpio.csv
│   ├── artists.csv
│   ├── tracks_con_error_fk.csv
│   ├── tracks_limpio.csv
│   ├── tracks_para_cargar.csv
│   └── tracks.csv
│
├── proyecto_final_modulo2.ipynb (Notebook)
│
├── credenciales.py (Credenciales de conexion BD en TiBDCloud)
├── dataset/
    ├── dataset_analitico.parquet
    └── dataset_analitico_limpio.parquet
├── sql/
    ├── schema.zip
├── requirements.txt
└── README.md
```
Nota: Los ficheros csv origen (artists.csv y tracks.csv) contenidos en la carpeta "data/" no se encuentran presentes, se deben descargar desde el enlace Kaggle contenido en este README.md 

Los CSV generados en el proyecto (artists_limpio.csv, traks_con_error_fk.csv,tracks_limpio.csv,tracks_para_cargar.csv) no estan incluidos. Se generan ejecutando el fichero proyecto_final_modulo2.ipynb (Notebook)
---

# Cómo ejecutar el proyecto

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecutar el dashboard

```bash
streamlit run app.py
```

---

# Autor

Proyecto desarrollado como práctica de análisis de datos, modelado SQL y visualización interactiva.