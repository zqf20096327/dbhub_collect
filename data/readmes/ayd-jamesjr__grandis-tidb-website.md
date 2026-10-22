# Grandis Business Website (TiDB Cloud Integration)

## Overview
This is my updated full-stack web application for Grandis ("Build. Scale. Evolve."), featuring a 3-tier architecture with **PHP PDO** and **TiDB Cloud** (distributed MySQL engine).

## Architecture
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Backend**: PHP 8.x with PDO extension
- **Database**: TiDB Cloud (MySQL compatible)

## Setup Instructions

1. I imported `schema.sql` into your TiDB Cloud database instance.

2. I set my environment variables on Render or hosting provider:
   - `TIDB_HOST`
   - `TIDB_PORT`
   - `TIDB_DB_NAME`
   - `TIDB_USER`
   - `TIDB_PASSWORD`

3. I can now run `index.php` on any PHP web server (XAMPP / Render Web Service).
