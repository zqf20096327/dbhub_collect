# Karthikraj S - Personal Portfolio Website

A full-stack, responsive personal portfolio web application built with **Flask**, **SQLAlchemy**, **PyMySQL / SQLite**, and **Vanilla HTML5/CSS3/JavaScript**. Designed to showcase projects, skills, education, and credentials, featuring an interactive, rate-limited contact form and a dynamic DEV MODE fallback.

---

## 1. Project Overview

This application serves as Week 1's internship submission for **Karthikraj S**, an undergraduate Computer Science student at Rajalakshmi Institute of Technology, Chennai, aspiring to become an AI Engineer.

The project strictly follows honesty guidelines:
- Real academic details only (no fabricated experience, awards, scores, or fake certificate links).
- Projects clearly marked with development status ("Planned / In Progress") and empty demo/repo links hidden.
- Dynamic resume availability check: disables download button with "Resume coming soon" when no physical PDF is uploaded.
- Clean separation of concerns: modular Flask backend, RESTful API endpoints, and zero-framework frontend.

---

## 2. Features

- **Dynamic Data Ingestion**: Projects, skills, and certifications are dynamically fetched via RESTful endpoints (`/api/*`) on page load.
- **DEV MODE (Zero-Config SQLite Fallback)**: Automatically switches to a local SQLite database (`portfolio_dev.db`) if no MySQL connection string is set in environment variables.
- **Production MySQL Ready**: Configured for MySQL 8.0+ / TiDB Cloud Starter via Flask-SQLAlchemy and PyMySQL with full UTF-8 Unicode support.
- **Idempotent Database Seeder**: `seed.py` loads `data/portfolio_data.json` into the database without creating duplicate entries when executed repeatedly.
- **Spam-Protected Contact Form**:
  - Hidden honeypot field (`website_url`) to catch automated bots.
  - Rate limiting (5 messages/hour per IP via Flask-Limiter).
  - Backend and frontend regex validation and length checking.
  - Safe UI text injection using `textContent` to prevent Cross-Site Scripting (XSS).
- **Responsive & Accessible Design**:
  - Fully responsive from mobile devices (360px) to desktops.
  - WCAG AA color contrast, visible `:focus-visible` outlines, skip-to-content link, and semantic HTML5.
  - Respects `prefers-reduced-motion` accessibility preferences.
- **Dark / Light Theme Toggle**: Seamless theme switching with state persistence in `localStorage`.
- **Automated Test Suite**: 10 automated unit & integration tests using `pytest` covering health, catalogs, honeypot detection, rate limits, and persistence.

---

## 3. Technology Stack

- **Frontend**: HTML5, CSS3 (Modern Flexbox/Grid, CSS Custom Properties), Vanilla JavaScript (ES6+ Fetch API). No external frontend frameworks or heavy dependencies.
- **Backend**: Python 3.11+ / 3.13, Flask 3.1+, Flask-SQLAlchemy 3.1+, Flask-Limiter 4.1+, python-dotenv.
- **Production Server**: Gunicorn WSGI server.
- **Database**:
  - Development: SQLite (auto-created `portfolio_dev.db`).
  - Production / Local MySQL: MySQL 8.0+ or MySQL-compatible cloud database (TiDB Cloud Starter) via PyMySQL.
- **Testing**: Pytest 9.2+.
- **Version Control & Tooling**: Git, GitHub, VS Code on Windows 11.

---

## 4. Folder Structure

```text
portfolio/
├── app.py                     # Flask application factory and server entry point
├── config.py                  # Environment config and automatic SQLite/MySQL mode detection
├── extensions.py              # Shared Flask extensions (Flask-Limiter)
├── requirements.txt           # Python package dependencies
├── .env.example               # Template for environment configuration
├── .gitignore                 # Files excluded from Git tracking
├── schema.sql                 # MySQL table definitions (DDL)
├── seed.py                    # Idempotent database seeder (reads portfolio_data.json)
├── render.yaml                # Render Blueprint deployment specification
├── Procfile                   # Gunicorn process definition for cloud hosts
├── README.md                  # Comprehensive project documentation
├── TESTING_CHECKLIST.md       # Real execution checklist and verification results
├── database/
│   ├── db.py                  # SQLAlchemy instance initialization
│   └── models.py              # Data models (Project, Skill, Certification, ContactMessage)
├── routes/
│   └── api.py                 # REST API endpoints (/api/health, /api/projects, etc.)
├── data/
│   └── portfolio_data.json    # Source data for projects, skills, and certifications
├── templates/
│   └── index.html             # Accessible single-page application layout
├── static/
│   ├── css/
│   │   └── style.css          # Theme-aware, responsive CSS stylesheet
│   ├── js/
│   │   └── script.js          # Dynamic DOM rendering and client validation
│   ├── images/                # Static visual assets
│   └── resume/                # Directory for Karthikraj_S_Resume.pdf
└── tests/
    └── test_app.py            # Pytest automated test suite
```

