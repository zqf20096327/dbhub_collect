# Online-Movie-Booking

Movie Ticket Booking System (Core PHP + MySQL + Bootstrap)

This project is for college/study only.

## Cleanups done
- Added shared DB connection code in `app/db/` (so DB logic is not duplicated between `Database.php` and `admin/Database.php`).
- Updated DB connections to read from environment variables (required for running inside Docker).
- `Database.php` / `admin/Database.php` / `database_connection.php` are now thin wrappers around the shared implementation.

## Structure (without breaking existing links)
- `app/db/` - shared DB connection logic
- root `*.php` - public entry pages (kept where they are because many pages link relatively like `include("header.php")`)
- `admin/` - admin pages and admin templates
- `css/`, `js/`, `img/`, `image/`, `fonts/` - static assets (kept in-place)

## Docker (recommended)

### 1) Setup environment
Copy `.env.example` to `.env` (optional; defaults exist in `docker-compose.yml`):

`copy .env.example .env`

### 2) Start containers
Run from `online-movie-booking/`:

`docker compose up --build`

On the first MySQL startup, `moviebook.sql` is imported automatically.

### 3) Open the app
- Web: `http://localhost:8080`

## Default logins (from `moviebook.sql`)
Admin:
- Name: `Jainam`
- Password: `admin`

Example customer user:
- Username: `pratik`
- Password: `4550`

## Screenshots
## 1. Home page ##
![home1](https://user-images.githubusercontent.com/104883953/167260990-670d3197-5c62-44bc-b821-fcc8d0efd36d.jpg)
![home2](https://user-images.githubusercontent.com/104883953/167261156-947f1206-6d2f-48c5-b3ba-319ff50b2e95.jpg)

## 2. All Movie ##
![all movie](https://user-images.githubusercontent.com/104883953/167261026-0c6d020e-7963-4e33-85e9-97b2b118d2e6.jpg)

## 3. Seat Book ##
![seat book](https://user-images.githubusercontent.com/104883953/167261039-e45bb084-ed5a-4b43-b8d2-132a16100d41.jpg)

