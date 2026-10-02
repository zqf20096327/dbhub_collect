# CodePath Academy – Interactive Programming Learning Platform

CodePath Academy is an enterprise-grade, full-stack interactive engineering learning platform built with **Spring Boot 3.3.4 (Java 21)**, **MySQL 8.0**, and **Vite + React 18 with Tailwind CSS**.

The platform is purpose-built to guide students through foundational computer science and modern frameworks step-by-step, featuring an embedded **Monaco Code Editor**, safe test-case evaluation, interactive quizzes with answer justifications, visual prerequisite dependency graphs, personal markdown engineering notes, and an operational **Admin Console**.

---

## 🌟 Key Platform Features

### 1. 3-Pane Interactive Learning Workspace
- **Navigation Pane**: Course syllabus tree, modules, and topic progression indicators.
- **Content Pane**: In-depth theoretical walkthroughs with syntax breakdowns and interactive explanations.
- **Embedded Monaco Editor**: Multi-language code practice (Java, Python, C++, C, JavaScript, SQL) with line highlighting and keyboard shortcuts.
- **"Understand This Code" Analyzer**: 6-dimensional code breakdown covering:
  1. *Plain English Summary*
  2. *Line-by-Line Execution Walkthrough*
  3. *Key Programming Concepts Identified*
  4. *Memory & Performance Implications*
  5. *Common Beginner Pitfalls & Bugs*
  6. *Real-World Production Applications*
- **"How This Platform Works" Modal**: Architectural request tracer that visualizes the client-to-database journey for educational transparency.

### 2. Multi-Language & Modern Framework Coverage
- **Core Languages**: C, C++, Java, Python, JavaScript, and SQL.
- **Frameworks & Ecosystems**: Spring Boot, Spring Framework, Hibernate / JPA, React, Node.js, Express.js, Django, Flask, MySQL, REST APIs, Git/GitHub, Docker, and DevOps principles.
- **Ecosystem Relationship Maps**: Understand *why* and *how* frameworks build upon language foundations (e.g. Java → Spring Boot, JavaScript → React/Node, Python → Django).

### 3. Gamification & Career Readiness
- **Experience Points (XP) & Levels**: Earn XP through lesson completion, quiz accuracy, and coding submissions.
- **Daily Coding Streaks**: Keep consistent habits with automated streak counters.
- **Unlockable Badges**: First Steps, Polyglot Apprentice, Quiz Wizard, Bug Hunter, Code Ninja, Sprint Finisher.
- **Categorized Technical Interview Prep**: Curated question bank across Core CS, System Design, Frameworks, and SQL with collapsible answers.
- **Tiered Engineering Projects**: Real-world blueprints (Beginner, Intermediate, Advanced) with architectural specifications.
- **Personal Engineering Notebook**: Markdown editor with live preview for taking notes during lessons.
- **Bookmarks Hub**: Save critical topics, lessons, coding challenges, or interview questions.

### 4. Admin Operations Console
- **Role-Based Security**: Strict access segregation between `ROLE_USER` and `ROLE_ADMIN`.
- **Telemetry & Metrics**: Total users, active enrollment, quizzes taken, code runs, and completion rates.
- **Visual Analytics**: Interactive Recharts user growth area charts and curriculum popularity breakdowns.
- **User Management**: Search user accounts, toggle administrator privileges, and manage accounts.
- **Curriculum Authoring**: Create new courses, toggle published/draft statuses, and manage course offerings.

---

## 🏗️ Architecture & Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Frontend Framework** | React | 18.3.1 | Modular UI Component Architecture |
| **Build Tool** | Vite | 5.4.21 | Ultra-fast HMR and bundling |
| **Styling** | Tailwind CSS | 3.4.17 | Dark engineering-grade aesthetic |
| **Code Editor** | Monaco Editor | 0.44.0 | VS Code browser editor experience |
| **Data Visualization** | Recharts | 2.12.7 | User growth & skill distribution charts |
| **Animation & Confetti** | Framer Motion & canvas-confetti | Latest | Milestone unlocks and quiz celebrations |
| **Icons** | Lucide React | Latest | Clean developer iconography |
| **Backend Framework** | Spring Boot | 3.3.4 | Robust REST API microservices |
| **Language** | Java | 21 / 23 | High-performance enterprise backend |
| **Security & Auth** | Spring Security + JJWT | 0.12.6 | Stateless JWT Access & Refresh Tokens |
| **Persistence** | Spring Data JPA / Hibernate | 6.5.3 | Object-Relational Mapping |
| **Database** | MySQL | 8.0 | Normalized relational database schema |
| **API Documentation** | Springdoc OpenAPI (Swagger) | 2.6.0 | Interactive API documentation |

---

## 🚀 Quick Start & Running Locally

