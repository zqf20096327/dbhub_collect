<div align="center">
  <h1>🗳️ VoteSync — Real-Time Polling Platform</h1>

  <img src="https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel" alt="Deployed on Vercel" />
  <img src="https://img.shields.io/badge/Node.js-v18+-green?style=for-the-badge&logo=node.js" alt="Node.js" />
  <img src="https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react" alt="React" />
  <img src="https://img.shields.io/badge/PostgreSQL-Neon-blue?style=for-the-badge&logo=postgresql" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Firebase-Realtime%20Database-ffca28?style=for-the-badge&logo=firebase&logoColor=black" alt="Firebase" />
  <img src="https://img.shields.io/badge/Socket.io-v4-010101?style=for-the-badge&logo=socketdotio" alt="Socket.io" />
  <img src="https://img.shields.io/badge/Swagger-API%20Docs-85ea2d?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License" />
</div>

**VoteSync** is a full-stack, production-ready polling application that enables users to **create live polls, collect real-time votes, and visualize results interactively**. It is built with a modern tech stack and designed for performance, scalability, and a premium user experience. Deployed and hosted on **Vercel** with a serverless backend.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Live Demo](#live-demo)
3. [Features](#features)
4. [Recent Enhancements](#recent-enhancements)
5. [How It Works](#how-it-works)
6. [Tech Stack](#tech-stack)
7. [Project Structure](#project-structure)
8. [Getting Started](#getting-started)
9. [Environment Variables](#environment-variables)
10. [API Reference](#api-reference)
11. [Database Schema](#database-schema)
12. [Deployment (Vercel)](#deployment-vercel)
13. [Vercel Configuration](#vercel-configuration)
14. [Troubleshooting](#troubleshooting)
15. [Known Limitations](#known-limitations)
16. [Contributing](#contributing)
17. [License](#license)

---

## 📖 Overview

VoteSync allows users to create and manage polls with various question types (single choice, multiple choice, image choice, open-ended). Participants can join live polls and see results update in real time. Presenters can export voter data to Excel and track participation.

The platform was migrated from MongoDB + Firebase to **PostgreSQL (Neon)**, retaining Firebase Realtime Database for live poll broadcasting. The backend Express server is hosted as a **Vercel Serverless Function**, making it globally fast and scalable with zero infrastructure management.

🎥 **[Watch Website Demo Video](https://screenapp.io/app/v/gqNauhDjUd)**

---

## 🌍 Live Demo

> The app is deployed on Vercel. Access the live version at:
>
> **Frontend**: `https://eventpoll-client-a2bl.vercel.app`
>
> **API Docs (Swagger)**: `https://eventpoll-client-a2bl.vercel.app/api-docs`

---

## ✨ Features

| Feature | Description | Status |
|---|---|---|
| ⚡ **Real-Time Voting** | Instant result updates via Socket.io | ✅ Live |
| 📊 **Live Charts** | Beautiful, animated charts using Chart.js | ✅ Live |
| 🔐 **JWT Authentication** | Secure, token-based auth with role-based access (admin / user) | ✅ Live |
| 👤 **User Sign-up & Sign-in** | Email/password registration with bcrypt hashing | ✅ Live |
| 📁 **Poll Templates** | Save and reuse question sets as templates | ✅ Live |
| 🗂️ **Multiple Question Types** | Single choice, multi-choice, image choice, open-ended | ✅ Live |
| 📥 **Excel Export** | Export voter data to `.xlsx` using ExcelJS | ✅ Live |
| 🎨 **Premium UI** | Glassmorphism, Framer Motion animations, Chakra UI | ✅ Live |
| 🌐 **Vercel Deployment** | Serverless backend + frontend on Vercel CDN | ✅ Live |
| 🔑 **Role-Based Access** | Admin dashboard vs User dashboard, separate permissions | ✅ Live |
| 📱 **Responsive Design** | Works on mobile, tablet, and desktop | ✅ Live |
| 🔒 **Authentication Gate** | Protected routes — login required to access core pages | ✅ Live |
| 🗳️ **Voter Tracking** | Tracks who voted on which option, prevents double-voting | ✅ Live |

---

## 🚀 Recent Enhancements

We have recently upgraded the platform with a series of features that improve robustness, user management, and overall design aesthetics:

- **Branding Update (VoteSync)**: Fully rebranded the system (Navbar, Title, Metadata, copyright notices, and Sign-in portals) to **VoteSync**.
- **Expansion of Ready-to-use Templates**: Expanded default templates from 4 to 8, adding Tech Stack Preferences, Remote Work Habits, Customer Satisfaction, and Health/Wellness check-ins.
- **Dedicated Results History Page**: Created a separate `/results` page to archive completed polls and view historical turnout metrics, isolating active poll management into the `/my-polls` view.
- **Live Active Presenter Dashboard**: Removed restrictive admin-only views to allow regular presenter accounts to create, launch, and monitor active polls from their own dashboard.
- **Copyable Poll Code & Share Link Extraction**: Presenters can now copy the short alphanumeric code itself directly from a successful creation modal. When joining an event, the portal automatically extracts this short code if a voter accidentally pastes the entire shareable URL.
- **Legal & Contact Information**: Added custom footer pages for **Terms of Service**, **Privacy Policy** (detailing Neon Postgres database security and Firebase usage), and **Contact Us** containing admin information.
- **Session Expiration Guard**: Added an Axios interceptor to catch `401` unauthorized calls. It logs users out and redirects them to `/signin?session_expired=true` with a clear info toast.
- **Resilient Fallback Screens**: Added retry buttons and detailed error screens to `Dashboard` and `Profile` views so if an API call fails, the user is not left with an infinite loading spinner.

---

## ⚙️ How It Works

### User Flow
```
User visits site → Redirected to Sign-in/Sign-up
        ↓
  Creates account or Signs in
        ↓
  JWT Token issued → Stored in localStorage
        ↓
  Redirected to Dashboard
        ↓
  User: Browse & vote on live polls
  Admin: Create polls, manage templates, view results
        ↓
  Poll ends → Results archived to PostgreSQL
```

### Voting Flow
```
Admin creates poll → Saved to Firebase Realtime DB
        ↓
  Share poll link with participants
        ↓
  Participant opens link → Authenticates via JWT
        ↓
  Answers questions → POST /api/firebase/vote
        ↓
  Firebase DB updates → All viewers see real-time results via Socket.io
        ↓
  Admin stops poll → Data saved to PostgreSQL for archive
```

---

## 🛠️ Tech Stack

### Frontend (`client/`)
- **React 18** — UI framework
- **Chakra UI** — Component library
- **Redux + Redux Thunk** — Global state & async actions
- **React Router Dom v6** — Client-side routing
- **Chart.js / react-chartjs-2** — Data visualization
- **Framer Motion** — Animations
- **Axios** — HTTP client
- **Socket.io Client** — Real-time communication

### Backend (`server/`)
- **Node.js + Express** — REST API server
- **PostgreSQL (Neon)** — Primary relational database (via `pg`)
- **Firebase Realtime Database** — Live poll state broadcasting
- **JWT (jsonwebtoken)** — Authentication tokens
- **bcryptjs** — Password hashing
- **ExcelJS** — Excel file generation
- **Socket.io** — WebSocket server
- **Swagger UI** — Interactive API documentation

### Infrastructure
- **Vercel** — Hosting (frontend + serverless API)
- **Neon PostgreSQL** — Managed cloud database

---

## 📁 Project Structure

Here is an overview of the workspaces setup in the monorepo structure. You can click on the file paths below to open them directly in your workspace:

* [package.json](file:///c:/Event%20poll/Eventpoll/package.json) — Monorepo root configuration and workspace scripts.
* [client](file:///c:/Event%20poll/Eventpoll/client) — React frontend application.
  * [client/vite.config.js](file:///c:/Event%20poll/Eventpoll/client/vite.config.js) — Vite environment configurations and local reverse proxy rules.
  * [client/src/App.jsx](file:///c:/Event%20poll/Eventpoll/client/src/App.jsx) — Core React router configuration.
* [server](file:///c:/Event%20poll/Eventpoll/server) — Express backend server.
  * [server/index.js](file:///c:/Event%20poll/Eventpoll/server/index.js) — Entry server file that switches configurations for local deployment vs Vercel Serverless Function.
  * [server/server.js](file:///c:/Event%20poll/Eventpoll/server/server.js) — Express app initialization, middleware configuration, API routing, and Socket.io binding.
  * [server/routes](file:///c:/Event%20poll/Eventpoll/server/routes) — API Endpoint route declarations:
    * [auth.routes.js](file:///c:/Event%20poll/Eventpoll/server/routes/auth.routes.js) — User authorization routes (signup, signin, google-signin).
    * [user.routes.js](file:///c:/Event%20poll/Eventpoll/server/routes/user.routes.js) — User profile details.
    * [poll.routes.js](file:///c:/Event%20poll/Eventpoll/server/routes/poll.routes.js) — Postgres-backed ended poll retrieval and Excel report exporting.
    * [firebase.routes.js](file:///c:/Event%20poll/Eventpoll/server/routes/firebase.routes.js) — Live poll creation, details, and voting on Firebase RTDB.
    * [template.routes.js](file:///c:/Event%20poll/Eventpoll/server/routes/template.routes.js) — Creating and retrieving pre-configured poll question templates.
  * [server/controllers](file:///c:/Event%20poll/Eventpoll/server/controllers) — Controller layer implementing core business logic:
    * [authController.js](file:///c:/Event%20poll/Eventpoll/server/controllers/authController.js) — Signup validation, password hashing, and token dispatch.
    * [userController.js](file:///c:/Event%20poll/Eventpoll/server/controllers/userController.js) — Fetch and assemble user profile details.
    * [pollController.js](file:///c:/Event%20poll/Eventpoll/server/controllers/pollController.js) — Manage active poll structures, persist to PostgreSQL, track voter selections, and build downloadable Excel spreadsheets.
    * [templateController.js](file:///c:/Event%20poll/Eventpoll/server/controllers/templateController.js) — Save templates and fetch them by unique identifier.
  * [server/models](file:///c:/Event%20poll/Eventpoll/server/models) — SQL-backed models querying PostgreSQL using `pg` pool:
    * [userModel.js](file:///c:/Event%20poll/Eventpoll/server/models/userModel.js) — PostgreSQL queries for user records and active associations.
    * [pollModel.js](file:///c:/Event%20poll/Eventpoll/server/models/pollModel.js) — PostgreSQL queries for completed polls (archived from Firebase).
    * [templateModel.js](file:///c:/Event%20poll/Eventpoll/server/models/templateModel.js) — PostgreSQL queries for templates.
  * [server/schema.sql](file:///c:/Event%20poll/Eventpoll/server/schema.sql) — Accurate schema table definitions for server queries.
  * [server/init-db.js](file:///c:/Event%20poll/Eventpoll/server/init-db.js) — Run this server script to configure table structures.
* [database](file:///c:/Event%20poll/Eventpoll/database) — Standalone database configuration:
  * [database/schema.sql](file:///c:/Event%20poll/Eventpoll/database/schema.sql) — Alternative, strict schema including database foreign key constraints.
  * [database/seed.sql](file:///c:/Event%20poll/Eventpoll/database/seed.sql) — Populates test data (admin/regular users, example template, and test completed poll).
  * [database/init-db.js](file:///c:/Event%20poll/Eventpoll/database/init-db.js) — Initializes database schema and seeds it from test data using server's environment variables.

---

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) v18+
- [PostgreSQL](https://www.postgresql.org/) (local) **or** a [Neon](https://neon.tech/) cloud database
- npm v8+ (for workspaces support)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/VIJAYAPANDIANT/event-poll.git
cd event-poll

# 2. Install all dependencies (monorepo workspaces installation)
npm install
```

### Database Setup

You have two options to initialize the PostgreSQL database schema:

#### Option A: Running the Server Setup (Recommended)
This runs the lightweight schema directly used by the server:
```bash
cd server
node init-db.js
cd ..
```

#### Option B: Running the Structured Database Setup with Seed Data
This runs the strict schema (including table constraints/foreign keys) and loads demo records:
```bash
cd database
node init-db.js
cd ..
```

### Start Development

Run this command from the root workspace to launch the frontend React server (on port 3000) and the backend Express server (on port 8080) concurrently:
```bash
npm start
```

> 💡 **Vite Dev Server Proxying:** The client development server automatically forwards any requests prefixing `/api` or `/socket.io` to `http://localhost:8080` (configured dynamically inside [client/vite.config.js](file:///c:/Event%20poll/Eventpoll/client/vite.config.js)).

---

## ⚙️ Environment Variables

### Server Configuration (`server/.env`)
Create a `.env` file inside the `server/` directory and configure the following variables:

| Variable Name | Required | Example / Description |
|---|---|---|
| `DATABASE_URL` | Yes | `postgresql://postgres:root18@localhost:5432/eventpoll` |
| `PRIMARY_SECRET_KEY` | Yes | `your_jwt_primary_secret` — Used to sign standard authentication payloads |
| `REFRESH_SECRET_KEY` | Yes | `your_jwt_refresh_secret` — Used to sign session refresh payloads |
| `FRONTEND_URL` | Yes | `http://localhost:3000` (or the deployed client domain) — Configures poll share link generator |
| `FIREBASE_DATABASE_URL` | Yes | `https://your-app-default-rtdb.firebaseio.com` — Required to establish connection for live poll streams |

> [!WARNING]
> Ensure each environment variable is set on its own separate line inside the `.env` file. Do not string them together.

### Client Configuration (`client/.env`)
Create a `.env` file inside the `client/` directory for stand-alone production configs:

| Variable Name | Required | Example / Description |
|---|---|---|
| `VITE_API_BASE_URL` | No | `https://your-api-server.vercel.app` (Overwrites the local proxy settings) |

---

## 📡 API Reference

Interactive Swagger documentation is available at:
- **Local Dev Server**: `http://localhost:8080/api-docs`
- **Production Server**: `https://<your-app>.vercel.app/api-docs`

Below are the mapped API endpoints from the controller routing files:

### 🔐 Authentication (`/api/auth`)
Mounted on [server/routes/auth.routes.js](file:///c:/Event%20poll/Eventpoll/server/routes/auth.routes.js):

| Method | Endpoint | Description | Payload Format |
|---|---|---|---|
| `POST` | `/api/auth/signup` | Registers a new user account | `{ "email": "...", "fullName": "...", "password": "..." }` |
| `POST` | `/api/auth/signin` | standard sign-in credentials check | `{ "email": "...", "password": "..." }` |
| `POST` | `/api/auth/google-signin` | Synchronizes Google OAuth identity | `{ "email": "...", "fullName": "..." }` |

### 👤 Profile Details (`/api/user`)
Mounted on [server/routes/user.routes.js](file:///c:/Event%20poll/Eventpoll/server/routes/user.routes.js):

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/user/details` | Retrieve authenticated user's profile information | ✅ Bearer JWT Token |

### 🗳️ Completed Poll Archival (`/api/poll`)
Mounted on [server/routes/poll.routes.js](file:///c:/Event%20poll/Eventpoll/server/routes/poll.routes.js):

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/poll/save-poll` | Archives ended poll details into PostgreSQL | ✅ Bearer JWT Token |
| `GET` | `/api/poll/ended-polls` | Fetches historical completed polls for the user | ✅ Bearer JWT Token |
| `POST` | `/api/poll/polls/votedBy` | Gets specific voter list details for a single option | ✅ Bearer JWT Token |
| `GET` | `/api/poll/download/votedby/:pollId/question/:questionId/option/:optionId` | Streams voter names and emails in `.xlsx` Excel format | ✅ Bearer JWT Token |

### ⚡ Live Firebase Polls (`/api/firebase`)
Mounted on [server/routes/firebase.routes.js](file:///c:/Event%20poll/Eventpoll/server/routes/firebase.routes.js):

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/firebase/create-poll` | Initializes a live poll structure in Firebase DB | ✅ Bearer JWT Token |
| `GET` | `/api/firebase/live-polls` | Lists all currently active polls created by presenter | ✅ Bearer JWT Token |
| `GET` | `/api/firebase/live-poll/:pollId` | Fetches live properties for an active poll | ✅ Bearer JWT Token |
| `POST` | `/api/firebase/vote` | Registers voter answers on active poll options | ✅ Bearer JWT Token |

### 📁 Custom Templates (`/api/template`)
Mounted on [server/routes/template.routes.js](file:///c:/Event%20poll/Eventpoll/server/routes/template.routes.js):

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/template/save-template` | Saves a template schema for future use | ✅ Bearer JWT Token |
| `GET` | `/api/template/get-template/:id` | Loads a single template by ID | ✅ Bearer JWT Token |

---

## 🗄️ Database Schema

Here are the active SQL tables deployed on Neon Postgres/Local instances (as specified in [server/schema.sql](file:///c:/Event%20poll/Eventpoll/server/schema.sql)):

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    fullName VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    userRole VARCHAR(50),
    pollsCreated JSONB DEFAULT '[]',
    templateCreated JSONB DEFAULT '[]',
    pollsAttended JSONB DEFAULT '[]'
);

-- Templates table
CREATE TABLE IF NOT EXISTS templates (
    id SERIAL PRIMARY KEY,
    adminId VARCHAR(255),
    templateName VARCHAR(255),
    topic VARCHAR(255),
    topicImage TEXT,
    questions JSONB DEFAULT '[]'
);

-- Completed Polls table (Archived from Firebase Database)
CREATE TABLE IF NOT EXISTS polls (
    id SERIAL PRIMARY KEY,
    pollId VARCHAR(255) UNIQUE,
    adminId VARCHAR(255),
    pollName VARCHAR(255),
    topic VARCHAR(255),
    topicImage TEXT,
    templateName VARCHAR(255),
    questions JSONB DEFAULT '[]',
    pollStatus BOOLEAN DEFAULT TRUE,
    usersAttended JSONB DEFAULT '[]',
    pollCreatedAt VARCHAR(50),
    pollEndsAt VARCHAR(50)
);
```

---

## ☁️ Deployment (Vercel)

VoteSync is fully deployed on **Vercel** — both the React frontend and the Express backend (as a Serverless Function).

### How Vercel Serves This App

```
 Browser
   │
   ▼
 Vercel CDN
   ├── /                    → Serves React build (client/build/)
   ├── /api/*               → Proxied to Express (api/index.js → server/index.js)
   └── /api-docs            → Swagger UI (served by Express)
```

The `/api` directory contains a single `index.js` that imports and re-exports the full Express app. Vercel treats this as a serverless function that handles all `/api/*` routes.

### Step-by-Step Deployment Guide

#### 1. Prepare Your Repository
```bash
# Make sure your code is committed and pushed to GitHub
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

#### 2. Import to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in.
2. Click **"Add New Project"** → **"Import Git Repository"**.
3. Select your GitHub repository.
4. Set the **Root Directory** to the project root (leave as-is if repo root = project).

#### 3. Configure Build Settings

| Setting | Value |
|---|---|
| **Framework Preset** | `Create React App` |
| **Build Command** | `npm run build` (or `cd client && npm run build`) |
| **Output Directory** | `client/build` |
| **Install Command** | `npm install` |

#### 4. Set Environment Variables

In the Vercel dashboard under **Settings → Environment Variables**, add the environment variables listed in the [Server Configuration](#server-configuration-serverenv) section.

#### 5. Deploy
1. Click **"Deploy"**.
2. Vercel will install dependencies, build the React app, and publish.
3. Done! Your app is live.

#### 6. Redeploy After Changes
```bash
git add .
git commit -m "Your changes"
git push origin main
# Vercel auto-deploys on every push to main
```

---

## 🔧 Vercel Configuration

The `vercel.json` file in the root coordinates serverless routing. The key rule routes all `/api/*` traffic to the Express serverless function:

```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api" }
  ]
}
```

The `api/index.js` file is the Vercel serverless entry point:

```js
// api/index.js
const app = require("../server/index.js");
module.exports = app;
```

> 💡 The React app is served as static files. All `/api/*` calls made by the frontend are automatically forwarded to the Express backend.

---

## 🩺 Troubleshooting

### Server Fails to Start Locally

**Problem:** `node index.js` exits immediately with code 1.

**Fix:** Check your `.env` file:
```env
# WRONG — all on one line:
PRIMARY_SECRET_KEY=abc123REFRESH_SECRET_KEY=xyz456

# CORRECT — each on its own line:
PRIMARY_SECRET_KEY=abc123
REFRESH_SECRET_KEY=xyz456
```

### Sign-up / Sign-in Not Working

| Symptom | Cause | Fix |
|---|---|---|
| Button does nothing | Server not running | Run `npm start` from project root |
| Network Error toast | Server down | Restart `server/index.js` |
| "User already exists" | Email taken | Use a different email |
| Redirect doesn't happen | State not updating | Check Redux store for error responses |

### Database Connection Failed

```bash
cd server
node test-db.js
# Should print: Database Connection: SUCCESS
```

If it fails, verify your `DATABASE_URL` in `server/.env` is correct and that your PostgreSQL instance is running.

### Vercel Build Fails

- Ensure `client/build` is the **Output Directory** in Vercel settings.
- Make sure all environment variables are set in Vercel dashboard.
- Check that `npm run build` works locally before deploying.

---

## ⚠️ Known Limitations

- **Live Polls** (create poll, vote, live results) require Firebase Realtime Database credentials. Without them, the `/api/firebase/*` routes are disabled. Sign-in and Sign-up are not affected.
- **Socket.io** real-time features may not work in Vercel's serverless environment (serverless functions are stateless). For full Socket.io support, deploy the server on a persistent host like **Railway**, **Render**, or **Fly.io**.
- **Excel download** works locally. In Vercel's serverless environment, large file streaming may time out after 10 seconds.
- Legacy models (`Polls.model.js` and `Template.model.js`) inside `server/models/` are unused and can be ignored. Active PostgreSQL models are `userModel.js`, `pollModel.js`, and `templateModel.js`.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit: `git commit -m 'Add your feature'`.
4. Push to your branch: `git push origin feature/your-feature-name`.
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <strong>Built with ❤️ using React, Node.js, and PostgreSQL</strong><br/>
  <strong>Deployed ☁️ on Vercel</strong>
</div>