---

## 5. Prerequisites

Before installing, ensure the following are installed on your Windows 11 machine:
- **Python 3.11 or later** (`python --version`)
- **Git** (`git --version`)
- *(Optional for MySQL mode)* **MySQL Server 8.0+** or an account on **TiDB Cloud Starter** (Free tier)

---

## 6. Installation (Windows 11 PowerShell)

1. Open PowerShell and navigate to the project directory:
   ```powershell
   cd c:\Users\karth\Desktop\portfolio
   ```

2. Create a Python virtual environment:
   ```powershell
   python -m venv .venv
   ```

3. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   *(If PowerShell shows execution policy restrictions, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

4. Upgrade pip and install all required dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Copy the sample environment file:
   ```powershell
   Copy-Item .env.example .env
   ```

---

## 7. MySQL Setup

### Option A: Use Local MySQL 8.0 Server
1. Log in to your local MySQL server using MySQL Command Line Client or PowerShell:
   ```powershell
   mysql -u root -p
   ```
2. Create the portfolio database:
   ```sql
   CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   EXIT;
   ```
3. Import the database schema:
   ```powershell
   mysql -u root -p portfolio_db < schema.sql
   ```
4. Update `DATABASE_URL` in your `.env` file:
   ```env
   DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/portfolio_db
   ```
5. Run the seeder to populate the MySQL tables:
   ```powershell
   python seed.py
   ```

### Option B: Cloud MySQL (TiDB Cloud Starter - Free Tier)
TiDB Cloud provides a free, 100% MySQL-wire-compatible cloud database without requiring a credit card:
1. Create a free account at [https://tidbcloud.com](https://tidbcloud.com).
2. Create a free **Starter** cluster and obtain your connection string.
3. Update `.env`:
   ```env
   DATABASE_URL=mysql+pymysql://<user>:<password>@<host>:4000/portfolio_db?ssl_verify_cert=true
   ```
4. Run `python seed.py` to seed the database tables.

---

## 8. Environment Variables

Configure the following keys in your `.env` file:

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `SECRET_KEY` | Flask session & cryptographic signature secret | `karthikraj-portfolio-secret-key-2026` |
| `FLASK_ENV` | Application environment mode (`development` or `production`) | `development` |
| `DATABASE_URL` | SQLAlchemy connection URI. **Leave blank for DEV MODE (SQLite)** | `mysql+pymysql://root:password@localhost:3306/portfolio_db` |
| `PORT` | Optional local development port | `5000` |

---

## 9. Run Locally

### Running in DEV MODE (Local SQLite)
If `DATABASE_URL` is empty or commented out in `.env`, the app automatically launches in DEV MODE using SQLite:

1. Seed the local database:
   ```powershell
   python seed.py
   ```
   *Terminal Output:*
   ```text
   =================================================================
    [DEV MODE] DATABASE_URL is not set.
    Automatically using local SQLite: sqlite:///.../portfolio_dev.db
   =================================================================
   [SEED RESULTS]
   Skills:         10 added, 0 verified/updated
   Projects:       2 added, 0 verified/updated
   Certifications: 2 added, 0 verified/updated
   Database seeding completed successfully!
   ```

2. Start the Flask application:
   ```powershell
   python app.py
   ```

3. Open your web browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

### Running Tests
Execute the automated test suite with pytest:
```powershell
pytest -v
```

---

## 10. Screenshots

*(Screenshots can be placed in `static/images/` when taking screen captures of your live demo)*

| Section | Preview Placeholder |
| :--- | :--- |
| **Hero & Navigation** | `[Screenshot: Desktop Hero Section with Dark Theme]` |
| **Skills & Projects** | `[Screenshot: Project Cards with Planned Badges & Skills Plls]` |
| **Contact Form** | `[Screenshot: Responsive Contact Form with Success Feedback]` |
| **Mobile Layout** | `[Screenshot: Mobile 360px viewport with active navigation menu]` |

---

## 11. API Endpoints

All data is served through clean, RESTful JSON endpoints:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Returns backend health status and active database engine. |
| `GET` | `/api/projects` | Returns sorted array of projects. |
| `GET` | `/api/skills` | Returns categorized skill entries. |
| `GET` | `/api/certifications` | Returns earned certification records. |
| `GET` | `/api/resume-status` | Verifies whether physical resume PDF is stored on disk. |
| `POST` | `/api/contact` | Submits message to `contact_messages`. Protected by honeypot & rate limiter (5/hr). |

### Example Contact Request:
```http
POST /api/contact HTTP/1.1
Content-Type: application/json

{
  "name": "Jane Recruiter",
  "email": "jane@techcorp.com",
  "subject": "Internship Inquiry",
  "message": "Hello Karthikraj, we would like to invite you for an internship interview.",
  "website_url": ""
}
```

### Example Contact Response (201 Created):
```json
{
  "status": "success",
  "message": "Thank you, Karthikraj will get back to you shortly!"
}
```

---

## 12. Deployment (Render & Cloud MySQL)

The application is pre-configured for free-tier deployment on **Render** (using Gunicorn) with an external MySQL-compatible cloud database.

> **Honest Note on Free Cloud Tiers**: Free web services (like Render) sleep after 15 minutes of inactivity and take ~50 seconds to boot on cold starts. Furthermore, Render does not offer native free MySQL databases, so a free external provider (such as TiDB Cloud Starter) is recommended for production MySQL.

### Step-by-Step Deployment Guide:
1. **Push Code to GitHub**:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit of full-stack portfolio"
   git remote add origin https://github.com/karthikraj-tech/portfolio.git
   git branch -M main
   git push -u origin main
   ```

2. **Create Free Cloud Database (TiDB Cloud Starter)**:
   - Go to [tidbcloud.com](https://tidbcloud.com) and create a free Starter cluster.
   - Copy your standard MySQL connection URL (e.g. `mysql+pymysql://<user>:<pwd>@<host>:4000/portfolio_db?ssl_verify_cert=true`).

3. **Deploy on Render**:
   - Go to [render.com](https://render.com) and sign in.
   - Click **New +** -> **Web Service**.
   - Select your GitHub repository `karthikraj-tech/portfolio`.
   - Set the following options:
     - **Name**: `karthikraj-portfolio`
     - **Runtime**: `Python`
     - **Build Command**: `pip install -r requirements.txt && python seed.py`
     - **Start Command**: `gunicorn app:app`
     - **Plan**: Free
   - Add Environment Variables in Render Dashboard:
     - `DATABASE_URL`: *(Your TiDB Cloud connection string from Step 2)*
     - `SECRET_KEY`: *(Generate a secure random string)*
     - `FLASK_ENV`: `production`
   - Click **Deploy Web Service**.

4. **Verify Deployment**:
   - Visit the public Render URL (`https://karthikraj-portfolio.onrender.com`).
   - Test `/api/health` to confirm database connectivity.
   - Submit a test inquiry on the live contact form.

---

## 13. Known Limitations

- **Email Dispatching**: Contact form submissions are securely stored in the `contact_messages` database table, but direct SMTP notification (e.g. sending an email to `karthikpnk17@gmail.com` via SendGrid/Mailgun) is not yet configured.
- **Project Demonstrations**: Project repositories and live demo links are marked "Planned / In Progress" and hidden until projects are completed.
- **Resume File**: The download button remains disabled with "Resume coming soon" until a verified `Karthikraj_S_Resume.pdf` file is placed in `static/resume/`.

---

## 14. Future Improvements

- Add transactional email alerting (via SMTP / SendGrid) upon contact message submission.
- Implement an authenticated admin portal (`/admin`) to view and reply to received contact messages.
- Complete and deploy the "Student Attendance Management System" and "Nutrazs E-commerce Website" projects, adding active links and screenshots.
- Implement automated CI/CD pipeline using GitHub Actions to run pytest on push.
