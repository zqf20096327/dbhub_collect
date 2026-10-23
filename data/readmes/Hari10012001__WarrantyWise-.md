# 🛡️ WarrantyWise — Product Warranty, Service History and Renewal Reminder Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7.svg?style=for-the-badge&logo=render)](https://warrantywise-tg3t.onrender.com)
[![Status](https://img.shields.io/badge/Status-200%20OK%20%7C%20Active-brightgreen.svg?style=for-the-badge)]()
[![Java](https://img.shields.io/badge/Java-21%20LTS-ED8B00.svg?style=for-the-badge&logo=openjdk&logoColor=white)]()
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.3.2-6DB33F.svg?style=for-the-badge&logo=springboot&logoColor=white)]()
[![Security](https://img.shields.io/badge/Security-Spring%20Security%206%20%7C%20JWT-red.svg?style=for-the-badge&logo=jsonwebtokens&logoColor=white)]()
[![Database](https://img.shields.io/badge/Database-MySQL%208.x%20%7C%20TiDB%20Cloud-00758F.svg?style=for-the-badge&logo=mysql&logoColor=white)]()
[![Frontend](https://img.shields.io/badge/UI-Glassmorphism%20%7C%20Bootstrap%205.3.3-7952B3.svg?style=for-the-badge&logo=bootstrap&logoColor=white)]()

> **A modern, full-stack personal asset management platform designed to eliminate missed warranty expirations, digitize purchase receipts, track post-purchase service histories, and deliver intelligent renewal reminders.**

---

## 🌐 Live Production Deployment

| Service | Endpoint / Link | Description |
|---|---|---|
| **Live Web Application** | 🔗 **[https://warrantywise-tg3t.onrender.com](https://warrantywise-tg3t.onrender.com)** | Deployed on Render Cloud via Docker |
| **Health Check API** | 🩺 **[`/api/v1/health`](https://warrantywise-tg3t.onrender.com/api/v1/health)** | Public readiness probe (`status: UP`, HTTP 200) |
| **Cloud Database** | ☁️ **TiDB Cloud Serverless** | High-availability MySQL 8 compatible cluster |
| **Uptime Monitoring** | ⏱️ **UptimeRobot / BetterStack** | Target URL: `https://warrantywise-tg3t.onrender.com/api/v1/health` |

> ℹ️ **Cold Start Note (Render Free Tier):** After 15 minutes of inactivity, Render puts the free container to sleep. The first request takes ~15–30 seconds for the container and Spring Boot to initialize. Subsequent requests are instant. UptimeRobot checks (every 5–10 mins on `/api/v1/health`) help keep the service warm and responsive.

---

## 📖 Quick Links & Guides

- 📘 **[GUIDE_TANGLISH.md](GUIDE_TANGLISH.md)** — Comprehensive ELI5 Tanglish Guide for easy understanding & viva presentation.
- 📄 **[Project_Documentation.docx](Project_Abstract_Literature_Existing_Proposed_Software_Hardware_Requirements.docx)** — Complete academic project report (Abstract, Literature Survey, Existing vs Proposed System, Software & Hardware Requirements).

---

## 🎯 Problem Statement & Solution

In modern households and workplaces, individuals own dozens of electronic devices, home appliances, gadgets, and vehicles. However, managing these assets using physical paper bills and warranty cards results in:
- ❌ **Faded Paper Receipts:** Thermal receipts fade within months, making warranty claims impossible.
- ❌ **Missed Expirations:** Users forget warranty expiration dates and miss out on free repairs or renewal opportunities.
- ❌ **Unrecorded Repairs:** No historical tracking of repair expenses, parts replaced, or service center visits.
- ❌ **Fragmented Storage:** Documents scattered across folders, physical drawers, and disparate emails.

**WarrantyWise solves this by delivering:**
- ✅ **Centralized Digital Archival:** Store product metadata, serial numbers, models, and upload high-resolution invoices/receipts.
- ✅ **Automated Renewal Alerts:** Multi-tier proactive alerts (90, 30, 15, 7, 3, 1, and 0 days prior to expiry).
- ✅ **Warranty Health Intelligence:** Automated scoring engine calculating asset protection levels (0–100%).
- ✅ **Comprehensive Maintenance Logs:** Track repair costs, routine servicing, parts replaced, and warranty claim status.
- ✅ **Financial Analytics & 1-Click Exports:** View monthly spending trends and export clean CSV reports for auditing.

---

## ✨ Key Features

- **🔐 Stateless JWT Authentication:** Secure registration, login, BCrypt password hashing, and HMAC-SHA512 signed JWT access and refresh token pair.
- **📦 Comprehensive Product Inventory:** Catalog products by category (Electronics, Home Appliances, Vehicles, etc.), brand, serial number, IMEI, purchase date, and vendor.
- **🛡️ Warranty Lifecycle Management:** Track manufacturer, extended, and seller warranties with dynamic status indicators (`ACTIVE`, `EXPIRING_SOON`, `EXPIRED`).
- **🧠 Warranty Health Index:** Intelligent algorithm evaluating user inventory to determine overall asset coverage and vulnerability.
- **🔧 Service & Repair History:** Record maintenance dates, technician contacts, work descriptions, and expenditures with warranty linkage.
- **📈 Service Expense Analytics:** Monthly spending breakdown, total cost of ownership (TCO), and high-maintenance asset identification.
- **⏰ Multi-Interval Expiration Reminders:** Background evaluation of expiring policies with user-friendly alert badges and snoozing.
- **📎 Invoice & Receipt Attachments:** Multipart file upload for digital bills and warranty cards (PDF, PNG, JPG).
- **📊 1-Click CSV Reporting:** Instant export for products, active warranties, service expenditures, and lifecycle history.
- **🎨 Glassmorphism Responsive UI:** Modern translucent frosted-glass aesthetic built with Bootstrap 5.3.3 and native dark/light theme switching.
- **⚡ Zero Framework Friction:** Pure Vanilla JavaScript frontend communicating asynchronously with Spring Boot REST APIs via `fetch()`.

---

## 🛠️ Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Backend** | Java | 21 LTS | Core programming language |
| **Framework** | Spring Boot | 3.3.2 | Enterprise REST API and web application engine |
| **Security** | Spring Security & JJWT | 6.x / 0.12.6 | Stateless JWT authentication (HMAC-SHA512) & BCrypt |
| **Data & ORM** | Spring Data JPA / Hibernate | 6.x | Relational persistence, transactional services |
| **Database** | MySQL / TiDB Cloud | 8.x | Production & local relational database storage |
| **Connection Pool**| HikariCP | 5.x | High-performance DB connection pooling with keepalive |
| **Frontend** | HTML5 / CSS3 / Vanilla JS | ES6+ | Responsive Single-Page UI with native async API client |
| **Styling** | Bootstrap / Glassmorphism | 5.3.3 | Frosted-glass design system with Bootstrap Icons 1.11.3 |
| **Build Tool** | Apache Maven | 3.9+ | Dependency management, build lifecycle, packaging |
| **Deployment** | Docker & Render | Multi-stage | Alpine JRE 21 container deployed to Render Web Service |

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- **JDK 21** installed and configured on your `PATH`.
- **MySQL Server 8.x** running locally (or access to a cloud MySQL/TiDB instance).
- **Apache Maven 3.9+** (optional if using IDE).

### 1. Database Setup
Log into your MySQL CLI or Workbench and create the database:
```sql
CREATE DATABASE warrantywise_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Configure Environment Variables (Optional)
By default, the application falls back to `localhost:3306` with default credentials. You can customize them via environment variables:

**Windows (PowerShell):**
```powershell
$env:DB_URL = "jdbc:mysql://localhost:3306/warrantywise_db?createDatabaseIfNotExist=true&useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true"
$env:DB_USER = "root"
$env:DB_PASSWORD = "your_mysql_password"
$env:PORT = "8080"
```

**Linux / macOS (Bash):**
```bash
export DB_URL="jdbc:mysql://localhost:3306/warrantywise_db?createDatabaseIfNotExist=true&useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true"
export DB_USER="root"
export DB_PASSWORD="your_mysql_password"
export PORT="8080"
```

### 3. One-Click Launchers (Windows)
- **Start Application:** Double-click **`start.bat`** in the project root.
  - Automatically verifies Java & Maven.
  - Launches Spring Boot server on port `8080`.
  - Automatically opens default browser to `http://localhost:8080/pages/login.html`.
- **Stop Application:** Double-click **`stop.bat`** to gracefully terminate the background process on port `8080`.

### 4. Running via Terminal
```bash
# Build and package
mvn clean package -DskipTests

# Run Spring Boot
mvn spring-boot:run
```
Once started, visit: `http://localhost:8080`

---

## ☁️ Cloud Deployment (Render + Docker)

WarrantyWise includes a production-grade multi-stage `Dockerfile` and `render.yaml` configuration:

```dockerfile
# Build stage
FROM maven:3.9.6-eclipse-temurin-21-alpine AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Run stage
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Render Web Service Settings:
- **Build Command:** Built automatically via `Dockerfile`
- **Health Check Path:** `/api/v1/health`
- **Environment Variables:**
  - `PORT`: `8080`
  - `DB_URL`: `jdbc:mysql://<host>:<port>/<db>?useSSL=true&serverTimezone=UTC&allowPublicKeyRetrieval=true`
  - `DB_USER`: `<cloud_db_username>`
  - `DB_PASSWORD`: `<cloud_db_password>`
  - `JWT_SECRET`: `<minimum-512-bit-secure-random-secret>`

---

## 📋 Presentation & Viva Demo Data

When demonstrating the project during practical exams, reviews, or college vivas, use the following sample data to showcase all lifecycle states (`Active`, `Expiring Soon`, `Expired`):

### 📦 1. Products (Add These First)
| Product Name | Category | Purchase Price | Purchase Date | Notes / State |
| :--- | :--- | :--- | :--- | :--- |
| `MacBook Pro M3` | Electronics | `₹1,50,000` | `15-Sep-2025` | Needs Attention / Expiring Soon |
| `Samsung Galaxy S24 Ultra` | Electronics | `₹1,29,999` | `15-May-2024` | Expired / Out of Coverage |
| `LG 8kg Front Load Washing Machine` | Home Appliances | `₹35,000` | `10-Jan-2026` | Active / Safe |
| `Royal Enfield Classic 350` | Vehicles | `₹2,40,000` | `05-Mar-2026` | Active / Long Term |
| `Sony WH-1000XM5 Headphones` | Electronics | `₹29,990` | `01-Aug-2026` | Active (Zero Service History) |

### 🛡️ 2. Warranties (Link to Products Above)
| Select Product | Warranty Provider | Start Date | End Date | Status |
| :--- | :--- | :--- | :--- | :--- |
| MacBook Pro M3 | `Apple Care+` | `15-Sep-2025` | `15-Sep-2026` | `ACTIVE` |
| Samsung Galaxy S24 Ultra | `Samsung India Electronics` | `15-May-2024` | `15-May-2025` | `EXPIRED` |
| LG 8kg Front Load Washing Machine | `LG Extended Care` | `10-Jan-2026` | `10-Jan-2029` | `ACTIVE` |
| Royal Enfield Classic 350 | `RE Sure` | `05-Mar-2026` | `05-Mar-2030` | `ACTIVE` |
| Sony WH-1000XM5 Headphones | `Sony India Guarantee` | `01-Aug-2026` | `01-Aug-2027` | `ACTIVE` |

### 🔧 3. Service Records (Link to Products Above)
| Select Product | Service Name / Issue | Service Type | Cost | Status | Notes / Work Performed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| MacBook Pro M3 | `Keyboard Replaced` | Repair | `₹0` | COMPLETED | Covered 100% under warranty |
| Samsung Galaxy S24 Ultra | `Screen Replacement` | Repair | `₹15,000` | COMPLETED | Out of warranty; display replaced |
| LG 8kg Front Load Washing Machine | `Routine Drum Cleaning` | Maintenance | `₹500` | COMPLETED | Preventive maintenance |
| Royal Enfield Classic 350 | `First Free Service` | Maintenance | `₹800` | COMPLETED | Engine oil & filter change |
| *(Keep Sony Headphones empty)* | — | — | — | — | *Shows graceful empty state on UI* |

---

## 📁 Project Architecture & Folder Structure

```text
WarrantyWise/
├── Dockerfile                   # Multi-stage production container build
├── render.yaml                  # Render cloud infrastructure blueprint
├── pom.xml                      # Maven project configuration & dependencies
├── start.bat                    # 1-Click launcher script (Windows)
├── stop.bat                     # 1-Click graceful shutdown script (Windows)
├── README.md                    # Project documentation (this file)
├── GUIDE_TANGLISH.md            # ELI5 Tanglish Viva guide
├── src/
│   ├── main/
│   │   ├── java/com/warrantywise/
│   │   │   ├── WarrantyWiseApplication.java   # Spring Boot entry point
│   │   │   ├── config/                        # SecurityConfig, JpaAuditingConfig
│   │   │   ├── controller/                    # REST Controllers (/api/v1/*)
│   │   │   │   ├── AuthController.java        # Authentication & Profile API
│   │   │   │   ├── HealthController.java      # Public /api/v1/health Probe
│   │   │   │   ├── ProductController.java     # Product CRUD & Search
│   │   │   │   ├── WarrantyController.java    # Warranty Policies & Status
│   │   │   │   ├── ServiceRecordController.java # Maintenance & Repair Logs
│   │   │   │   ├── CategoryController.java    # Product Categories API
│   │   │   │   ├── DashboardController.java   # KPI Aggregations & Counts
│   │   │   │   ├── ReportController.java      # CSV Report Generation
│   │   │   │   └── ...
│   │   │   ├── dto/                           # Request & Response DTOs
│   │   │   ├── entity/                        # JPA Database Entities
│   │   │   ├── repository/                    # Spring Data JPA Repositories
│   │   │   ├── security/                      # JWT Filter, CustomUserDetailsService
│   │   │   └── service/                       # Business Logic & Analytics Engines
│   │   └── resources/
│   │       ├── application.properties         # Main app & cloud datasource config
│   │       └── static/                        # Web Frontend (Vanilla JS + Bootstrap)
│   │           ├── index.html                 # App entrypoint & auth redirector
│   │           ├── css/                       # Glassmorphism design system
│   │           ├── js/                        # API client, auth util, page engines
│   │           └── pages/                     # Dashboard, Products, Warranties, etc.
│   └── test/                                  # Unit & MockMvc integration tests
└── uploads/                                   # User uploaded invoice documents
```

---

## 🔌 Core REST API Endpoints

| Category | Method | Endpoint | Authentication | Description |
|---|---|---|---|---|
| **Health** | `GET` | `/api/v1/health` | **Public** | Lightweight health check for Render & Uptime monitors |
| **Auth** | `POST` | `/api/v1/auth/register` | **Public** | Register new user account |
| **Auth** | `POST` | `/api/v1/auth/login` | **Public** | Authenticate user & return JWT tokens |
| **Auth** | `POST` | `/api/v1/auth/refresh` | **Public** | Refresh expired access token |
| **Categories** | `GET` | `/api/v1/categories` | **Public** | Fetch all product categories |
| **Products** | `GET` | `/api/v1/products` | Required | List user's products (paginated) |
| **Products** | `POST` | `/api/v1/products` | Required | Register a new product |
| **Warranties** | `GET` | `/api/v1/warranties` | Required | Retrieve warranty coverage list |
| **Warranties** | `POST` | `/api/v1/warranties` | Required | Add new warranty policy |
| **Intelligence**| `GET` | `/api/v1/warranties/intelligence/health` | Required | Compute Warranty Health Score |
| **Services** | `GET` | `/api/v1/services` | Required | Retrieve maintenance & repair history |
| **Dashboard** | `GET` | `/api/v1/dashboard` | Required | Fetch summary counts and upcoming alerts |
| **Reports** | `GET` | `/api/v1/reports/export/csv` | Required | Download CSV export of inventory/records |

---

## 🔒 Security Architecture

1. **Stateless JWT Authorization:** Client requests pass bearer tokens in the `Authorization: Bearer <token>` HTTP header.
2. **Cryptographic Signing:** Signed using HMAC-SHA512 with a 512-bit key to prevent token tampering.
3. **Password Security:** All user passwords are encrypted using salted **BCrypt** hashing before database persistence.
4. **Tenant Isolation:** Every data query enforces strict ownership filters (`where user_id = :currentUser`) to prevent horizontal privilege escalation.

---

## 👨‍💻 Author & Repository

- **Developer:** Hariharan P
- **GitHub Repository:** [https://github.com/Hari10012001/WarrantyWise-](https://github.com/Hari10012001/WarrantyWise-)
- **Live Cloud Deployment:** [https://warrantywise-tg3t.onrender.com](https://warrantywise-tg3t.onrender.com)
