# Grandis Business Website

A business website project for **Grandis — Build. Scale. Evolve.**, built with PHP and TiDB Cloud.

## Overview

This project combines a web frontend, a PHP backend, and a TiDB Cloud database to support a database-driven business website.

## Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** PHP 8.x
- **Database:** TiDB Cloud
- **Database access:** PHP PDO
- **Containerization:** Docker

## Project Structure

| File | Purpose |
|---|---|
| `index.php` | Main website entry point |
| `db.php` | Secure database connection configuration |
| `.env.example` | Example environment configuration (no real credentials) |
| `schema.sql` | Database schema |
| `style.css` | Website styling |
| `script.js` | Frontend interactions |
| `Dockerfile` | Container configuration |

## Configuration

The application requires these environment variables:

- `TIDB_HOST`
- `TIDB_PORT` (defaults to `4000`)
- `TIDB_DB_NAME`
- `TIDB_USER`
- `TIDB_PASSWORD`
- `TIDB_SSL_CA` (optional; defaults to the Linux system CA bundle)

For local development, copy `.env.example` to `.env` and enter your own database settings. The `.env` file is excluded from Git. On Render or another hosting platform, add the variables in the service's environment settings instead of uploading a `.env` file.

**TLS certificate verification is enabled.** The Docker image installs the Linux CA certificate bundle. If developing directly on Windows, follow the TiDB Cloud TLS instructions to download the ISRG Root X1 certificate and set `TIDB_SSL_CA` to its local PEM file path.

Never commit real database credentials, private keys, or production environment files to GitHub. If a credential has ever been committed to a public repository, rotate it in TiDB Cloud; removing it from the latest file does not remove it from Git history.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/ayd-jamesjr/grandis-tidb-website.git
   cd grandis-tidb-website
   ```

2. Copy `.env.example` to `.env` and fill in your TiDB Cloud connection values.
3. If running PHP directly on Windows, set `TIDB_SSL_CA` to the downloaded ISRG Root X1 PEM certificate path.
4. Import `schema.sql` into your TiDB database.
5. Ensure PHP 8.x and the PDO MySQL extension are available.
6. Run the application using a compatible PHP web server.

## Deployment

The project includes a Dockerfile and can be prepared for deployment on a compatible hosting platform. Configure all required environment variables in the hosting platform, then verify database connectivity, TLS certificate validation, and form submission before treating the deployment as production-ready.

## Project Category

**Grandis / Greatness — Business & Technology Project**

---

*Build. Scale. Evolve.*
