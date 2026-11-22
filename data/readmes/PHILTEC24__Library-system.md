<div align="center">
  <a href="https://github.com/PHILTEC24/Library-system"><strong>🔗 GitHub Repository: https://github.com/PHILTEC24/Library-system</strong></a>
  <br><br>
  <img src="database/logo.png" alt="Library Management System logo" width="260">
  <h1>Library Management System</h1>
  <p><strong>LibraryMS — a complete, database-driven library operations system</strong></p>

  <a href="https://github.com/PHILTEC24/Library-system"><img alt="GitHub Repository" src="https://img.shields.io/badge/GitHub-Library--system-181717?logo=github"></a>
  <img alt="PHP" src="https://img.shields.io/badge/PHP-8.1%2B-777BB4?logo=php&logoColor=white">
  <img alt="MySQL" src="https://img.shields.io/badge/MySQL%2FMariaDB-4479A1?logo=mysql&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-green">
</div>

## Overview

**LibraryMS** is a web-based library management application built for a database tools course project. It gives authorised library staff a practical interface for managing books, authors, categories, sub-categories, members, loans and returns.

The application uses **PHP 8 + PDO** for secure server-side operations and **MySQL/MariaDB** for relational data storage. Its schema enforces third normal form, foreign keys, unique constraints and referential integrity. The interface is responsive and uses **Bootstrap 5**, Bootstrap Icons, custom CSS and JavaScript for confirmation prompts, live table search and alert dismissal.

### Core capabilities

- Secure login and role-aware staff sessions
- Dashboard with live library statistics and overdue alerts
- CRUD management for books, authors, categories and members
- Book cover images and staff-uploaded PDF e-books with in-browser viewing
- 14-day book issue workflow with availability and transaction checks
- Book return workflow with automatic overdue-day calculation
- Active-loan and overdue-loan tracking
- CSV exports for books, members and loans
- Responsive navigation and live client-side search
- PDO prepared statements and HTML output escaping

## Languages & technologies

| Area | Technology | Purpose |
|---|---|---|
| Backend | PHP 8.1+ | Authentication, validation, CRUD and transactions |
| Database | MySQL 8+ / MariaDB 10.4+ | Schema, constraints and seeded data |
| Database access | PDO | Prepared statements and safe parameter binding |
| Markup | HTML5 | Page structure and forms |
| Styling | CSS3, Bootstrap 5 | Responsive layout and components |
| Interaction | JavaScript, Bootstrap Icons | Live search, confirmations and alerts |
| Reporting | SQL, CSV | Analytical queries and downloadable exports |
| Diagramming | Mermaid | User-flow documentation |
| Local platform | XAMPP / Apache | Development and deployment environment |
| Source control | Git & GitHub | Collaboration and versioning |

## Interactive features

<details>
<summary><strong>Try the live-search experience</strong></summary>

Every searchable table has an automatic **Search** box. Enter a title, member name, ISBN or another visible value and matching rows are filtered instantly in the browser.

</details>

<details>
<summary><strong>Test transaction safeguards</strong></summary>

The issue and return workflows use database transactions. An unavailable book or duplicate active loan prevents the operation, and stock/count changes are committed only when the complete transaction succeeds.

</details>

<details>
<summary><strong>Export a report</strong></summary>

Open **Books**, **Members** or **Loans** and select **Export CSV**. The application generates a downloadable spreadsheet that can be opened in Excel or LibreOffice.

</details>

## How the system works

```mermaid
flowchart TD
    A[Open LibraryMS] --> B[Staff login]
    B --> C{Valid credentials?}
    C -->|No| D[Show login error]
    D --> B
    C -->|Yes| E[Dashboard]

    E --> F{Choose operation}
    F -->|Browse/manage| G[Books, Authors, Categories or Members]
    G --> H[Create, edit or delete record]
    H --> I[PDO validation & database operation]

    F -->|Issue a book| J[Select active member and available book]
    J --> K[Check stock and duplicate active loan]
    K -->|Invalid| L[Return friendly error]
    K -->|Valid| M[Start transaction]
    M --> N[Create 14-day loan]
    N --> O[Decrement available copies]
    O --> P[Commit transaction]

    F -->|Return a book| Q[Select active loan]
    Q --> R[Set returned date]
    R --> S[Increment available copies]
    S --> T[Calculate overdue fine if applicable]

    F -->|Report| U[View dashboard / run SQL / export CSV]

    I --> E
    P --> E
    T --> E
    U --> E
```

