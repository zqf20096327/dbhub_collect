# 🏥🌍 Welsh Healthcare Spatial Analysis (PostgreSQL/PostGIS)

Advanced spatial SQL queries for analyzing healthcare access, vulnerable demographics, and environmental features in Wales.

## 📖 Overview
This research repository demonstrates the power of PostgreSQL combined with the PostGIS extension to perform complex spatial analytics on Welsh demographic and geographic data. By intersecting administrative boundaries (LSOAs) with infrastructure point data (GP surgeries, care homes, wind farms), this project uncovers critical insights into public health accessibility and environmental impacts on vulnerable populations.

## 🎯 Objectives & Queries
- **Query 1 (Proximity Analysis):** Calculate the exact distances between elderly care homes and historic landfill sites utilizing `ST_DWithin` and `ST_Distance`. This identifies vulnerable populations living in potentially hazardous environmental zones.
- **Query 2 (Access Index):** Calculate the ratio of population per Primary Care GP Surgery at the Local Authority (Council) level utilizing `ST_Intersects` and Common Table Expressions (CTEs).
- **Query 3 (Demographic Intersection):** Compare the percentage of elderly populations in LSOAs that contain wind farms versus those that do not, heavily utilizing `ST_Intersects` and weighted demographic aggregations.

## 🛠️ Technology Stack
- **Database:** PostgreSQL 18
- **Spatial Extension:** PostGIS
- **Coordinate Reference System:** British National Grid (EPSG:27700)
- **Tools:** pgAdmin, psql, QGIS (for visual verification)

## 📂 Project Structure
```text
welsh-healthcare-spatial-sql/
├── src/
│   └── spatial_queries.sql       # The raw, optimized SQL scripts
└── docs/
    └── IS4S703_Final_Report.docx # Academic report detailing the methodology
```

## ⚙️ Usage & Execution
These queries are designed to be run against a specific, normalized database structure containing the following schemas:
- `census`: Contains demographic data (e.g., `lsoas_age` tables).
- `admin`: Contains administrative boundaries (e.g., `councils`, `lsoas` polygons).
- `xtras`: Contains point infrastructure (e.g., `carehomes`, `historic_landfills`, `gp_surgeries`, `wind_farms`).

Execute the `.sql` script in your preferred database IDE (like pgAdmin or DBeaver) connected to the properly configured PostGIS database.



## 👨‍💻 Author
**Agha Abdullah**
- GitHub: [@AGHAABDULLAH](https://github.com/AGHAABDULLAH)
## ⚖️ License
This project is licensed under the MIT License.
