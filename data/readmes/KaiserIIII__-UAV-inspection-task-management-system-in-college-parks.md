# Campus UAV Inspection Manager

[简体中文](README_zh.md)

A Flask application for coordinating campus drone inspections, from equipment allocation and task scheduling to abnormality tracking and repair review. The database layer targets GaussDB/openGauss and PostgreSQL-compatible environments.

## Features

- Dashboard for scheduled tasks, available equipment, completed inspections, and unresolved abnormalities.
- Drone, battery, pilot, and inspection-area records.
- Scheduling checks for equipment availability, battery charge, pilot status, and overlapping assignments.
- Inspection results linked to abnormality and repair records.
- SQL schema, sample records, and verification queries.

## Run locally

From the repository root:

```bash
cd uav_inspection_gaussdb
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a local `.env`:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=teaching
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_SCHEMA=yy_uav
```

Run `sql/schema_gaussdb.sql`, then `sql/seed_gaussdb.sql` in the database. Use `sql/test_queries.sql` to inspect the initialized records.

```bash
python app.py
```

Open <http://127.0.0.1:5000>.

## Implementation

| Area | Implementation |
| --- | --- |
| Web application | Python, Flask, Jinja templates |
| Database access | psycopg2, python-dotenv |
| Data model | Equipment, personnel, tasks, inspection results, abnormalities, repairs |
| Scheduling rules | End after start; available drone and pilot; available battery with at least 30% charge; no active drone or pilot time conflicts |

Application code is in [app.py](uav_inspection_gaussdb/app.py); database definitions are in [sql/](uav_inspection_gaussdb/sql/).

## Project status

This is a database application prototype. Production deployment requires password hashing, CSRF protection, authorization checks, a configured Flask secret, and a production server. Keep database credentials outside version control.

No project-wide license is currently specified.
