# URBANGENTS APPARELS

> Premium menswear e-commerce platform with a luxury editorial aesthetic.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Site-black?style=for-the-badge)](https://urbangents-apparel-eta.vercel.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)](https://react.dev)
[![Node.js](https://img.shields.io/badge/Node.js-Express-339933?style=for-the-badge&logo=node.js)](https://nodejs.org)

---

## 🔗 Live Demo

**[urbangents-apparel-eta.vercel.app](https://urbangents-apparel-eta.vercel.app)**

---

## 📸 Screenshots

<!-- Tip: drag and drop images into this file when editing on GitHub to auto-upload them -->

| Home / Catalog | Product Detail | Admin Dashboard |
|---|---|---|
| <img width="1344" height="655" alt="Screenshot 2026-05-18 011024" src="https://github.com/user-attachments/assets/8e99929e-626f-46e6-a55f-051d8148306b" /> | <img width="1336" height="650" alt="image" src="https://github.com/user-attachments/assets/9cf40cd9-799a-448b-8254-5bdbd94f9a52" /> |<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/1e3a9fee-ad07-4105-9ee0-b798b7891e2e" />



## About

Urbangents Apparels is a full-stack e-commerce platform for premium menswear, built with a modern "Atelier" design aesthetic inspired by high-end streetwear brands. Developed as a final year engineering project, it demonstrates end-to-end product ownership — from database schema design to deployment.

---

## Features

- 🛍️ Dynamic product catalog with editorial asymmetric grid layout
- 🔐 User authentication with JWT + bcrypt and role-based access (shopper & admin)
- 🛒 Persistent shopping cart with size and color selection
- 📦 Admin dashboard with full product CRUD and order management
- 📱 Fully mobile-responsive with smooth CSS animations
- 🌙 Dark-mode luxury design

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS |
| Backend | Node.js, Express.js |
| Database | TiDB (MySQL-compatible, serverless) |
| Auth | JWT + bcrypt |
| Deployment | Vercel |

---

## Getting Started

### Prerequisites

- Node.js v18+
- A MySQL-compatible database instance (TiDB Cloud free tier works)

### 1. Clone the repo

```bash
git clone https://github.com/Engrojkeh/urbangents-apparel.git
cd urbangents-apparel
```

### 2. Set up the backend

```bash
cd backend
cp .env.example .env   # fill in your own environment values
npm install
npm run dev
```

### 3. Set up the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173` and the backend on `http://localhost:5000` by default.

> **Note:** You must supply your own environment variables. See `backend/.env.example` for all required keys. Never commit any `.env` files.

---

## Project Structure

```
urbangents-apparel/
├── backend/              # Express API — auth, products, orders, cart
│   ├── routes/
│   ├── middleware/
│   └── .env.example      # Environment variable template
├── frontend/             # React + Vite app
│   └── src/
│       ├── pages/        # Home, Shop, Cart, Login, Admin, etc.
│       ├── components/   # Navbar and shared UI components
│       └── context/      # CartContext (global state)
├── schema.sql            # Database schema
├── .gitignore
└── README.md
```

---

## License

This project is licensed under the [MIT License](./LICENSE).

---

## Author

**Engrojkeh** — built as a final year engineering project.

Connect: [GitHub](https://github.com/Engrojkeh)
