# Built On It 🚀

> A modern open-source platform for developers to discover, share, collaborate, and solve technical challenges together.

---

## 🌐 Live Deployments

- **Frontend Application:** [https://built-on-it-sies-1.onrender.com](https://built-on-it-sies-1.onrender.com)
- **Backend API:** [https://built-on-it-sies.onrender.com](https://built-on-it-sies.onrender.com)

---

## ✨ Features

- 🔍 **Explore Projects & Problems** — Discover developer-built solutions, open-source tools, and real-world challenges.
- 🗂️ **Categorized by Tech Stack** — Browse by tags, technologies, and project categories.
- 🤝 **Build Together** — Collaborate with developers and teams across the community.
- 💬 **AskDev & Solutions** — Community-driven Q&A and problem-solving hub.
- 📚 **Tutorials** — Step-by-step guides and learning resources.
- 👤 **Developer Profiles** — Showcase your projects, contributions, and skills.
- 📤 **Upload & Share** — Submit projects with screenshots and documentation.

---

## 🏗️ Repository Architecture & Organization

The repository is structured as a clean full-stack monorepo:

```text
Built_On_It/
├── backend/                  # Node.js + Express REST API
│   ├── routes/               # API route handlers
│   │   ├── problems.js       # Problems endpoints (create, fetch, search)
│   │   └── solutions.js      # Solutions & submission endpoints
│   ├── uploads/              # Storage directory for uploaded images/assets
│   ├── .env.example          # Template for backend environment variables
│   ├── db.js                 # TiDB/MySQL connection configuration
│   ├── package.json          # Backend dependencies and scripts
│   └── server.js             # Express application entrypoint
│
├── frontend/                 # React 18 + Vite Single Page Application
│   ├── public/               # Public assets and Netlify/Render redirects
│   ├── src/
│   │   ├── components/       # Reusable UI components (Sidebar, TopNav, Layout, etc.)
│   │   ├── pages/            # Page views (Home, Projects, AskDev, Profile, etc.)
│   │   ├── styles/           # Global styles and styling rules
│   │   ├── api.js            # Axios client configuration & base URL
│   │   ├── App.jsx           # Client-side router & application shell
│   │   └── main.jsx          # React DOM entrypoint
│   ├── .env.example          # Template for frontend environment variables
│   ├── index.html            # HTML shell
│   ├── package.json          # Frontend dependencies and scripts
│   └── vite.config.js        # Vite build tool configuration
│
├── .gitignore                # Root git ignore rules
└── README.md                 # Project documentation
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** [React 18](https://react.dev/)
- **Bundler & Build Tool:** [Vite](https://vitejs.dev/)
- **Routing:** [React Router v6](https://reactrouter.com/)
- **HTTP Client:** [Axios](https://axios-http.com/)
- **Styling:** Custom CSS with CSS variables

### Backend
- **Runtime:** [Node.js](https://nodejs.org/)
- **Framework:** [Express.js](https://expressjs.com/)
- **Database:** MySQL / [TiDB Serverless Cloud](https://www.pingcap.com/tidb-cloud/) (via `mysql2`)
- **File Uploads:** [Multer](https://github.com/expressjs/multer)
- **CORS & Environment:** `cors`, `dotenv`

---

## 🚀 Getting Started Locally

### Prerequisites
- [Node.js](https://nodejs.org/) (v18+ recommended)
- [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/)
- MySQL or TiDB cloud database instance

---

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Built_On_It.git
cd Built_On_It
```

---

### 2. Backend Setup

```bash
cd backend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
```

Open `backend/.env` and configure your credentials:
```env
DB_HOST=gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com
DB_PORT=4000
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=test
PORT=5000
```

Start the backend server:
```bash
# Start in watch mode (development)
npm run dev

# Or standard start
npm start
```

The API will be available at `http://localhost:5000`.

---

### 3. Frontend Setup

Open a new terminal window:

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
```

Set the API URL in `frontend/.env`:
```env
VITE_API_URL=http://localhost:5000
```

Start the Vite development server:
```bash
npm run dev
```

The application will run locally at `http://localhost:5173`.

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check endpoint |
| `GET` | `/problems` | Fetch all problems / discussions |
| `POST` | `/problems` | Create a new problem post |
| `GET` | `/solutions` | Fetch submitted solutions |
| `POST` | `/solutions` | Submit a project or solution (with image upload) |
| `GET` | `/uploads/:filename` | Serve uploaded assets |

---

## 📄 License

This project is licensed under the [ISC License](LICENSE).
