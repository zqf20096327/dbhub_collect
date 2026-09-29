# ReCart 🛒

A full-stack e-commerce web application built with **React, Flask, SQLAlchemy, and TiDB Cloud**.

ReCart provides a complete shopping experience with user authentication, product browsing, search and filtering, cart management, wishlist, product comparison, checkout, and order management.

---

## 🚀 Live Project

**Frontend:**  
https://re-cart-gilt.vercel.app/

**Backend API:**  
https://recart-backend-kuem.onrender.com/

**Database:** TiDB Cloud

---

## ✨ Features

### 🛍️ Product Browsing

- Browse products from the DummyJSON Product API
- Dynamic product categories
- Product details page
- Product search
- Category filtering
- Price range filtering
- Sorting by:
  - Latest
  - Popularity
  - Rating
- Grid and list product views
- Pagination

### ❤️ Wishlist

- Add products to wishlist
- Remove products from wishlist
- Backend-persistent wishlist
- Authentication-based wishlist management

### ⚖️ Product Comparison

- Add products to comparison
- Compare product information
- Remove products from comparison

### 🛒 Shopping Cart

- Add products to cart
- Increase/decrease quantity
- Remove products
- Quantity-aware product addition
- Automatic cart totals
- Checkout navigation

### 🔐 Authentication

- User registration
- User login
- JWT-based authentication
- Protected routes
- Current-user verification
- Logout functionality
- Account page

### 💳 Checkout

- Billing address
- Optional shipping address
- Order summary
- Payment method selection
- Order validation
- Order placement

### 📦 Order Management

- Order creation
- Order success page
- Order history
- Order details
- Order cancellation
- Persistent order data

### 🔔 Notifications

Reusable notification system for:

- Success messages
- Error messages
- Validation messages
- Cart actions
- Authentication feedback

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   React + Vite      │
                    │     Frontend        │
                    │      Vercel         │
                    └──────────┬──────────┘
                               │
                               │ REST API
                               ▼
                    ┌─────────────────────┐
                    │   Flask Backend     │
                    │      REST API       │
                    │       Render        │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌────────────────┐            ┌────────────────┐
       │   SQLAlchemy   │            │   JWT Auth     │
       └───────┬────────┘            └────────────────┘
               │
               ▼
       ┌────────────────┐
       │   TiDB Cloud   │
       │ MySQL Compatible│
       └────────────────┘

               External API
                    │
                    ▼
       ┌────────────────────┐
       │     DummyJSON      │
       │   Product Catalog  │
       └────────────────────┘
```

---

## 🧰 Tech Stack

### Frontend

- React
- Vite
- React Router
- Bootstrap
- JavaScript
- Axios

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- PyMySQL
- Gunicorn

### Database

- TiDB Cloud
- MySQL-compatible database

### External API

- DummyJSON Product API

### Deployment

- Vercel — Frontend
- Render — Backend
- TiDB Cloud — Database

---

## 📁 Project Structure

```text
ReCart/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── auth.py
│   │   ├── orders.py
│   │   └── wishlist.py
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── .env.example
│
├── .gitignore
└── README.md
```

---

## 🔐 Authentication Flow

ReCart uses JWT-based authentication.

```text
User
 │
 ├── Register
 │      ↓
 │   Flask API
 │      ↓
 │   Password Hash
 │      ↓
 │   TiDB
 │
 └── Login
        ↓
     Flask API
        ↓
     JWT Token
        ↓
     React AuthContext
        ↓
     Protected Routes
```

Protected features include:

- Account
- Checkout
- Orders
- Order Details
- Order Success
- Wishlist management

---

## 🛒 Order Flow

```text
Product
   ↓
Add to Cart
   ↓
Cart
   ↓
Checkout
   ↓
Place Order
   ↓
Flask REST API
   ↓
TiDB Cloud
   ↓
Order Created
   ↓
Order Success
   ↓
Order History
```

---

## 🌐 API Endpoints

### Authentication

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Orders

```text
POST   /api/orders
GET    /api/orders
GET    /api/orders/<order_id>
PUT    /api/orders/<order_id>/cancel
```

### Wishlist

```text
GET    /api/wishlist
POST   /api/wishlist
DELETE /api/wishlist/<product_id>
```

### Database Test

```text
GET /api/test-db
```

---

## ⚙️ Environment Variables

### Backend

Create:

```text
backend/.env
```

```env
DATABASE_URL=your_database_connection_string
JWT_SECRET_KEY=your_jwt_secret
```

### Frontend

Create:

```text
frontend/.env
```

```env
VITE_API_URL=http://127.0.0.1:5000
```

For production, the Vercel environment variable points to the deployed Render backend.

> Environment files containing secrets are excluded from Git using `.gitignore`.

---

## 🧪 Testing

The application has been tested across the major user flows, including:

- User registration
- User login
- JWT authentication
- Logout and re-login
- Product browsing
- Product search
- Category filtering
- Price filtering
- Sorting
- Cart management
- Wishlist persistence
- Product comparison
- Checkout
- Order creation
- Order history
- Order details
- Order cancellation
- Authentication validation
- Duplicate registration handling
- Invalid login handling
- Database persistence

---

## 🚀 Deployment

### Frontend

The React/Vite frontend is deployed using **Vercel**.

```text
GitHub
   ↓
Vercel
   ↓
React + Vite
```

### Backend

The Flask backend is deployed using **Render** with Gunicorn.

```text
GitHub
   ↓
Render
   ↓
Gunicorn
   ↓
Flask
```

### Database

The application uses **TiDB Cloud**, a MySQL-compatible cloud database.

```text
Flask
  ↓
SQLAlchemy
  ↓
PyMySQL
  ↓
TiDB Cloud
```

---

## 🔒 Security

- Passwords are hashed before storage
- JWT authentication is used for protected API routes
- Database credentials are stored in environment variables
- JWT secret is stored in an environment variable
- `.env` files are excluded from Git
- Production frontend/backend communication uses HTTPS

---

## 📌 Future Improvements

Potential improvements include:

- Online payment integration
- Admin dashboard
- Product management
- Order management dashboard
- User profile editing
- Product reviews and ratings
- Advanced product recommendations
- Improved responsive design
- Image optimization
- Production monitoring and logging

---

## 👨‍💻 Project

**ReCart** — Full-Stack E-Commerce Application

Built using **React + Flask + SQLAlchemy + TiDB Cloud**.

---

⭐ If you find this project useful, consider giving the repository a star.