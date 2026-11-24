# Karya API - Task Management API

**Live API (Swagger UI):** [https://karya-api-e0ok.onrender.com/swagger/](https://karya-api-e0ok.onrender.com/swagger/)

A production-ready Task Management API MVP built with Django REST Framework, featuring JWT authentication, comprehensive search/filtering, and automatic Swagger UI documentation. The API is containerized using Docker and deployed on Render with PostgreSQL.

## Features

- **Authentication**: Secure JWT (JSON Web Tokens) implementation for login and signup.
- **Task Management**: Full CRUD operations with strict user-isolation (users can only access their own tasks).
- **Advanced Querying**: 
  - Custom page-number pagination (default: 10 items/page).
  - Filter by `status` (Pending, In Progress, Completed) and `priority` (Low, Medium, High).
  - Search functionality across task `title` and `description`.
- **Documentation**: Auto-generated Swagger UI and ReDoc integration.
- **Production Infrastructure**: Dockerized environment, PostgreSQL database, Gunicorn WSGI server, and Infrastructure as Code (IaC) via `render.yaml`.

## Tech Stack

- **Backend**: Python 3.12, Django 5.2, Django REST Framework
- **Database**: PostgreSQL (Production) / SQLite (Local)
- **Authentication**: SimpleJWT (`djangorestframework_simplejwt`)
- **Deployment & DevOps**: Docker, Render, Gunicorn, Whitenoise

---

## How the API Works (Workflow)

This API uses stateless JWT authentication. Here is the standard workflow to interact with the endpoints:

### 1. Registration & Login
- **Signup**: Send a `POST` request to `/api/auth/signup/` with a `username`, `password`, and `confirm_password`. The API will create the user and immediately return an `access` token and a `refresh` token.
- **Signin**: Existing users can send a `POST` request to `/api/auth/signin/` with their credentials to receive the tokens.

### 2. Authenticated Requests
- To access protected endpoints (like creating or viewing tasks), you must include the access token in the HTTP Headers of your request:
  ```http
  Authorization: Bearer <your_access_token>
  ```

### 3. Managing Tasks
- **Create**: Send a `POST` request to `/api/tasks/`. The task will automatically be assigned to the authenticated user.
- **Retrieve/Update/Delete**: Use `GET`, `PUT`, `PATCH`, or `DELETE` on `/api/tasks/{id}/`. The API strictly isolates data; you will get a `404 Not Found` if you try to access another user's task.

### 4. Refreshing Tokens
- Access tokens expire for security reasons. When it expires, send a `POST` request to `/api/auth/token/refresh/` containing your `refresh` token to obtain a new access token without needing to log in again.

---

## 📡 API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/swagger/` | GET | Swagger UI Documentation | No |
| `/api/auth/signup/` | POST | Register a new user & get tokens | No |
| `/api/auth/signin/` | POST | Login and get JWT tokens | No |
| `/api/auth/token/refresh/` | POST | Refresh JWT access token | No |
| `/api/tasks/` | GET, POST | List user's tasks or create a new task | Yes |
| `/api/tasks/<id>/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a specific task | Yes |

---

## 🛠️ Local Development Setup

### Option 1: Using Docker (Recommended)
1. Clone the repository:
   ```bash
   git clone [https://github.com/ft-mammoo/Karya-API.git](https://github.com/ft-mammoo/Karya-API.git)
   cd Karya-API
   ```
2. Build and run the Docker container:
   ```bash
   docker build -t karya-api .
   docker run -p 8000:8000 karya-api
   ```
3. Access the API documentation at `http://localhost:8000/swagger/`

### Option 2: Using Python Virtual Environment
1. Clone the repository:
   ```bash
   git clone [https://github.com/ft-mammoo/Karya-API.git](https://github.com/ft-mammoo/Karya-API.git)
   cd Karya-API
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables by copying `.env.dist` to `.env` and updating the values:
   ```bash
   cp .env.dist .env
   ```
5. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
