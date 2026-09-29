# 📌 Notice Board – Reno Platforms Assignment

A full-stack **CRUD Notice Board** application built with **Next.js (Pages Router)**, **Prisma ORM**, and **TiDB Cloud (MySQL)**. The application allows users to create, view, edit, and delete notices with server-side validation and persistent database storage.

## 🚀 Live Demo

🌐 **Live Application:**  
https://notice-board-gilt.vercel.app

📂 **GitHub Repository:**  
https://github.com/ajeet4302/notice-board

---

## 📖 Project Overview

This application was developed as part of the **Reno Platforms Web Development Assignment**.

The Notice Board supports complete CRUD functionality while following the required technology stack:

- Next.js (Pages Router)
- Prisma ORM
- TiDB Cloud (Hosted MySQL)
- Vercel Deployment

---

## ✨ Features

- ✅ Create Notice
- ✅ View All Notices
- ✅ Edit Existing Notice
- ✅ Delete Notice with Confirmation
- ✅ Server-side Validation
- ✅ Persistent Database Storage
- ✅ Responsive Design (Mobile & Desktop)
- ✅ Urgent Notices Displayed First
- ✅ Red "Urgent" Badge
- ✅ RESTful API Routes

---

## 🛠 Tech Stack

| Technology | Usage |
|------------|-------|
| Next.js 14 | Frontend & Backend (Pages Router) |
| React | UI |
| Prisma ORM | Database ORM |
| TiDB Cloud | Hosted MySQL Database |
| Tailwind CSS | Styling |
| Vercel | Deployment |

---

## 📂 Project Structure

```
notice-board/
│── components/
│── lib/
│── pages/
│   ├── api/
│   ├── notices/
│   └── index.js
│── prisma/
│── styles/
│── public/
│── package.json
│── README.md
```

---

## ⚙️ Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/ajeet4302/notice-board.git
cd notice-board
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env` file.

Add:

```env
DATABASE_URL="mysql://<username>:<password>@<host>:4000/notice_board?sslaccept=strict"
```

### 4. Push Prisma Schema

```bash
npx prisma db push
```

### 5. Generate Prisma Client

```bash
npx prisma generate
```

### 6. Run the Development Server

```bash
npm run dev
```

Open:

```
http://localhost:3000
```

---

## 🌐 Deployment

This application is deployed on **Vercel** using **TiDB Cloud** as the database.

Deployment Steps:

1. Push project to GitHub.
2. Import repository into Vercel.
3. Add `DATABASE_URL` in Environment Variables.
4. Deploy.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notices` | Get all notices |
| POST | `/api/notices` | Create a notice |
| GET | `/api/notices/[id]` | Get single notice |
| PUT | `/api/notices/[id]` | Update notice |
| DELETE | `/api/notices/[id]` | Delete notice |

---

## ✅ Validation

The application validates the following fields on the server:

- Title (Required)
- Body (Required)
- Category
- Priority
- Publish Date

Invalid requests return appropriate HTTP status codes and validation errors.

---

## 📈 Future Improvements

Given more time, I would add:

- User Authentication
- Search & Filter Notices
- Pagination
- Image Upload using Vercel Blob or AWS S3
- Rich Text Editor
- Dark Mode
- Unit & Integration Tests

---

## 🤖 AI Usage

AI tools (ChatGPT) were used to assist with:

- Understanding assignment requirements
- Debugging Prisma and TiDB configuration
- Deployment guidance for GitHub and Vercel
- Code explanations and documentation improvements

All code was reviewed, tested, and integrated manually before submission.

---

## 👨‍💻 Author

**Ajeet Malviya**

GitHub:  
https://github.com/ajeet4302

---

## 📄 License

This project was created as part of the **Reno Platforms Web Development Assignment** and is intended for educational and evaluation purposes.
