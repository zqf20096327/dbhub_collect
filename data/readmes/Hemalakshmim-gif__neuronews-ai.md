# 🧠 NeuroNews AI – Personalized AI News Agent

NeuroNews AI is a full-stack AI-powered news platform that delivers personalized news based on user interests. It leverages Artificial Intelligence to summarize articles, recommend relevant content, and provide an engaging reading experience.

## 🚀 Live Demo

### 🌐 Frontend
https://neuronews-ai-lime.vercel.app

### 🚀 Backend API
https://neuronews-ai.onrender.com

---

# ✨ Features

- 🔐 User Authentication (JWT)
- 📰 Personalized News Feed
- 🤖 AI-powered News Summaries (Google Gemini)
- ❤️ Bookmark Favorite Articles
- 📜 Reading History
- 🎯 AI-based News Recommendations
- 🌙 Dark & Light Theme
- 🔍 Search News
- 📱 Responsive UI
- ☁️ Cloud Database (TiDB Cloud)

---

# 🛠️ Tech Stack

## Frontend
- React.js
- Vite
- React Router
- Axios
- CSS3
- React Toastify
- Lucide React

## Backend
- Node.js
- Express.js
- JWT Authentication
- bcryptjs
- Google Gemini API

## Database
- TiDB Cloud (MySQL Compatible)

## Deployment
- Frontend: Vercel
- Backend: Render

---

# 📂 Project Structure

```
NeuroNews-AI
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   ├── hooks
│   │   ├── context
│   │   ├── services
│   │   ├── routes
│   │   └── styles
│   │
│   └── package.json
│
├── backend
│   ├── config
│   ├── controllers
│   ├── middleware
│   ├── routes
│   ├── services
│   ├── utils
│   ├── certs
│   └── server.js
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Hemalakshmim-gif/neuronews-ai.git

cd neuronews-ai
```

---

## Backend Setup

```bash
cd backend

npm install

npm run dev
```

Create a `.env` file:

```env
PORT=5000

DB_HOST=YOUR_DATABASE_HOST
DB_PORT=4000
DB_USER=YOUR_DATABASE_USER
DB_PASSWORD=YOUR_DATABASE_PASSWORD
DB_NAME=neuronews_ai

JWT_SECRET=YOUR_SECRET_KEY

NEWS_API_KEY=YOUR_NEWSDATA_API_KEY

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# 📸 Screenshots

Add screenshots of:

- Home Page
- Login
- Signup
- AI Summary
- Bookmarks
- Profile
- Recommendation Page

---

# 🔑 API Endpoints

## Authentication

```
POST /api/auth/signup
POST /api/auth/login
```

## News

```
GET /api/news
GET /api/news/search
```

## AI

```
POST /api/ai/summary
GET /api/ai/feed
```

## Bookmarks

```
GET /api/bookmarks
POST /api/bookmarks
DELETE /api/bookmarks/:id
```

## History

```
GET /api/history
POST /api/history
```

## Profile

```
GET /api/profile
PUT /api/profile
```

---

# 🌟 Future Improvements

- Voice-based News Reading
- AI Chatbot for News
- Multi-language Support
- Email Notifications
- Push Notifications
- Trending Analytics Dashboard
- Real-time News Updates

---

# 📖 Learning Outcomes

This project helped in learning:

- React.js
- Express.js
- REST API Development
- JWT Authentication
- Google Gemini API Integration
- Cloud Database (TiDB)
- Full Stack Deployment
- Responsive UI Design
- API Integration
- Git & GitHub Workflow

---

# 👨‍💻 Author

**Hemalakshmi M**

Computer Science Engineering Student

GitHub:
https://github.com/Hemalakshmim-gif

LinkedIn:
(Add your LinkedIn Profile)

---

# ⭐ Support

If you like this project, don't forget to **Star ⭐ the repository**.

Contributions, suggestions, and feedback are always welcome!
