# Elegance & Others Backend

[Live API](https://elegance-and-others-backend.onrender.com)

## Overview
This repository hosts the **Node.js / Express** backend for the Elegance & Others e‑commerce platform. It provides a RESTful API for managing products, carts, orders, and user profiles. The API connects to a PostgreSQL database and handles authentication, validation, and business logic.

## Tech Stack
- **Node.js** with **Express**
- **TypeScript** for type safety
- **PostgreSQL** as the database (managed via Prisma ORM)
- **Jest** for unit testing
- **Docker** for containerised deployment (optional)

## Local Development
```bash
# install dependencies
npm install   # or yarn install

# set environment variables (see .env.example)
cp .env.example .env
# edit .env as needed

# start development server
npm run dev   # or yarn dev
```
The API runs at `http://localhost:5000`.

## Available Scripts
- `npm run dev` – Starts the server in development mode with hot‑reloading.
- `npm run build` – Compiles TypeScript to JavaScript in the `dist/` folder.
- `npm start` – Runs the compiled production server.
- `npm test` – Executes the test suite.

## Deployment on Render
1. Create a **Web Service** on Render.
2. Connect the repository and set the **Build Command** to `npm install && npm run build`.
3. Set the **Start Command** to `npm start`.
4. Add required environment variables (`DATABASE_URL`, `JWT_SECRET`, etc.) in the Render dashboard.
5. Enable **Auto‑Deploy** for automatic updates on push.

## Environment Variables
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string. |
| `JWT_SECRET` | Secret key for JWT authentication. |
| `PORT` | Port number the server listens on (default `5000`). |
| `VITE_FRONTEND_URL` | URL of the frontend site (e.g., `https://elegance-and-others.onrender.com`). |

## License
MIT © Elegance & Others
