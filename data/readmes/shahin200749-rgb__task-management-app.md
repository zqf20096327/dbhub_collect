# Task Management Application

A full-stack Task Management Application built using React, Node.js, Express.js and TiDB.

## Features

- User Registration and Login
- JWT Authentication and Authorization
- Add New Tasks
- View All Tasks
- Edit Existing Tasks
- Delete Tasks
- Mark Tasks as Completed
- Database Integration
- Responsive Design for Mobile and Desktop

## Technologies Used

**Frontend**
- React.js
- HTML
- CSS
- JavaScript

**Backend**
- Node.js
- Express.js
- REST API
- JWT
- bcryptjs

**Database**
- TiDB (MySQL compatible)

## Project Structure

```text
task-management-app/
├── frontend/
└── backend/
```

## Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/shahin200749-rgb/task-management-app.git
```

### 2. Start Backend

```bash
cd backend
npm install
```

Create a `.env` file inside the backend folder with your own database credentials and JWT secret.

```env
DB_HOST=your_host
DB_PORT=4000
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=task_management
JWT_SECRET=your_secret
```

Start the backend:

```bash
npm run dev
```

### 3. Start Frontend

Open another terminal:

```bash
cd frontend
npm install
npm start
```

Open `http://localhost:3000` in your browser.

## Author

Shahin S.

B.E. Electronics and Communication Engineering

Full Stack Development Project