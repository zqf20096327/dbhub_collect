# Grocery Store Website – Complete E-commerce Platform

A full-stack grocery delivery platform with **42+ products**, **user authentication**, **admin dashboard**, and **smart analytics**.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-red.svg)

---

# Project Overview

A complete **Full-Stack E-commerce Website** for fresh and organic grocery products. Users can browse products, add to cart, place orders with delivery slots, write verified reviews, manage wishlist, and track orders.

The admin panel provides full control over products, orders, customers, analytics, and revenue tracking.

* **Total Code:** ~5900+ lines  
* **API Endpoints:** 50+  
* **Database Tables:** 12+  

---

## 📸 Screenshots

### 🏠 Homepage
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/home.png?raw=true)

### 🛍️ Products
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/products.png?raw=true)

### 📂 Categories
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/categories.png?raw=true)

### ⭐ Features
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/features.png?raw=true)

### 🎯 Smart Picks
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/smart%20pics%20.png?raw=true)

### ⭐ Reviews
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/reviews.png?raw=true)

### ✅ Why Choose Us
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/why%20choose%20us%20.png?raw=true)

### ❤️ Wishlist
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/wishlist.png?raw=true)

### 📧 Newsletter
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/newsletter.png?raw=true)

### 🦶 Footer
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/footer.png?raw=true)

### 📝 Blogs
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/Blogs.png?raw=true)

### 👤 User Dashboard
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/user-dashboard.jpeg?raw=true)

### 👨‍💼 Admin Dashboard
![](https://github.com/Sara12-2/Grocery_Store_Website-/blob/main/frontend/images/dashboard.jpeg?raw=true)

---

# Features

## User Features

| Feature               | Description                                             |
| --------------------- | ------------------------------------------------------- |
| Authentication        | Session-based login/register with bcrypt                |
| Product Browsing      | 42+ products with 6 categories                          |
| Search & Filter       | Real-time product search + category filter              |
| Price Sorting         | Low to High / High to Low                               |
| Shopping Cart         | Add/update/remove items with quantity controls          |
| Wishlist              | Save favorite products                                  |
| Reviews & Ratings     | 5-star system with Verified Purchase badge              |
| Order Placement       | Delivery slot selection                                 |
| Payments              | COD, Credit/Debit Card, UPI                             |
| User Dashboard        | Order history, profile editing                          |
| Smart Recommendations | AI-based recommendations                                |
| One-click Reorder     | Instantly reorder previous purchases                    |

## Admin Features

| Feature            | Description                                          |
| ------------------ | ---------------------------------------------------- |
| Dashboard          | Real-time stats for users, products, orders, revenue |
| Revenue Charts     | Monthly revenue analytics with Chart.js              |
| Product Management | Complete CRUD operations                             |
| Order Management   | Multi-status order workflow                          |
| User Management    | View and delete customers                            |
| Product Analytics  | Weekly, monthly & yearly insights                    |
| User Activity      | Active users tracking                                |
| Customer Frequency | Purchase frequency analysis                          |

---

## Security Features

* bcrypt password hashing  
* Account lockout after 5 failed login attempts  
* Login attempt logging with IP tracking  
* Session-based authentication  
* Secure cookies & proper CORS configuration  
* SQL Injection protection using parameterized queries  
* Stock validation before order placement  
* Transaction rollback support on errors  

---

# Tech Stack

| Component      | Technology                      |
| -------------- | ------------------------------- |
| Backend        | Python Flask                    |
| Frontend       | HTML5, CSS3, Vanilla JavaScript |
| Database       | MySQL                           |
| Authentication | Session-based Authentication    |
| Charts         | Chart.js                        |
| Icons          | Font Awesome 6                  |
| Fonts          | Google Fonts (Poppins)          |

---

# Database Schema

| Table          | Description                         |
| -------------- | ----------------------------------- |
| users          | User accounts with bcrypt passwords |
| products       | Product details, stock & categories |
| cart           | Shopping cart items                 |
| orders         | Order details & statuses            |
| order_items    | Individual order products           |
| wishlist       | Saved products                      |
| reviews        | Product ratings & reviews           |
| addresses      | User delivery addresses             |
| login_attempts | Failed login security logs          |

---

# Products by Category

| Category   | Count |
| ---------- | ----- |
| Fruits     | 12    |
| Vegetables | 12    |
| Dairy      | 6     |
| Meat       | 4     |
| Bakery     | 4     |
| Organic    | 4     |
| Total      | 42    |

---

# Installation & Setup

## Prerequisites

* Python 3.11+
* MySQL Server
* Git

## Step 1: Clone Repository

```bash
git clone https://github.com/Sara12-2/Grocery_Store_Website-.git
cd Grocery_Store_Website-
```
---

## Step 2: Backend Setup
```bash
cd Backend

python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install flask flask-cors mysql-connector-python python-dotenv bcrypt
```
## Step 3: Environment Variables

Create a .env file inside Backend:
```bash
SECRET_KEY=your-strong-secret-key-here
DB_HOST=localhost
DB_NAME=grocery_store
DB_USER=root
DB_PASSWORD=your_database_password_here
```
⚠️ Never commit .env file.

## Step 4: Database Setup
```bash 
CREATE DATABASE grocery_store;
USE grocery_store;
Step 5: Import Database Schema
mysql -u root -p grocery_store < database/schema.sql
```
---

## Step 6: Start Backend Server
```bash
python app.py
```
## Step 7: Open Browser
```bash 
http://localhost:5001
```

## Project Structure
```bash
Grocery Store Website/
│
├── Backend/
│   ├── app.py
│   ├── .env
│   ├── routes/
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   ├── admin.py
│   │   ├── user.py
│   │   └── reviews.py
│   └── utils/
│       └── database.py
│
├── frontend/
│   ├── index.html
│   ├── admin_dashboard.html
│   ├── user-dashboard.html
│   ├── style.css
│   ├── script.js
│   ├── admin.js
│   ├── user-dashboard.js
│   └── images/
│
└── README.md
```
## API Endpoints Overview

| Module   | Endpoints |
|----------|----------|
| Auth     | /api/auth/login, /register, /logout |
| Products | /api/products, /categories |
| Cart     | /api/cart, /add, /update |
| Orders   | /api/orders, /place |
| Admin    | /api/admin/dashboard |
| User     | /api/user/profile |
| Reviews  | /api/reviews/add |

---

## Challenges Solved

| Challenge | Solution |
|----------|----------|
| Session persistence with CORS | Secure cookie settings |
| Cart restoration after login | sessionStorage |
| Verified purchase reviews | Order history validation |
| Transaction safety | MySQL rollback |
| Stock management | Deduct after order |
## Future Improvements

- Email notifications  
- Stripe/Razorpay integration  
- Product return/refund system  
- Live order tracking  
- Discount coupons  
- WhatsApp notifications  
- Out-of-stock alerts  
- Multi-language support  

---

## Acknowledgments

- Flask  
- Chart.js  
- Font Awesome  
- Google Fonts  
- Open Source Community  

