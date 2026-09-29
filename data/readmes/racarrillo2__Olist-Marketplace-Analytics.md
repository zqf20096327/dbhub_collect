# 📊 Análisis Olist Brazilian E-commerce

Pipeline ETL y plataforma de análisis interactivo sobre el marketplace brasileño Olist, que integra procesamiento de datos en la nube, análisis exploratorio y un dashboard visual desarrollado con Streamlit.

---

## 📁 Estructura del proyecto

```
Olist-Marketplace-Analytics/
│
├── app/
│   └── app.py                        # Dashboard interactivo (Streamlit)
│
├── data/
│   ├── olist_customers_dataset.csv
│   ├── olist_orders_dataset.csv
│   └── olist_order_items_dataset.csv
│
├── exports/
│   └── dataset_analitico.parquet     # Dataset consolidado generado por el pipeline
│
├── sql/
│   └── schema.sql                    # Definición del modelo relacional en TiDB Cloud
│
├── credenciales.py                   # Configuración de conexión a TiDB Cloud (no incluir en Git)
├── proyecto_final.ipynb              # Notebook principal: ETL + EDA
└── README.md
```

---

## 🎯 Objetivo

Construir un pipeline ETL completo y un modelo analítico para estudiar el comportamiento del marketplace Olist, respondiendo preguntas clave de negocio sobre:

- Evolución temporal de las ventas
- Distribución geográfica del revenue
- Comportamiento de compra de los clientes
- Relación entre precio y coste logístico
- Concentración del revenue por cliente

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Pandas | Procesamiento y transformación de datos |
| MySQL Connector | Conexión con TiDB Cloud |
| TiDB Cloud | Base de datos relacional en la nube (MySQL-compatible) |
| Matplotlib / Seaborn | Visualizaciones del EDA |
| Streamlit | Dashboard interactivo |
| PyArrow | Exportación del dataset en formato Parquet |

---

## ⚙️ Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/Olist-Marketplace-Analytics.git
cd Olist-Marketplace-Analytics
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install pandas mysql-connector-python matplotlib seaborn numpy pyarrow streamlit
```

### 4. Configurar credenciales de TiDB Cloud

Crea el archivo `credenciales.py` en la raíz del proyecto con el siguiente contenido:

```python
mysql_config = {
    "host":     "tu-host.tidbcloud.com",
    "port":     4000,
    "user":     "tu-usuario",
    "password": "tu-contraseña",
    "database": "olist"
}
```

> ⚠️ **Importante:** añade `credenciales.py` a tu `.gitignore` para no exponer credenciales en el repositorio.

---

## 🚀 Cómo ejecutar el proyecto

### Paso 1 — Ejecutar el notebook ETL + EDA

Abre y ejecuta `proyecto_final.ipynb` en orden. El notebook realiza:

1. Conexión a TiDB Cloud
2. Exploración y limpieza de los datasets
3. Carga de datos en las tablas SQL
4. Extracción del dataset analítico mediante JOIN
5. Exportación a `exports/dataset_analitico.parquet`
6. Análisis exploratorio completo (EDA)

### Paso 2 — Lanzar el dashboard

```bash
cd app
streamlit run app.py
```

---

## 🗄️ Modelo relacional

El pipeline carga los datos en tres tablas relacionadas en TiDB Cloud:

```
customers
─────────────────────────
PK  customer_id
    customer_city
    customer_state

orders
─────────────────────────
PK  order_id
FK  customer_id  →  customers.customer_id
    order_status
    order_purchase_timestamp

order_items
─────────────────────────
PK  order_id + order_item_id  (clave compuesta)
FK  order_id  →  orders.order_id
    price
    freight_value
```

El dataset analítico se obtiene mediante un JOIN entre las tres tablas, consolidando en una única tabla plana toda la información necesaria para el análisis.

---

## 🔄 Pipeline ETL

```
CSVs locales
     │
     ▼
Exploración y selección de columnas (Pandas)
     │
     ▼
Carga por lotes en TiDB Cloud (mysql-connector)
     │
     ▼
Query SQL con JOINs → Dataset analítico
     │
     ▼
Exportación a Parquet (exports/)
     │
     ▼
EDA + Dashboard (Streamlit)
```

La función `cargar_csv_en_tabla()` gestiona la inserción en lotes de 1.000 filas para optimizar el rendimiento y evitar timeouts en la carga masiva de datos.

---

## 📈 Análisis exploratorio (EDA)

El notebook realiza un EDA estructurado en dos bloques:

**Análisis univariante**
- Distribución de precios e identificación de outliers (histograma + boxplot)
- Distribución de costes de envío
- Frecuencia de estados de pedidos

**Preguntas de negocio respondidas**

| # | Pregunta | Tipo de análisis |
|---|---|---|
| 1 | ¿Cómo evoluciona el revenue a lo largo del tiempo? | Serie temporal mensual |
| 2 | ¿Qué estados generan mayor volumen de ventas? | Ranking geográfico |
| 3 | ¿Existe relación entre precio y coste de envío? | Scatter plot |
| 4 | ¿Qué % del revenue genera el top de clientes? | Curva de Pareto acumulada |

---

## 📊 Dashboard interactivo

El dashboard desarrollado en Streamlit permite explorar los datos de forma dinámica con filtros por **estado** y **año**. Incluye:

**KPIs principales**
- Total de pedidos
- Total de clientes únicos
- Revenue filtrado
- Ticket promedio por pedido

**Visualizaciones**
- Evolución mensual de las ventas
- Ventas por estado (ranking)
- Top 10 estados por volumen de pedidos
- Relación precio vs. coste de envío

---

## 💡 Hallazgos principales

- El revenue muestra una **tendencia de crecimiento progresivo** a lo largo del periodo analizado, con variaciones estacionales identificables.
- Existe una marcada **concentración geográfica**: unos pocos estados concentran la mayor parte del revenue y el volumen de pedidos.
- Los **costes logísticos** presentan una relación positiva con el precio del pedido, aunque con alta dispersión.
- La **gran mayoría de clientes realiza una única compra**, con un grupo reducido de compradores recurrentes.
- Una **pequeña proporción de clientes genera una parte desproporcionada del revenue total**, siguiendo un patrón Pareto.

---

## 📌 Notas

- El dataset fuente es el [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), disponible en Kaggle.
- Durante el desarrollo del pipeline fue necesario vaciar y recargar tablas para evitar conflictos de PRIMARY KEY al repetir ejecuciones de prueba.
- Si se producen errores con PyArrow en Windows, se puede usar `fastparquet` como motor alternativo: `pip install fastparquet`.
Proyecto de análisis de datos end-to-end basado en un marketplace brasileño de Olist (Kaggle). Integra SQL, Python, ETL, EDA y Streamlit para analizar ventas, clientes y pedidos mediante una base de datos cloud en TiDB.