## Screenshots

### Application Overview

| Dashboard | Books Catalogue | Loans Circulation |
|---|---|---|
| ![Dashboard](docs/screenshots/01_dashboard.png) | ![Books](docs/screenshots/02_books_list.png) | ![Loans](docs/screenshots/03_loans_list.png) |

| Issue a Book | Business Rules Safeguard |
|---|---|
| ![Issue a book](docs/screenshots/04_issue_book.png) | ![Business rules](docs/screenshots/05_business_rules.png) |

### CRUD Operations & Business Logic

| Entity / Domain | Create | Read / List | Update | Delete / Safeguard |
|---|---|---|---|---|
| **Books** | [![Books: Create](docs/screenshots/crud/01_books_create.png)](docs/screenshots/crud/01_books_create.png) | [![Books: Read](docs/screenshots/crud/02_books_read.png)](docs/screenshots/crud/02_books_read.png) | [![Books: Update](docs/screenshots/crud/03_books_update.png)](docs/screenshots/crud/03_books_update.png) | [![Books: Delete](docs/screenshots/crud/04_books_delete.png)](docs/screenshots/crud/04_books_delete.png) |
| **Members** | [![Members: Create](docs/screenshots/crud/05_members_create.png)](docs/screenshots/crud/05_members_create.png) | [![Members: Read](docs/screenshots/crud/06_members_read.png)](docs/screenshots/crud/06_members_read.png) | [![Members: Update](docs/screenshots/crud/07_members_update.png)](docs/screenshots/crud/07_members_update.png) | [![Members: Delete](docs/screenshots/crud/08_members_delete.png)](docs/screenshots/crud/08_members_delete.png) |
| **Loans** | [![Loans: Create](docs/screenshots/crud/09_loans_create.png)](docs/screenshots/crud/09_loans_create.png) | [![Loans: Read](docs/screenshots/crud/10_loans_read.png)](docs/screenshots/crud/10_loans_read.png) | [![Loans: Update](docs/screenshots/crud/11_loans_update.png)](docs/screenshots/crud/11_loans_update.png) | [![Delete Refused (Rule 6)](docs/screenshots/crud/12_delete_refused.png)](docs/screenshots/crud/12_delete_refused.png) |

| Authors: Create & Read | Categories: Create & Read |
|---|---|
| [![Authors: Create and Read](docs/screenshots/crud/13_authors_create_and_read.png)](docs/screenshots/crud/13_authors_create_and_read.png) | [![Categories: Create and Read](docs/screenshots/crud/14_categories_create_and_read.png)](docs/screenshots/crud/14_categories_create_and_read.png) |

## Project structure

Your project folder sits inside XAMPP's `htdocs` directory (e.g. `C:\xampp\htdocs\library-system`) and is strictly organized according to the course specification:

```text
library-system/
├── index.php                 redirects to login or dashboard
├── README.md                 how to install and run the project
├── config/
│   └── database.php          the one and only database connection
├── database/
│   ├── library_db.sql        creates tables and inserts sample data
│   ├── queries.sql           your JOIN and aggregate queries
│   └── erd.png               your ERD diagram
├── includes/
│   ├── header.php
│   ├── navbar.php
│   ├── footer.php
│   ├── auth_check.php        blocks any page when not logged in
│   └── functions.php         shared helpers (validation, messages)
├── auth/
│   ├── login.php
│   └── logout.php
├── dashboard/
│   └── index.php             summary after login
├── books/
│   ├── index.php             list, search, filter
│   ├── create.php
│   ├── edit.php
│   └── delete.php
├── members/
│   ├── index.php
│   ├── create.php
│   ├── edit.php
│   └── delete.php
├── loans/
│   ├── index.php
│   ├── issue.php
│   └── return.php
├── authors/                  minimum: list and add
├── categories/               minimum: list and add
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── docs/
    ├── report.pdf
    └── screenshots/
```

### Rules for the structure

- **One folder per entity:** Do not mix book pages and member pages in one folder.
- **Shared page parts:** (header, navigation, footer, login check) live only in `includes/`. Do not copy and paste them into every page.
- **Single database connection:** The database connection is written once in `config/database.php` and reused with `require_once`.
- **Clean root:** No file may sit loose in the root except `index.php` and `README.md`.
- **Consistent naming:** Use lowercase names with no spaces, and the same naming pattern everywhere.

## Installation

### Requirements

- XAMPP or another Apache/PHP/MySQL environment
- PHP 8.1 or newer
- MySQL 8.0+ or MariaDB 10.4+
- A modern web browser

