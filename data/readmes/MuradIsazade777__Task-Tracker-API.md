# 📝 Task Tracker API

A lightweight, containerized task management system built with **Go (Gin)**, **PostgreSQL**, and **Vite + Nginx**. Designed for fast development, reproducibility, and future scalability — ideal for learning Docker, backend API design, and full-stack orchestration.
---

## 🚀 Features

- RESTful API with `GET` and `POST` endpoints
- PostgreSQL database with auto-init via `init.sql`
- Frontend served via Nginx (Vite build)
- Docker Compose orchestration
- Clean separation of concerns: `models`, `handlers`, `db`
- Environment-based configuration via `.env`
---

## 🧱 Tech Stack

| Layer      | Technology         |
|------------|--------------------|
| Backend    | Go + Gin           |
| Database   | PostgreSQL         |
| Frontend   | Vite + Nginx       |
| DevOps     | Docker Compose     |

---

## 📦 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/task-tracker-api.git
cd task-tracker-api

1. Create .env file
env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tasks
DB_URL=postgres://postgres:postgres@db:5432/tasks?sslmode=disable

2. Run the app
docker compose up --build

3. Access the app
Frontend: http://localhost:3000
Backend API: http://localhost:8080/tasks

📮 API Endpoints
GET /tasks
Returns all tasks.

json
[
  {
    "id": 1,
    "title": "Learn Docker",
    "completed": false
  }
]
POST /tasks
Creates a new task.

bash
curl -X POST http://localhost:8080/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "completed": false}'

🛠 Project Structure
Code
task-tracker-api/
├── backend/
│   ├── db/
│   ├── handlers/
│   ├── models/
│   └── main.go
├── frontend/
│   └── (Vite project)
├── db/
│   └── init.sql
├── .env
├── docker-compose.yml
└── README.md

📄 License
This project is licensed under the MIT License. See LICENSE for details.

🌟 Author
Murad — building scalable, reproducible, and impactful platforms. Follow my journey on GitHub: github.com/MuradIsazade777
