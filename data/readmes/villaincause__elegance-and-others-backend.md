# Elegance & Others – Backend API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

This is the **backend** for the *Elegance & Others* e‑commerce store. It is built with **Node.js**, **Express**, and **MySQL** via **TiDB Cloud**. The API serves product, user, order, and search data to the frontend, and handles image uploads directly to **Cloudinary**.

- **Database**: TiDB Cloud (MySQL‑compatible) – see `.env` for connection details.
- **Image storage**: Cloudinary (folder `elegance-and-others`).
- **Authentication**: JWT based login/registration.
- **CORS**: Configured to allow the deployed frontend and local development.

✅ Live API endpoint: <https://elegance-and-others-backend.onrender.com>

## Quick Start (local development)

```bash
# 1️⃣ Clone the repo
git clone https://github.com/villaincause/elegance-and-others-backend.git
cd elegance-and-others-backend

# 2️⃣ Install dependencies
npm install

# 3️⃣ Create a .env file (see below for required keys)
cp .env.example .env   # if an example exists, otherwise create manually

# 4️⃣ Run the server (development with hot‑reload)
npm run dev   # uses nodemon, listens on $PORT (default 5000)
```

### .env variables
```
DB_HOST=your-tidb-host
DB_PORT=4000
DB_USER=your-db-user
DB_PASSWORD=your-db-pass
DB_NAME=elegance_db

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
CLOUDINARY_FOLDER=elegance-and-others

# Optional – Render will inject PORT automatically
# PORT=5000

# Frontend URL for CORS (used in production)
CLIENT_URL=https://elegance-and-others.onrender.com
```

## Scripts

| Script | Description |
|--------|-------------|
| `npm start` | Starts the server (uses `node index.js`). |
| `npm run dev` | Starts the server with **nodemon** for live reload. |
| `npm test` | Placeholder – add your tests here. |

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products` | List all products. |
| `GET` | `/api/products/:id` | Get a single product. |
| `POST` | `/api/auth/register` | Register a new user. |
| `POST` | `/api/auth/login` | Login and receive a JWT. |
| `POST` | `/api/orders` | Create a new order (authenticated). |
| `GET` | `/api/search?q=...` | Search products. |
| `POST` | `/api/addresses` | Add a user address. |
| `GET` | `/api/addresses/:userId` | Get addresses for a user. |

> The API returns image URLs that point directly to Cloudinary, so the frontend never serves static files from the backend.

## Deployment (Render)

1. **Create a Web Service** in Render and connect this repository.
2. **Build command**: `npm install`
3. **Start command**: `node index.js`
4. Add the environment variables from the `.env` section above (Render will inject `$PORT`).
5. Set `CLIENT_URL` to the frontend URL (`https://elegance-and-others.onrender.com`).

After deployment, the live API is reachable at the URL shown at the top of this file.

---

© 2024‑2026 Elegance & Others – Open‑source under the MIT License.