### 1. Install XAMPP

Download XAMPP from <https://www.apachefriends.org>, install it and start **Apache** and **MySQL** from the XAMPP Control Panel.

### 2. Place the project

Clone or download the repository into the Apache web root:

```powershell
cd C:\xampp\htdocs
git clone https://github.com/PHILTEC24/Library-system.git library-system
```

The application entry point should be:

```text
C:\xampp\htdocs\library-system\index.php
```

If cloned under another folder name, update `BASE_URL` in PHP entry files or use `library-system` as shown below.

### 3. Import the database

Open <http://localhost/phpmyadmin>, select **Import**, choose:

```text
C:\xampp\htdocs\library-system\database\library_db.sql
```

and click **Import**. The SQL script creates `library_db`, tables, relationships, constraints and sample records.

For an existing database, run `database/migrations/20261120_add_book_media.sql` once in phpMyAdmin instead of re-importing the full SQL file. Re-importing `library_db.sql` drops and recreates the database, replacing its data.

### 4. Configure the connection

Check [config/database.php](config/database.php). The default XAMPP credentials are:

```php
$host = 'localhost';
$db   = 'library_db';
$user = 'root';
$pass = '';
```

Update these values only if your MySQL root account or server differs.

### 5. Start LibraryMS

Visit <http://localhost/library-system>. Use one of the seeded accounts:

| Username | Password | Role |
|---|---|---|
| `admin` | `password` | Administrator |
| `librarian` | `password` | Librarian |

> Change or remove demo credentials before using the application in production.

### Upload covers and digital books

From **Books → Add book** or **Edit book**, optionally attach a JPEG/PNG/WebP cover image (up to 5 MB) and a PDF digital copy (up to 25 MB). Covers appear in the catalogue. Staff can open PDFs in the browser or download them. Uploaded media is private to authenticated users; only upload digital books that the library is authorised to distribute.

If uploads are rejected due to PHP limits, update `upload_max_filesize` to at least `25M` and `post_max_size` to at least `32M` in `php.ini`, then restart Apache. The application stores files under `uploads/books/`; retain this directory and its contents when backing up or moving the database.

## Database design

<p align="center">
  <img src="database/erd.png" alt="LibraryMS entity relationship diagram" width="850">
</p>

The database separates authors, categories and sub-categories from books, while a `book_authors` table supports primary authors, co-authors, editors and translators. Members and staff users create loan records for individual books. `ON DELETE` constraints and application checks protect important historical and inventory relationships.

## Business rules

- Members must be active before borrowing.
- A member cannot have two active loans for the same book.
- A book cannot be issued when `available_copies` is zero.
- Loans receive an automatic 14-day due date.
- Issue and return operations use database transactions.
- Overdue returns calculate a fine of $0.50 per overdue day.
- Records linked to active loans or other records are protected from unsafe deletion.

## Useful SQL

Additional reporting queries are available in [database/queries.sql](database/queries.sql), including:

- Currently borrowed books
- Overdue loans and days overdue
- Loans per category
- Available copies against borrowed copies
- Members with the most loans
- Books that have never been borrowed

## Team & attribution

**Project lead:** **EGABO AARON**

The supplied team register contains the following twelve names and registration numbers:

| # | Member | Registration number |
|---:|---|---:|
| 1 | EGABO AARON — **Group Lead** | 258-154 |
| 2 | ALIMPA ANNE HILLARY | 269-896 |
| 3 | KABAJUNGU RITAH | 267-640 |
| 4 | KIRABO ALICE | 274-961 |
| 5 | MUAWIA MOHAMED IBRAHIM ISHAG | 229-449 |
| 6 | NATOZO PATIENCE MARTHA| 258-901 |
| 7 | NIWASIIMA ASHELYCOLE | 275-353 |
| 8 | ONYANGO JOHN STEVEN | 270-472 |
| 9| RWOTHOMIO EVANS . E. | 275-372 |
| 10 | TUSABEGE PHILBERT | 272-210 |

## Security

- PDO prepared statements prevent SQL injection
- Passwords are stored with PHP `password_hash()` and checked with `password_verify()`
- Output is escaped with `htmlspecialchars()` through the shared `e()` helper
- Protected pages check the staff session
- Successful login regenerates the PHP session ID
- Database availability and duplicate-loan rules are checked again during transactions

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for the full text.

Copyright (c) 2026 EGABO AARON and contributors.
