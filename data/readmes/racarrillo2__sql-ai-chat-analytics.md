# Proyecto Guiado: Analítica de una Plataforma de Chat con IA

## 📋 Descripción General

Este proyecto simula el trabajo de un **junior data analyst** en una startup de chat con IA llamada *NovaChat*. A través de SQL y Python, analizamos datos de usuarios, modelos de IA, conversaciones y tokens consumidos para responder preguntas estratégicas de negocio.

**Stack tecnológico:**
- Python 3.x
- MySQL (TiDB Cloud Serverless)
- Pandas
- Jupyter Notebook

---

## 🎯 Objetivos de Aprendizaje

- ✅ Conectarse a una base de datos **MySQL remota** desde Python
- ✅ Explorar y entender el esquema de datos (`SHOW TABLES`, `DESCRIBE`)
- ✅ Escribir consultas SQL complejas: `WHERE`, `GROUP BY`, `HAVING`, `JOIN`, subconsultas
- ✅ Traducir **preguntas de negocio** a SQL
- ✅ Transformar resultados en **DataFrames** para análisis
- ✅ Comunicar insights de datos de forma clara y accionable
- ✅ Crear un entregable profesional para portfolio

---

## 📊 Estructura de la Base de Datos

| Tabla | Descripción |
|---|---|
| `usuarios` | Usuarios registrados (id, nombre, email, país, plan, fecha_registro) |
| `modelos` | Catálogo de modelos LLM (nombre, proveedor, coste por 1k tokens, fecha lanzamiento) |
| `conversaciones` | Conversaciones entre usuario y modelo |
| `mensajes` | Mensajes individuales con tokens (input/output) |
| `feedback` | Valoraciones positivas/negativas de respuestas |
| `suscripciones` | Histórico de planes de pago |

---

## 🚀 Bloques del Proyecto

### **Bloque 1: Setup e Exploración**
- Instalación de dependencias (`pandas`, `mysql-connector-python`)
- Conexión a TiDB Cloud Serverless
- Definición de funciones helper (`run_query`, `execute`, `show_query`)
- Exploración del esquema de datos

**Aprendizaje clave:** Cómo conectar Python a una base de datos MySQL remota de forma segura.

---

### **Bloque 2: Warm-up — Conoce a tus usuarios y modelos**

**Ejercicios:**
1. **Distribución de usuarios por plan** → `GROUP BY` básico
2. **Catálogo de modelos ordenado por coste** → `ORDER BY`
3. **Modelos lanzados en 2024** → Filtrado por fecha con `YEAR()` o `BETWEEN`

**Insight:** Entender la composición de la base de datos y los principales jugadores (usuarios/modelos).

---

### **Bloque 3: Distribución y Filtros**

**Ejercicios:**
4. **Distribución de usuarios por país** → `GROUP BY` con `HAVING`
5. **Conversaciones por mes** → Agrupación temporal con `DATE_FORMAT()`

**Insight:** Identificar patrones geográficos y temporales de actividad.

---

### **Bloque 4: Métricas de Uso por Modelo**

**Ejercicios:**
6. **Tokens totales y promedio por modelo** → Multi-tabla `JOIN`
7. **Modelos más populares** → `COUNT(DISTINCT ...)` para contar únicos
8. **Coste estimado por modelo** → Cálculos financieros en SQL
9. **Tasa de feedback negativo** → `CASE WHEN` para conteos condicionales

**Insight:** Qué modelos son más usados, más costosos y mejor/peor valorados.

---

### **Bloque 5: Candidatos a Upgrade y Análisis Combinado**

**Ejercicios:**
10. **Usuarios free heavy users** → Identificar candidatos a upgrade
11. **Top 5 usuarios por gasto** → Análisis multi-tabla complejo
12. **Modelos por encima del coste medio** → Subconsultas escalares
13. **(Bonus) Adopción de modelos 2024** → Proporciones y `CASE WHEN`

**Insight:** Oportunidades de negocio (upgrades, optimización de costes).

---

## 🛠️ Instalación y Ejecución

