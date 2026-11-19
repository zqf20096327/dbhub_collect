# Campus Maintenance & Facility Issue Reporting System

A web-based platform for reporting, managing, and tracking maintenance issues at East West University (EWU).

**[🚀 Live Demo](https://campus-maintenance.pages.dev)** | **[GitHub Repository](https://github.com/Tahsin-Jawad/Campus-Maintenance)**

---

## About the Project

This project originally started as part of my **CSE 302 – Database Systems** course at East West University.

While working on the project, I realized that a campus maintenance and issue reporting system could be genuinely useful beyond an academic assignment. So, instead of keeping it as just a university project, I decided to take it a step further by hosting it online, improving its functionality, and making it accessible through the web.

The primary goal is to build something practical for my own campus — a platform where students and faculty members can report facility issues, track complaints, and help make campus maintenance more organized and efficient.

Although it was initially developed with East West University in mind, the system is designed in a way that others can explore and use as well.
## Features

- User Registration and Login
- Role-Based Authentication
- Student and Faculty Complaint Submission
- Complaint Tracking and History
- Admin Dashboard
- Maintenance Staff Dashboard
- Complaint Assignment to Staff
- Complaint Status Management
- User Feedback and Rating System

## User Roles

| Role | Responsibilities |
|---|---|
| Student | Submit complaints and track progress |
| Faculty | Report campus facility issues |
| Admin | Manage complaints and assign staff |
| Maintenance Staff | Handle assigned complaints and update status |

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Node.js, Express.js |
| Database | TiDB Cloud (MySQL compatible) |
| Database Driver | mysql2 |
| Authentication | JSON Web Token (JWT) |
| Password Security | bcryptjs |
| Version Control | Git, GitHub |

## Database Design

**Database Name:** `ewu_campus_maintenance`

The database contains 9 tables:

| Table | Purpose |
|---|---|
| roles | Stores user roles |
| users | Stores user information |
| locations | Stores campus locations |
| categories | Stores complaint categories |
| statuses | Stores complaint statuses |
| complaints | Stores complaint details |
| staff_assignments | Stores staff assignments |
| complaint_history | Stores complaint history |
| feedback | Stores user feedback |

Primary Keys and Foreign Keys maintain relationships and data integrity.

## Project Architecture

1. The frontend sends API requests to the backend.
2. The backend validates requests and handles application logic.
3. The backend communicates with the database.
4. The database stores and retrieves application data.
5. The backend returns responses to the frontend.

## Deployment

| Component | Platform |
|---|---|
| Frontend | Cloudflare Pages |
| Backend API | Render |
| Database | TiDB Cloud |

- **Live Website:** https://campus-maintenance.pages.dev
- **Backend API:** https://ewu-campus-maintenance-api.onrender.com

## Run Locally

### Prerequisites

- Node.js and npm
- A configured TiDB Cloud database

### 1. Clone the Repository

```bash
git clone https://github.com/Tahsin-Jawad/Campus-Maintenance.git
cd Campus-Maintenance
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and add your own database credentials and JWT secret.

```env
PORT=5000
TIDB_HOST=your_tidb_host
TIDB_PORT=4000
TIDB_USER=your_tidb_user
TIDB_PASSWORD=your_tidb_password
TIDB_DATABASE=ewu_campus_maintenance
TIDB_ENABLE_SSL=true
JWT_SECRET=your_jwt_secret
```

### 4. Start the Backend

```bash
npm start
```

The backend will run at:

`http://localhost:5000`

## Future Improvements

- Improve user interface and accessibility.
- Add more reporting and monitoring features.
- Enhance complaint analytics and management.

---
 
**Project Status:** Deployed — Under Development  
**Live Demo:** [campus-maintenance.pages.dev](https://campus-maintenance.pages.dev)  
**GitHub:** [Tahsin-Jawad/Campus-Maintenance](https://github.com/Tahsin-Jawad/Campus-Maintenance)
