# ServeEase

ServeEase is a Java web application for booking home services (cleaning, plumbing, electrical, AC repair, etc.) with separate user and admin modules.  
This project appears to be developed as an Eclipse Dynamic Web Project using JSP/Servlets and MySQL.

## Project Type

- BCA Final Year Project
- Domain: Home Service Booking Platform
- Architecture: JSP + Servlets + DAO + MySQL

## Submitted By

For Shivaji University, Kolhapur

| Sr. No. | Project Member |
|---|---|
| 1 | Mr. Avishkar Tanaji Deshmukh |
| 2 | Mr. Rushikesh Rajaram Mahadik |
| 3 | Mr. Bhavesh Vishwas Shinde |

## Academic Details

- College: **SOU. SHOBHAKAKI BABAR KANYA MAHAVIDYALAYA, VITA** (B.C.A College)
- Course: **Bachelor of Computer Application**
- Semester: **Semester VI**
- Academic Year: **2025 - 2026**

## Core Features

### User Module

- User registration and login
- Browse categories and services
- View service details and providers
- Book services
- View booking history and booking details
- Payment flow pages (gateway, processing, success)
- Submit reviews
- Contact support
- Profile management and password change

### Admin Module

- Admin login/logout
- Dashboard metrics and recent activity
- Manage users
- Manage categories
- Manage services
- Manage providers
- Manage schedules
- Manage bookings
- Manage reviews
- Reports and CSV export

## Tech Stack

- Java 21
- Jakarta Servlet/JSP (Web facet 6.0)
- Apache Tomcat 10.1
- MySQL (schema and demo SQL included)
- JDBC (`mysql-connector-j-9.3.0.jar`)
- Frontend: JSP, HTML, CSS, JavaScript

## Project Structure

```text
ServeEase/
+-- src/main/java/com/serveease/controller/
|   +-- admin/         # Admin servlets
|   +-- user/          # User servlets
|   +-- dao/admin/     # Admin DAOs
|   +-- dao/user/      # User DAOs
|   +-- model/         # Entity/model classes
|   +-- util/          # DB/password utilities
+-- src/main/webapp/
|   +-- admin/         # Admin JSP pages
|   +-- user/          # User JSP pages
|   +-- assets/css/    # Styles
|   +-- WEB-INF/       # web.xml + libs
+-- database/
|   +-- serveease.sql  # Full schema + baseline data
|   +-- demo_data.sql  # Extra demo records
+-- build/classes/     # Compiled classes
```

## Database Setup

1. Create database:

```sql
CREATE DATABASE serveease;
```

2. Import base schema:

- `database/serveease.sql`

3. (Optional) Import extended sample data:

- `database/demo_data.sql`

## Application Configuration

Database settings are in:

- `src/main/java/com/serveease/controller/util/DBConnection.java`

Default values currently:

- Host: `localhost`
- Port: `3306`
- DB: `serveease`
- User: `root`
- Password: *(empty)*

Update these values based on your local MySQL setup.

## How To Run (Eclipse + Tomcat)

1. Open Eclipse IDE (Enterprise Java / Web).
2. Import existing project from:
   - `C:\Users\Perfect\eclipse-workspace\ServeEase`
3. Configure server runtime:
   - Apache Tomcat v10.1
4. Add project to Tomcat server.
5. Start Tomcat.
6. Open in browser:
   - `http://localhost:8080/ServeEase/user/index.jsp`

## Important URLs

- User home: `/ServeEase/user/index.jsp`
- User login: `/ServeEase/user/login.jsp`
- User register: `/ServeEase/user/register.jsp`
- Admin login: `/ServeEase/admin/login.jsp`
- Admin dashboard: `/ServeEase/admin/dashboard.jsp`

## Demo Credentials (from SQL)

- Admin:
  - Username: `admin`
  - Password: `admin123`
- User:
  - Email: `r@gmail.com`
  - Password: *(hashed in DB; create a fresh user via Register page for login testing)*

## Project Analysis

### Strengths

- Good modular separation (`controller`, `dao`, `model`, `util`)
- Clear user/admin feature split
- Relational database design with keys and constraints
- Includes demo data and report export
- Uses password hashing utility for user passwords

### Current Gaps / Risks

- `ExportReportServlet` uses `javax.servlet.*` imports while project is configured for Jakarta/Tomcat 10 (`jakarta.servlet.*`).
- Some report SQL in export servlet references columns like `booking_time` and `location`, while current schema mainly uses `booking_date` and `address`.
- Admin credential in SQL is plain text (`admin123`), not hashed.
- DB credentials are hardcoded in source.
- No build tool (`pom.xml`/`build.gradle`) or automated test suite present.

### Suggested Improvements

1. Standardize all servlets to `jakarta.servlet.*`.
2. Align report queries with latest schema.
3. Hash admin passwords similarly to user passwords.
4. Move DB config to environment variables or a properties file.
5. Add Maven/Gradle for reproducible builds.
6. Add unit/integration tests for DAO and servlet flows.
7. Add role-based filters/interceptors for stronger access control.

## Notes

- The project already includes compiled classes under `build/classes`.
- For clean evaluation/demo, use a fresh database import before presentation.

---

