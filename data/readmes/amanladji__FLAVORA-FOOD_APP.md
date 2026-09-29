# 🍽️ FLAVORA – Online Food Delivery Web Application

FLAVORA is a full-stack online food delivery web application developed using Java Servlets, JSP, JDBC, and MySQL following the MVC architecture. The application allows customers to browse restaurants, order food, make secure online payments using Razorpay, and track their order history. It also includes an Admin Panel for managing restaurants and menu items.

---

## 🚀 Features

### 👤 Customer
- User Registration & Login
- Secure Password Hashing (BCrypt)
- Browse Restaurants
- View Restaurant Menus
- Add Items to Cart
- Update Cart Quantity
- Checkout & Place Orders
- Online Payment (Razorpay)
- Cash on Delivery
- Order History
- Logout

### 👨‍💼 Admin
- Admin Login
- Admin Registration (Protected)
- Manage Restaurants
- Add / Update / Delete Menus
- View Customer Orders
- Dashboard

---

## 💳 Payment Gateway

- Razorpay Java SDK
- Online UPI/Card/Net Banking Payments
- Environment Variable based API Key Management

---

## 🔒 Security

- BCrypt Password Hashing
- PreparedStatement (SQL Injection Prevention)
- Session-Based Authentication
- Environment Variables for API Keys
- DAO Design Pattern
- MVC Architecture

---

## 🛠️ Tech Stack

### Backend
- Java
- Servlets
- JSP
- JDBC

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- MySQL

### Architecture
- MVC Design Pattern
- DAO Design Pattern

### Payment
- Razorpay Java SDK

### Server
- Apache Tomcat 10

### Deployment
- Docker
- Render

---

## 📂 Project Structure

```
FLAVORA-FOODAPP
│
├── src
│   ├── main
│   │   ├── java
│   │   │   ├── Controllers (Servlets)
│   │   │   ├── DAO
│   │   │   ├── DAOImplementation
│   │   │   ├── Models
│   │   │   └── Utility
│   │   │
│   │   └── webapp
│   │       ├── JSP Pages
│   │       ├── HTML Pages
│   │       ├── CSS
│   │       ├── Images
│   │       └── WEB-INF
│
├── Dockerfile
├── FLAVORA-FOODAPP.war
└── README.md
```

---

## 🗄️ Database Tables

- User
- Restaurant
- Menu
- OrderTable
- OrderItem

---

## 📸 Screenshots

- Login Page
- Registration Page
- Restaurant Page
- Menu Page
- Cart
- Checkout
- Razorpay Payment
- Order History
- Admin Dashboard

---

## ⚙️ Environment Variables

Create the following environment variables before running the application.

```
DB_URL=
DB_USERNAME=
DB_PASSWORD=

RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
```

---

## 🐳 Docker

Build Docker Image

```bash
docker build -t flavora .
```

Run Container

```bash
docker run -p 8080:8080 flavora
```

---

## 🌐 Deployment

The project is deployed using:

- Render
- Docker
- Apache Tomcat

---

## 📌 Key Concepts Implemented

- MVC Architecture
- DAO Pattern
- JDBC Connectivity
- Session Management
- BCrypt Password Encryption
- PreparedStatement Security
- Razorpay Payment Gateway Integration
- Dynamic Cart Management
- Order Management

---

## 🔮 Future Enhancements

- Delivery Partner Module
- Restaurant Owner Dashboard
- Live Order Tracking
- Reviews & Ratings
- Coupons & Offers
- Email Notifications
- SMS Notifications
- AI Food Recommendation

---

## 👨‍💻 Author

**Masroor Ahmed Aman**

- GitHub: https://github.com/amanladji?tab=repositories
- LinkedIn: https://www.linkedin.com/in/masroor-ahmed-aman/

---

## ⭐ If you like this project

Give this repository a ⭐ on GitHub.
