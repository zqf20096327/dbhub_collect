# 🚀 Project Management Tool

A full-featured **Project Management Web Application** built with modern technologies, enabling teams to collaborate efficiently through real-time updates, Kanban boards, analytics, and more.

---

## ✨ Features

### 🗂️ Project Management

* Create, update, and delete projects with full ownership control
* Invite team members and assign roles (**Admin / Member**)
* Track project activity and performance

### 📋 Kanban Board

* Drag-and-drop task cards (**To Do → In Progress → Done**)
* Real-time updates using **Socket.io**
* Persistent task ordering with float-based positioning

### ✅ Task Management

* Create tasks with title, description, priority, and due date
* Assign tasks to team members
* Add comments and file attachments
* Activity logs for every task

### 📊 Analytics Dashboard

* Visual charts using **Recharts**
* Task completion insights
* Priority distribution breakdown

### 📅 Calendar View

* Track tasks based on due dates in a calendar format

### 📝 Notes

* Sticky notes with color coding
* Pin important notes
* User-specific note management

### 🔔 Notifications

* Real-time in-app notifications
* Notification center with read/unread states

### 👥 Team Management

* View project members and roles
* Manage permissions and assigned tasks

### ⚙️ Settings

* Dark / Light mode toggle
* User profile and avatar management

### 🔐 Security & Authentication

* JWT-based authentication (**access + refresh tokens**)
* Secure HTTP-only cookies
* Password hashing with **bcryptjs**
* Rate limiting & security headers (**Helmet**)
* Input validation using **Zod**

---

## 🛠️ Tech Stack

### Frontend

* React (Vite)
* Tailwind CSS
* React Router DOM
* Zustand (State Management)
* Axios
* Socket.io Client
* @dnd-kit (Drag & Drop)
* Recharts
* Lucide Icons

### Backend

* Node.js
* Express.js
* Prisma ORM
* PostgreSQL
* Socket.io
* JWT Authentication
* bcryptjs
* Zod
* Multer
* Helmet
* Morgan

---

## 📁 Project Structure

```
project-management-tool/
├── backend/
│   ├── prisma/
│   ├── src/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── sockets/
│   │   └── utils/
│   ├── uploads/
│   └── seed.js
│
└── frontend/
    ├── src/
    │   ├── features/
    │   ├── components/
    │   ├── context/
    │   ├── hooks/
    │   ├── services/
    │   └── router/
```

---

## 🗄️ Database Schema (Overview)

* **User** → Projects, Tasks, Notes, Notifications
* **Project** → Members, Tasks
* **Task** → Comments, Attachments, Activity Logs
* **ProjectMember** → Role-based access
* **Notification / Notes / ActivityLog**

---

## 📡 API Overview

### Auth

```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/refresh
```

### Projects

```
GET    /api/projects
POST   /api/projects
GET    /api/projects/:id
PUT    /api/projects/:id
DELETE /api/projects/:id
```

### Tasks

```
GET    /api/projects/:projectId/tasks
POST   /api/projects/:projectId/tasks
PATCH  /api/tasks/:id/status
```

### Notes / Notifications / Users

```
/api/notes
/api/notifications
/api/users
```

---

## 🚀 Getting Started

### 1. Clone Repository

### 2. Backend Setup

```bash
cd backend
npm install
cp .env.example .env
npx prisma migrate dev
npx prisma generate
npm run dev
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🔐 Environment Variables

```env
DATABASE_URL=
PORT=5000
FRONTEND_URL=http://localhost:5173

JWT_SECRET=
JWT_REFRESH_SECRET=
JWT_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d
```

---

## 🛜 Real-Time Events

* `task:created`
* `task:updated`
* `task:status`
* `task:deleted`
* `comment:added`
* `notification:new`

---

## 📜 Scripts

### Backend

```bash
npm run dev
npm run start
```

### Frontend

```bash
npm run dev
npm run build
npm run preview
```

## 📄 License

MIT License

---

## 👨‍💻 Author

**Nouman A Khan**

* GitHub: https://github.com/noumanakhan1
* LinkedIn: https://linkedin.com/in/noumanakhan

---

  Built with ❤️ using MERN + PostgreSQL + Prisma...