### Prerequisites
- **Java 21+** (JDK installed and configured in `PATH`)
- **Maven 3.9+**
- **Node.js 18+** and **npm**
- **MySQL 8.0+** running on `localhost:3306`

### 1. Database Configuration
Ensure MySQL is running. The backend automatically creates the database if it doesn't exist and runs Flyway/Hibernate schema generation:
- **Database Name**: `codepath_academy`
- **Port**: `3306`
- **Default Username**: `root`
- **Default Password**: `root`

*(To customize credentials, edit `backend/src/main/resources/application.properties`)*

### 2. Start the Backend Server
```bash
cd backend
mvn spring-boot:run
```
- **Backend API**: `http://localhost:8080`
- **Swagger UI**: `http://localhost:8080/swagger-ui/index.html`
- **OpenAPI JSON**: `http://localhost:8080/v3/api-docs`

### 3. Start the Frontend Application
```bash
cd frontend
npm install
npm run dev
```
- **Web Application**: `http://localhost:5173`
- *Note: Vite automatically proxies `/api` requests to `http://localhost:8080`.*

---

## 🔑 Pre-Seeded Credentials

CodePath Academy comes with pre-seeded test accounts and complete curriculum data:

| Role | Username / Email | Password | Access Level |
|---|---|---|---|
| **Student** | `student@codepath.com` | `Student@123` | Learning paths, 3-pane lessons, quizzes, coding lab, notebooks, bookmarks |
| **Admin** | `admin@codepath.com` | `Admin@123` | Full student capabilities + Admin Operations Console, User Management, Course CRUD |

*Quick login buttons are available on the `/login` page for fast testing.*

---

## 📡 REST API Overview

### Authentication (`/api/auth`)
- `POST /api/auth/register` – Register new student account
- `POST /api/auth/login` – Authenticate and receive access + refresh JWT
- `POST /api/auth/refresh` – Exchange refresh token for new access token
- `POST /api/auth/logout` – Clear session

### Curriculum & Content (`/api/*`)
- `GET /api/languages` – List all 6 programming languages with metadata
- `GET /api/languages/{slug}` – Language details, compilation models, related frameworks
- `GET /api/frameworks` – List all supported frameworks and language relationships
- `GET /api/courses` – List courses with module counts and estimated hours
- `GET /api/courses/{id}` – Full course syllabus tree
- `GET /api/lessons/{id}` – Interactive lesson content with starter code
- `POST /api/lessons/understand-code` – 6-dimension code analysis engine
- `GET /api/lessons/how-it-works` – Architecture request tracer

### Coding & Quizzes (`/api/*`)
- `GET /api/problems` – Catalog of coding challenges (filterable by difficulty/category)
- `POST /api/problems/{id}/run` – Evaluate code against visible test cases
- `POST /api/problems/{id}/submit` – Evaluate code against all test cases and award XP
- `GET /api/quizzes/topic/{topicId}` – Fetch topic quiz questions
- `POST /api/quizzes/{id}/submit` – Grade quiz submission and return explanations

### Student Workspace & Telemetry (`/api/*`)
- `GET /api/progress` – Comprehensive student dashboard analytics & charts
- `GET /api/progress/achievements` – Badges and lock/unlock statuses
- `GET /api/bookmarks` – Student saved bookmarks
- `POST /api/bookmarks/toggle` – Toggle bookmark on resource
- `GET /api/notes` – Personal Markdown notebook
- `POST /api/notes` – Save or update personal note
- `GET /api/search?q={query}` – Global full-text search across all content

### Administration (`/api/admin/*`) *(ROLE_ADMIN only)*
- `GET /api/admin/dashboard` – Operational platform KPIs and growth analytics
- `GET /api/admin/users` – List all registered users
- `PUT /api/admin/users/{userId}/role` – Promote or demote user roles
- `DELETE /api/admin/users/{userId}` – Remove user account
- `POST /api/admin/courses` – Author and publish new courses
- `PATCH /api/admin/courses/{id}/toggle-publish` – Toggle published/draft status
- `DELETE /api/admin/courses/{id}` – Delete course

---

## 🔒 Security & Code Execution Model

1. **Password Hashing**: BCrypt encryption with high salt rounds.
2. **Stateless JWT**: Short-lived HS256 access tokens paired with refresh tokens.
3. **Role Guards**: Frontend `ProtectedRoute` and `AdminRoute` coupled with Spring Security `@PreAuthorize("hasAuthority('ROLE_ADMIN')")`.
4. **Safe Predefined Code Runner**: Test-case validation executes in a safe, deterministic sandbox without executing arbitrary remote shell commands on the host OS.

---

## 👥 Authors
Built for the **CodePath Academy** interactive programming education initiative.
