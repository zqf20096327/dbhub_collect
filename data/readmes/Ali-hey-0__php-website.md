# EduPortal — PHP School Website

[![Build Status](https://img.shields.io/badge/build-pending-lightgrey.svg)](https://github.com/Ali-hey-0/php-website/actions)
[![License: Unspecified](https://img.shields.io/badge/license-none-lightgrey.svg)]()
[![Stars](https://img.shields.io/github/stars/Ali-hey-0/php-website)](https://github.com/Ali-hey-0/php-website/stargazers)

A minimal, pragmatic PHP + MySQL school portal intended as a learning starter or lightweight production prototype. Provides role-based users (student / teacher / admin), courses, enrollments, announcements, and a clear, opinionated structure for extension.

---

Table of contents
- About
- Screenshots
- Features
- Tech stack
- Quick start
- Configuration
- Database schema & seeds
- Project layout
- Security & best practices
- Deployment (Nginx / Docker)
- Tests & CI
- Contributing
- License & contact

---

About
-----
EduPortal is designed to be:
- Small and readable — plain PHP, minimal dependencies.
- Extensible — clear separation of routes, controllers, templates.
- Secure by default — prepared statements, password hashing, role checks.

Screenshots
-----------
(Replace these with real screenshots in /docs or /assets)
- Landing / course catalog — docs/screenshots/catalog.png
- Course page / enroll flow — docs/screenshots/course.png
- Admin dashboard — docs/screenshots/admin.png

Features
--------
- Role-based authentication: student, teacher, admin
- Course management (CRUD)
- Enrollment management with uniqueness enforced
- Announcements / resources attachments
- MySQL-backed storage with sample schema + seed
- Simple templating & routing-ready structure
- File upload support (configurable)

Tech stack
----------
- PHP 7.4+ (8.x recommended)
- MySQL 5.7+ / MariaDB
- (Optional) Composer for third-party libs
- Web server: Nginx / Apache / PHP built-in

Quick start — local
-------------------
1. Clone
   ```bash
   git clone https://github.com/Ali-hey-0/php-website.git
   cd php-website
   ```

2. Copy config
   ```bash
   cp config.example.php config.php
   # edit config.php to set DB credentials and BASE_URL
   ```

3. Create DB and import schema
   ```bash
   mysql -u DB_USER -p -e "CREATE DATABASE IF NOT EXISTS eduportal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   mysql -u DB_USER -p eduportal < sql/eduportal.sql
   ```

4. Create an admin user (quick)
   ```bash
   php scripts/create_admin.php --username=admin --email=admin@example.com --password='StrongP@ssw0rd'
   ```

5. Run dev server
   ```bash
   php -S 127.0.0.1:8000 -t public
   # Visit http://127.0.0.1:8000
   ```

Configuration
-------------
- Copy `config.example.php` to `config.php` and set:
  - DB_HOST, DB_NAME, DB_USER, DB_PASS
  - BASE_URL (e.g. https://example.com)
  - UPLOAD_DIR and max upload size
- Keep `config.php` out of version control (add to .gitignore).

Sample config.example.php
```php
<?php
return [
    'db' => [
        'host' => '127.0.0.1',
        'name' => 'eduportal',
        'user' => 'edu_user',
        'pass' => 'secret',
        'charset' => 'utf8mb4',
    ],
    'base_url' => 'http://localhost:8000',
    'upload_dir' => __DIR__ . '/storage/uploads',
    'max_upload_size' => 5 * 1024 * 1024, // 5MB
];
```

Database schema (sql/eduportal.sql)
----------------------------------
Included minimal schema; import with `mysql` as shown above.

Core tables:
```sql
CREATE DATABASE IF NOT EXISTS eduportal DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE eduportal;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('student','teacher','admin') NOT NULL DEFAULT 'student',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  teacher_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE enrollments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  course_id INT NOT NULL,
  enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY (user_id, course_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

CREATE TABLE announcements (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  body TEXT NOT NULL,
  author_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
);
```

Seed admin script (scripts/create_admin.php)
--------------------------------------------
A simple script to create an admin without direct SQL editing. Example usage shown in Quick start.

Project structure (recommended)
-------------------------------
- public/ — web root (index.php, assets, front controller)
- app/ or src/ — controllers, models, services
- templates/ or views/ — PHP templates
- config.example.php — sample config
- sql/ — schema and seed data
- scripts/ — maintenance helpers (create_admin.php)
- storage/ — uploads & generated files (not in repo)
- docs/ — screenshots, architecture diagrams
- README.md — this file

Routing & controllers
---------------------
- The project ships with a simple front controller pattern:
  - public/index.php dispatches to a router map -> controllers
  - Controllers call models/services and render templates
- Keep controllers thin; place business logic in service classes.

Security & best practices
-------------------------
- Always use PDO with prepared statements. Example:
  ```php
  $stmt = $pdo->prepare('SELECT * FROM users WHERE email = ?');
  $stmt->execute([$email]);
  ```
- Store passwords with password_hash() and verify with password_verify().
- Escape HTML output: htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8').
- Validate and sanitize all uploads; enforce MIME type and size checks.
- Store uploads outside the public web root or deny direct access via server config.
- Disable display_errors in production and log to files.
- Use HTTPS in production and enable HSTS.

Deployment examples
-------------------
Nginx (conceptual)
```
server {
    listen 80;
    server_name example.com;
    root /srv/eduportal/public;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    location ~ /\.(ht|git) {
        deny all;
    }
}
```

Docker Compose (quick dev)
```yaml
version: '3.8'
services:
  php:
    image: php:8.1-fpm
    working_dir: /var/www/html
    volumes:
      - ./:/var/www/html
    ports: ['9000:9000']
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpwd
      MYSQL_DATABASE: eduportal
      MYSQL_USER: edu
      MYSQL_PASSWORD: edupass
    volumes:
      - db_data:/var/lib/mysql
volumes:
  db_data:
```
Note: adapt webserver / php-fpm integration; this is for development.

Testing & CI
------------
- No automated tests included by default. Recommended:
  - PHPUnit or Pest for unit tests
  - Simple integration tests for critical flows (auth, enroll)
- Add GitHub Actions workflow to run tests and static analysis (PHPStan/Psalm).

Coding conventions & tips
-------------------------
- Follow PSR-12 where practical.
- Use namespaces (App\Controllers, App\Models, App\Services).
- Keep single responsibility: controllers orchestrate, services implement logic, models map DB rows.
- Use dependency injection where feasible (pass PDO or a DB wrapper to services).
- Avoid inline SQL in views; avoid mixing HTML heavy logic in controllers.

Common maintenance tasks
------------------------
- Backup DB: mysqldump eduportal > backup.sql
- Reset schema (dev only): mysql -u user -p eduportal < sql/eduportal.sql
- Create admin (script): php scripts/create_admin.php --username=admin ...

Contributing
------------
1. Fork the repository
2. Create a feature branch: git checkout -b feature/your-feature
3. Commit early, describe clearly
4. Push & open a PR
- Provide migration notes for DB changes.
- Add unit tests for new behavior.

License
-------
This repository currently has no explicit license. If you want to permit reuse, add a LICENSE file (MIT, Apache-2.0, etc.).

Maintainer & contact
--------------------
Owner: https://github.com/Ali-hey-0  
Repo: https://github.com/Ali-hey-0/php-website

Appendix — Helpful snippets
---------------------------
- Hash a password
  ```php
  $hash = password_hash('YourSecurePass', PASSWORD_DEFAULT);
  ```
- Verify a password
  ```php
  if (password_verify($plain, $user['password_hash'])) { /* ok */ }
  ```

If you want, I can:
- Generate a polished `config.php` and `scripts/create_admin.php` file.
- Add a minimal PDO-based DB wrapper and example controller/view pairs.
- Produce GitHub Actions CI for linting/tests and a Docker Compose dev environment.

GitHub Copilot Chat Assistant