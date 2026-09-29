# 📚 Library Management System API

A robust RESTful API backend built for managing library books, stock, and transactions. Powered by Node.js, Express, and a cloud-hosted MySQL database (TiDB), fully deployed and live on Render.

## 🚀 Live API Endpoint
- **Base URL:** [https://library-api-backend-ej07.onrender.com/api/books](https://library-api-backend-ej07.onrender.com/api/books)

## 🛠️ Tech Stack
- **Runtime:** Node.js
- **Framework:** Express.js
- **Database:** TiDB (Cloud MySQL)
- **Deployment:** Render

## 📡 API Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/books` | Get all books |
| **GET** | `/api/books/:id` | Get a specific book by ID |
| **POST** | `/api/books` | Add a new book |
| **PUT** | `/api/books/:id` | Update book details |
| **DELETE** | `/api/books/:id` | Delete a book |

## ⚙️ Local Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/Pappukumar92/Library-API-Backend.git](https://github.com/Pappukumar92/Library-API-Backend.git)

Install dependencies:
npm install
  
Create a .env file and add your database configurations:
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=test
DB_PORT=4000
PORT=3000

Start the server:
npm run dev
