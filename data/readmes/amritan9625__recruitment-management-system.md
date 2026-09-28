# HireFlow
### Recruitment Management System

A full-stack recruitment management application built with **React** and **Spring Boot**. It supports role-based access for administrators, recruiters, interviewers, and candidates, with workflows for managing jobs, candidate profiles, applications, interviews, and offers.

## Live Demo

* **Frontend:** https://recruitment-management-system-frontend-ztke.onrender.com
* **Backend API:** https://recruitment-management-system-frsv.onrender.com

> The backend may take a short time to respond if its free hosting service has been idle.

## Features

* User registration and login with JWT authentication
* Role-based navigation and access control
* Dashboard with role-appropriate information
* Candidate profile creation and editing
* Job listing and job management
* Candidate job applications and application tracking
* Interview scheduling and management
* Offer management
* Pagination, sorting, filtering, and searching in management lists
* Form validation, loading indicators, and error feedback

## User Roles

| Role            | Main permissions                                                                                           |
| --------------- | ---------------------------------------------------------------------------------------------------------- |
| **ADMIN**       | Manage users, roles, jobs, candidates, applications, interviews, and offers                                |
| **RECRUITER**   | Manage recruitment workflows, including jobs, candidates, applications, interviews, and offers             |
| **INTERVIEWER** | Access the dashboard, view candidates, and manage interviews                                               |
| **CANDIDATE**   | Manage their profile, browse jobs, apply for jobs, and view their own applications, interviews, and offers |

Access is enforced by the backend as well as the frontend. Candidate-specific operations use the authenticated account rather than trusting a candidate ID supplied by the client.

## Technology Stack

| Layer             | Technologies                          |
| ----------------- | ------------------------------------- |
| Frontend          | React, Vite, JavaScript, CSS          |
| Backend           | Java 21, Spring Boot, Spring Security |
| Authentication    | JWT                                   |
| API documentation | OpenAPI / Swagger                     |
| Database          | TiDB Cloud                            |
| Deployment        | Render                                |

## Repository Structure

```text
recruitment-management-system/
├── backend/       # Spring Boot REST API
├── frontend/      # React + Vite application
└── README.md      # Project documentation
```

## Run Locally

### Prerequisites

* Java 21
* Node.js and npm
* Git
* Access to a configured database

### 1. Start the backend

Open a terminal in the repository root:

```bash
cd backend
```

Configure the backend database connection and required environment variables using the project's existing Spring Boot configuration. **Do not commit database passwords, JWT secrets, or other credentials.**

Run the Spring Boot application using the Maven wrapper:

```bash
./mvnw spring-boot:run
```

On Windows Command Prompt, use:

```bat
mvnw.cmd spring-boot:run
```

The backend should start at:

```text
http://localhost:8080
```

### 2. Configure and start the frontend

Open a second terminal:

```bash
cd frontend
```

Create a local `.env` file with the backend URL:

```env
VITE_API_BASE_URL=http://localhost:8080
```

Install dependencies and start the Vite development server:

```bash
npm install
npm run dev
```

Open the local URL printed by Vite, usually:

```text
http://localhost:5173
```

The frontend uses `VITE_API_BASE_URL` to determine which backend API to call. For production, this variable is configured in the frontend hosting environment.

## Application Workflow

1. Register or sign in.
2. Complete the candidate profile when using a Candidate account.
3. Browse available jobs and apply to an open job.
4. Track submitted applications from the Applications section.
5. Recruiters and administrators manage recruitment records through their role-specific sections.
6. Interviewers manage interview-related work according to their permissions.

## Security Notes

* JWT authentication protects secured API requests.
* Backend authorization restricts access by role.
* Candidate profile and application operations are associated with the authenticated user.
* Environment files containing local credentials should not be committed.
* Values prefixed with `VITE_` are included in the frontend build and must not contain secrets.

## Deployment

The frontend and backend are deployed separately on Render. The frontend is configured to use the deployed backend API, and the static site uses a rewrite rule so React Router routes continue to work when opened or refreshed directly.

## Screenshots

### Login page
![Login page](screenshots/login.png)

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Jobs
![Jobs](screenshots/jobs.png)

### Candidate Profile
![Candidate Profile](screenshots/candidate-profile.png)

### Applications
![Applications](screenshots/applications.png)

## Author

**Amritan Kumar**

GitHub: https://github.com/amritan9625
