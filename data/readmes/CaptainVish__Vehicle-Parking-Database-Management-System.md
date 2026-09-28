# Vehicle Parking Database Management System

A PHP, MySQL, and Bootstrap web project for managing a college-style vehicle parking workflow: vehicle entry, exit details, parking categories, users, and reports.

## Features

- Dashboard and vehicle-category management.
- Register incoming vehicles and record outgoing details and charges.
- Search vehicles and generate date-range reports.
- User/admin profile and password screens.
- Printable vehicle details and a database-backed log view.

## Local setup

Use a local PHP web server with the `mysqli` extension and MySQL/MariaDB.

1. Clone the repository into the web server's document root, for example `htdocs/parking/`.
2. Create an empty database named `vpmsdb` and import [vpmsdb.sql](vpmsdb.sql).
3. Update [includes/dbconnection.php](includes/dbconnection.php) with your local database settings.
4. Configure the vehicle-log trigger using [Trigger.txt](Trigger.txt) and the original [Trigger.png](Trigger.png) reference. `Trigger.txt` contains a trigger **body**, not a complete `CREATE TRIGGER` statement; choose the table, event, and timing in your database tool using the reference and verify a sample log entry.
5. Start the server and database, then open `http://localhost/parking/`.
6. The original setup documents demo login `admin` / `123456`. Use this only for local sample data and replace default credentials before exposing the application.

Import the SQL into a disposable development database, not an existing production database. No fresh installation or trigger execution was tested during this documentation update.

## Project map

| Path | Purpose |
| --- | --- |
| `index.php`, `dashboard.php` | Login and dashboard |
| `add-vehicle.php` | Vehicle entry |
| `manage-incomingvehicle.php`, `manage-outgoingvehicle.php` | Parking workflow |
| `search-vehicle.php` | Vehicle lookup |
| `bwdates-reports-details.php`, `bwdates-report-ds.php` | Date-range reporting |
| `logtable.php`, `Trigger.txt` | Log view and trigger body |
| `includes/` | Shared UI and database connection |
| `vpmsdb.sql` | Schema and starter data |

## Limitations and next steps

This is an educational project, not a production parking/access-control system. Runtime and dependency versions are not pinned.

Before deployment, review authentication and role checks, password storage, prepared SQL statements, CSRF protection, input validation, charge calculations, and concurrent updates. Add a repeatable database setup and tests for entry → exit → reporting/logging.

Use fictional vehicle registrations and contact details in demos. Do not publish real owner information, database credentials, or live database exports.
