# 🚌 GTFS Route Service Intensity Analysis

A PostgreSQL analytics project designed to calculate transport route service intensity using General Transit Feed Specification (GTFS) data.

## 📖 Overview
GTFS is the worldwide standard for public transit schedules and associated geographic information. This repository contains SQL queries engineered to parse raw GTFS tabular data inside a PostgreSQL database to determine "service intensity." By aggregating trips by route, transit authorities and urban planners can identify which corridors carry the heaviest transit volume and which are under-served.

## 🎯 Objectives
- Join `routes` and `trips` tables from a standard GTFS dataset.
- Aggregate and count total scheduled trips per route identifier.
- Rank routes by total trips to easily identify the backbone of the transit network.

## 🛠️ Technology Stack
- **Database:** PostgreSQL
- **Data Standard:** GTFS (General Transit Feed Specification)

## 📂 Project Structure
```text
gtfs-route-analysis/
├── src/
│   └── route_intensity.sql  # The analytical SQL query
└── docs/
    └── Report.docx          # Academic submission detailing query rationale
```

## ⚙️ Usage
The provided SQL script expects a schema named `gtfs_aug24` containing standard GTFS tables:
- `gtfs_aug24.routes` (requires `route_id`, `route_short_name`, `route_long_name`)
- `gtfs_aug24.trips` (requires `trip_id`, `route_id`)

Run the script in any SQL client connected to the database to generate the intensity report.



## 👨‍💻 Author
**Agha Abdullah**
- GitHub: [@AGHAABDULLAH](https://github.com/AGHAABDULLAH)
## ⚖️ License
This project is licensed under the MIT License.