### Requisitos Previos
- Python 3.7 o superior
- Acceso a una base de datos MySQL compatible (TiDB Cloud, MariaDB, etc.)

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/proyecto-chat-ai-analytics.git
   cd proyecto-chat-ai-analytics/Modulo_2/proyecto_guiado
   ```

2. **Instalar dependencias**
   ```bash
   pip install pandas mysql-connector-python jupyter
   ```

3. **Configurar credenciales de BD**
   - Abre `proyecto_guiado_sql.ipynb`
   - En la sección "Conexión a TiDB Cloud", reemplaza:
     - `host`
     - `user`
     - `password`
     - `database`
   
   > ⚠️ **Nunca subas credenciales reales a GitHub.** Usa un archivo `.env` o variables de entorno.

4. **Ejecutar el notebook**
   ```bash
   jupyter notebook proyecto_guiado_sql.ipynb
   ```
   - Ejecuta las celdas en orden (`Kernel → Restart & Run All`)
   - Los resultados aparecerán en DataFrames formateados

---

## 📝 Patrón SQL Clave: `CASE WHEN` para Conteos Condicionales

Uno de los patrones más importantes del proyecto es contar valores que cumplen una condición:

```sql
SELECT 
    modelo,
    COUNT(*) AS total,
    SUM(CASE 
        WHEN feedback = 'negativo' THEN 1
        ELSE 0
    END) AS negativos,
    ROUND(
        (SUM(CASE WHEN feedback = 'negativo' THEN 1 ELSE 0 END) * 100.0) 
        / COUNT(*),
        2
    ) AS porcentaje_negativo
FROM feedback
GROUP BY modelo
HAVING COUNT(*) >= 5;
```

**Lectura:** "Para cada modelo, cuenta cuántos feedbacks negativos hay y calcula su porcentaje sobre el total."

---

## 💡 Insights Principales

- **Usuarios:** Mayoría en plan free → Oportunidad de upgrade
- **Modelos:** GPT y Claude más caros pero más populares
- **Costes:** Concentrados en pocos modelos premium
- **Feedback:** Algunos modelos tienen tasas negativas > 20%
- **Adopción 2024:** Modelos nuevos aún tienen baja penetración

---

## 📚 Conceptos SQL Practicados

| Concepto | Ejercicio |
|----------|-----------|
| `GROUP BY` | #1, #4, #5, #6 |
| `HAVING` | #4, #9 |
| `JOIN` (multi-tabla) | #6, #7, #8, #9, #11 |
| `COUNT(DISTINCT ...)` | #7 |
| `CASE WHEN` | #9, #13 |
| `DATE_FORMAT()` | #5 |
| `YEAR()` / `BETWEEN` | #3 |
| Subconsultas escalares | #12 |
| Agregaciones con `ROUND()` | #8, #9, #12 |

---

## 🔐 Buenas Prácticas

✅ **Exploración previa:** `SHOW TABLES`, `DESCRIBE` antes de escribir queries  
✅ **Filtros `HAVING`:** Quita ruido (ej: grupos con < 5 registros)  
✅ **Conteos únicos:** Usa `COUNT(DISTINCT col)` para evitar duplicados en JOINs  
✅ **Cálculos de proporción:** Multiplica por `100.0` antes de dividir (evita truncaje)  
✅ **Documentación:** Comentarios en SQL explicando `JOIN` y lógica de negocio  
✅ **Limpieza de datos:** Valida valores nulos, outliers, fechas rotas

---

## 📦 Estructura del Repositorio

```
proyecto_guiado/
├── README.md                          # Este archivo
├── proyecto_guiado_sql.ipynb          # Notebook principal con todas las queries
└── .env.example                       # (Opcional) Template de credenciales
```

---

## 🎓 Próximos Pasos

Para expandir este proyecto:

1. **Visualizaciones:** Añade gráficos con Matplotlib/Plotly
2. **Dashboard:** Integra resultados en un dashboard (Streamlit/Metabase)
3. **Reportes automáticos:** Script Python que envíe reportes por email
4. **Predicción:** Regresión para estimar próximos costes
5. **Almacenamiento:** Exporta resultados a CSV/Parquet para BI tools

---

## ❓ FAQ

**P: ¿Cómo uso esto si no tengo una BD disponible?**  
R: Puedes crear una BD local con datos ficticios, o pedir acceso a TiDB Cloud (gratuito hasta ciertos límites).

**P: ¿Qué si no tengo experiencia en SQL?**  
R: Cada ejercicio tiene pistas. Empieza por los bloques 1-2, entiende cada `SELECT`, y ve subiendo dificultad.

**P: ¿Puedo usar SQLAlchemy o SQLModel?**  
R: Sí, pero el objetivo aquí es aprender SQL directo. Úsalos en proyectos posteriores.

---

## 👨‍💼 Autor

### Rafael Carrillo Mirabal 
#### Proyecto del **Bootcamp Data & IA — Módulo 2 (SQL y Python)**  
Bootcamp: UpgradeHUB

---

## 📄 Licencia

Este proyecto es de uso educativo. Siéntete libre de adaptarlo a tu aprendizaje.

---

**Hecho con ❤️ para aprender SQL desde casos reales.**
