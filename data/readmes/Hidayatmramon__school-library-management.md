# School Library Management

A library management app for a school, built with Laravel. It tracks students, books, publishers, and book borrowings.

## Features

- Full CRUD (Laravel resource controllers) for:
  - **Students:** name, student ID (NIS), class group, and rayon
  - **Rayons** and **student groups**
  - **Publishers**
  - **Books:** title, author, and publisher
  - **Borrowings:** borrower, book title, borrow and return dates, and notes

## Tech stack

- PHP 8.1, Laravel 10
- MySQL
- Blade templates, Vite

## Getting started

Requirements: PHP 8.1+, Composer, MySQL.

```bash
git clone https://github.com/Hidayatmramon/school-library-management.git
cd school-library-management
composer install
cp .env.example .env
php artisan key:generate
```

Create an empty database, then set `DB_DATABASE`, `DB_USERNAME`, and `DB_PASSWORD` in `.env`.

```bash
php artisan migrate
php artisan serve
```

## Roadmap

- Add authentication: all pages are currently open
- Link borrowings to students and books with foreign keys instead of plain text
- Escape or remove raw HTML output in views
- Replace `$request->all()` with validated data

## Status

Learning project, not actively developed. Do not deploy it publicly before authentication is added.
