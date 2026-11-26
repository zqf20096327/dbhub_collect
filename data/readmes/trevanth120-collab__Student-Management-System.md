
# Student Management System

A full-stack web application for managing student records with secure administrator authentication.

## Live Demo

- **Live Website:** https://trevanth120-collab.github.io/Student-Management-System/
- **Backend API:** https://student-management-system-3rni.onrender.com
- **API Documentation:** https://student-management-system-3rni.onrender.com/docs
- **GitHub Repository:** https://github.com/trevanth120-collab/Student-Management-System

## Project Overview

The Student Management System is a web-based application that allows an administrator to manage student information through a simple and user-friendly interface.

The frontend communicates with a Python FastAPI backend through REST APIs. Student records are stored in a MySQL-compatible database.

This project demonstrates full-stack development, API integration, database connectivity, authentication and cloud deployment.

## Features

- Secure administrator login using JWT authentication.
- Register new students.
- View all student records.
- Search student records.
- Update student information.
- Delete student records.
- Manage student departments using predefined options.
- Export student records as CSV.
- Department analytics dashboard.
- Database integration and data persistence.
- API validation and error handling.

## Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic
- JWT Authentication
- Argon2 Password Hashing

### Database
- MySQL Server (local development)
- TiDB Cloud (MySQL-compatible database for deployment)
- MySQL Connector for Python

### Tools
- Visual Studio Code
- MySQL Workbench
- Git
- GitHub

## Project Architecture

The application follows a three-tier architecture:

1. **Frontend:** HTML, CSS and JavaScript provide the user interface.
2. **Backend:** FastAPI handles API requests, authentication and application logic.
3. **Database:** TiDB Cloud stores student and administrator information.

### Deployment

- Frontend: GitHub Pages
- Backend: Render
- Database: TiDB Cloud

## Project Structure

```text
studentmanagementsystem/
│
├── backend/
│   ├── main.py
│   └── database.py
│
├── screenshots/
│
├── index.html
├── login.html
├── login.js
├── script.js
├── style.css
├── create_admin.py
├── test.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/trevanth120-collab/Student-Management-System.git
```

### 2. Open the Project Folder

```bash
cd Student-Management-System
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Configure your own local database credentials:

```env
SECRET_KEY=your_secret_key
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=student_management
DB_PORT=3306
```

Make sure your local MySQL database and required tables are configured.

**Important:** Never upload your `.env` file or secret credentials to GitHub.

### 5. Start the Backend

```bash
python -m uvicorn backend.main:app --reload
```

### 6. Open the Frontend

Use the VS Code Live Server extension to open `login.html`.

### 7. Access API Documentation

Open the following URL in your browser:

http://127.0.0.1:8000/docs

## Project Objectives

- Develop a full-stack student management application.
- Understand frontend and backend integration.
- Build REST APIs using FastAPI.
- Connect Python applications with a MySQL database.
- Implement authentication and authorization using JWT.
- Perform CRUD operations on student records.
- Deploy a web application using cloud platforms.

## Learning Outcomes

Through this project, I gained practical experience in:

- Frontend development using HTML, CSS and JavaScript.
- Backend development using Python and FastAPI.
- REST API development and integration.
- SQL and database connectivity.
- JWT authentication and password hashing.
- Git and GitHub version control.
- Cloud application deployment.

## Project Screenshots

### Login Page
![Login Page](screenshots/login-page.png)

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Student Registration
![Student Registration](screenshots/student-registration.png)

### Student Records
![Student Records](screenshots/student-records.png)

## Author

Developed as a learning project to gain practical experience in full-stack web development.
