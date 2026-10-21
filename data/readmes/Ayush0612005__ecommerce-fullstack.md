# 🛒 E-Commerce Full-Stack Platform

A production-oriented full-stack e-commerce platform built from the ground up using **Java + Spring Boot** on the backend and **React + TypeScript** on the frontend.

The application implements the complete e-commerce lifecycle — from product discovery and authentication to cart management, coupons, checkout, orders, and protected administration.

🌐 **Live Demo:** [ecommerce-frontend-3oyq.onrender.com](https://ecommerce-frontend-3oyq.onrender.com)
⚙️ **Backend API:** [ecommerce-fullstack-qmt1.onrender.com](https://ecommerce-fullstack-qmt1.onrender.com)
📦 **Repository:** [github.com/Ayush0612005/ecommerce-fullstack](https://github.com/Ayush0612005/ecommerce-fullstack)

---

## ✨ Features

### 👤 Customer Experience

- JWT-based user registration and authentication
- Product catalogue with:
  - Search
  - Category filtering
  - Brand filtering
  - Price filtering
  - Sorting
  - Pagination
- Product detail pages
- Product images, pricing, discounts, and stock information
- Persistent shopping cart
- Wishlist functionality
- Address management
- Checkout flow
- Payment-method selection
- Coupon validation and discount application
- Order placement
- Order history
- Order detail views
- Protected customer routes
- Graceful expired and malformed JWT handling
- Responsive editorial-style interface

### 🛡️ Admin Experience

- Protected admin dashboard
- Admin-only API authorization
- Product management
- Category management
- Order management
- Order status updates
- Coupon management
- Coupon creation and editing
- Coupon activation/deactivation

---

## 🖼️ Screenshots

### Customer Experience

| Homepage | Products | Cart |
|---|---|---|
| ![Homepage](docs/screenshots/homepage.png) | ![Products](docs/screenshots/products.png) | ![Cart](docs/screenshots/cart.png) |

| Checkout | Payment | Order |
|---|---|---|
| ![Checkout](docs/screenshots/checkout.png) | ![Payment](docs/screenshots/payment.png) | ![Order](docs/screenshots/order.png) |

---

# 🏗️ Architecture

```text
                         ┌─────────────────────────┐
                         │      React Frontend     │
                         │  TypeScript + Vite      │
                         │  React Query + Axios    │
                         └────────────┬────────────┘
                                      │
                                  HTTP / REST
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │     Spring Boot API     │
                         │          Java           │
                         │                         │
                         │      Controllers        │
                         │           ↓             │
                         │        Services         │
                         │           ↓             │
                         │     Repositories/JPA    │
                         └────────────┬────────────┘
                                      │
                                  JDBC / JPA
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      MySQL / TiDB       │
                         │      Relational DB      │
                         └─────────────────────────┘
```

### Request Flow

```text
React UI
   ↓
React Query
   ↓
Axios API Client
   ↓
Spring Security + JWT
   ↓
REST Controller
   ↓
Service Layer
   ↓
Spring Data JPA
   ↓
MySQL / TiDB
```

The backend follows a layered architecture separating controllers, business services, repositories, entities, DTOs, and security components.

---

## 🧰 Tech Stack

### Frontend

| Technology | Purpose |
|---|---|
| React | UI development |
| TypeScript | Type-safe frontend development |
| Vite | Development and production build tooling |
| React Router | Client-side routing |
| TanStack React Query | Server-state management and API caching |
| Axios | HTTP client |
| Lucide React | UI icons |
| CSS | Responsive and editorial-style interface |

### Backend

| Technology | Purpose |
|---|---|
| Java | Backend programming language |
| Spring Boot | Backend application framework |
| Spring Security | Authentication and authorization |
| JWT / JJWT | Stateless authentication |
| Spring Data JPA | Data persistence |
| Hibernate | ORM |
| MySQL / TiDB | Relational database |
| Maven | Dependency management and builds |
| Swagger / OpenAPI | API documentation |

---

## 📦 Core Modules

**Authentication**
- User registration
- User login
- JWT generation and validation
- Password hashing
- Protected routes
- Role-based authorization
- Expired-token handling

**Products**
- Product catalogue
- Product details
- Search
- Category filtering
- Brand filtering
- Price filtering
- Sorting
- Pagination
- Stock management
- Product images
- Discount pricing

**Cart**
- Add products
- Update quantities
- Remove products
- Persistent cart
- Cart total calculation
- Stock validation

**Addresses**
- Add addresses
- Update addresses
- Delete addresses
- Address type management
- Default address handling

**Checkout & Orders**
- Address selection
- Payment-method selection
- Coupon application
- Order creation
- Order history
- Order details
- Order status tracking

**Coupons**
- Coupon creation
- Coupon editing
- Coupon activation/deactivation
- Expiry handling
- Eligibility validation
- Discount calculation
- Backend-side coupon validation

**Wishlist**
- Add products to wishlist
- Remove products from wishlist
- Wishlist persistence

**Administration**
- Admin dashboard
- Product management
- Category management
- Order management
- Order status updates
- Coupon management
- Protected admin APIs

---

## 🎟️ Coupon System

Coupon validation is handled by the backend rather than relying on frontend-only calculations.

```text
Customer enters coupon
        ↓
POST /api/v1/coupons/validate
        ↓
Backend validates coupon
        ↓
Eligibility + discount calculated
        ↓
Discounted total returned
        ↓
Customer places order
```

The frontend also clears a previously applied coupon when the cart subtotal changes, preventing stale discount previews.

---

## 🔐 Security

The application uses Spring Security with JWT-based stateless authentication.

Security features include:

- JWT authentication
- Password hashing with BCrypt
- Protected customer routes
- Protected admin routes
- Role-based authorization
- Stateless session management
- Public product and category APIs
- Protected customer and administrative APIs
- Graceful expired JWT handling
- Graceful malformed JWT handling
- HTTP 401 Unauthorized responses for invalid authentication
- Environment-based secret and database configuration
- CSRF disabled for the stateless REST API

Sensitive credentials are not committed to the repository.

---

## 🌐 REST API

The backend exposes REST APIs covering the major application domains:

- `/api/auth`
- `/api/products`
- `/api/categories`
- `/api/cart`
- `/api/addresses`
- `/api/orders`
- `/api/payments`
- `/api/coupons`
- `/api/reviews`
- `/api/admin`

Swagger/OpenAPI support is included for API exploration and documentation.

Once the backend is running, API documentation is available through the configured Swagger UI endpoint.

---

## 🚀 Running Locally

### Prerequisites

Make sure the following are installed:

- Java 17+ or the version configured by the backend project
- Node.js
- npm
- MySQL
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Ayush0612005/ecommerce-fullstack.git

cd ecommerce-fullstack
```

### 2. Configure the Database

Create a MySQL database:

```sql
CREATE DATABASE ecommerce_db;
```

Configure the backend using environment variables:

```env
DB_URL=jdbc:mysql://localhost:3306/ecommerce_db
DB_USERNAME=your_mysql_username
DB_PASSWORD=your_mysql_password

JWT_SECRET=your_long_random_secret
JWT_EXPIRATION=86400000
```

Do not commit real credentials to Git.

### 3. Start the Backend

Open a terminal:

```bash
cd ecommerce-backend\ecommerce-backend
```

Run:

```bash
.\mvnw.cmd spring-boot:run
```

The backend runs on:

```text
http://localhost:8080
```

### 4. Start the Frontend

Open another terminal:

```bash
cd ecommerce-frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Vite will display the local frontend URL, typically:

```text
http://localhost:5173
```

---

## ⚙️ Environment Configuration

### Frontend

Create:

```text
ecommerce-frontend/.env.development
```

Example:

```env
VITE_API_BASE_URL=/api
```

For production deployments, configure the API base URL through the hosting platform's environment variables.

Example:

```env
VITE_API_BASE_URL=https://ecommerce-fullstack-qmt1.onrender.com/api
```

### Backend

The backend uses environment variables for production configuration:

- `DB_URL`
- `DB_USERNAME`
- `DB_PASSWORD`
- `JWT_SECRET`
- `JWT_EXPIRATION`
- `PORT`

---

## 🧪 Verification

**Frontend Production Build**
```bash
npm.cmd run build
```

**Backend Build**
```bash
.\mvnw.cmd clean package -DskipTests
```

**Backend Tests**
```bash
.\mvnw.cmd test
```

**Test Compilation**
```bash
.\mvnw.cmd test-compile
```

The authentication layer includes JWT filter testing covering scenarios such as:

- Valid token
- Expired token
- Malformed token
- Missing token

---

## 📁 Project Structure

```text
ecommerce-fullstack/
│
├── ecommerce-backend/
│   └── ecommerce-backend/
│       ├── src/
│       │   ├── main/
│       │   │   ├── java/
│       │   │   │   └── com/ayush/ecommerce_backend/
│       │   │   │       ├── config/
│       │   │   │       ├── controller/
│       │   │   │       ├── dto/
│       │   │   │       ├── entity/
│       │   │   │       ├── exception/
│       │   │   │       ├── mapper/
│       │   │   │       ├── repository/
│       │   │   │       ├── security/
│       │   │   │       └── service/
│       │   │   └── resources/
│       │   │       └── application.properties
│       │   │
│       │   └── test/
│       │
│       ├── pom.xml
│       ├── mvnw
│       └── mvnw.cmd
│
├── ecommerce-frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── types/
│   │   └── styles/
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.*
│
├── docs/
│   └── screenshots/
│       ├── cart.png
│       ├── checkout.png
│       ├── homepage.png
│       ├── order.png
│       ├── payment.png
│       └── products.png
│
└── README.md
```

---

## 🚀 Production Deployment

The application is deployed as separate frontend and backend services.

```text
                    ┌───────────────────┐
                    │   React Frontend  │
                    │      Render       │
                    └─────────┬─────────┘
                              │
                              │ HTTPS / REST
                              ▼
                    ┌───────────────────┐
                    │  Spring Boot API  │
                    │      Render       │
                    └─────────┬─────────┘
                              │
                              │ JDBC
                              ▼
                    ┌───────────────────┐
                    │   TiDB Cloud DB   │
                    │ MySQL-compatible  │
                    └───────────────────┘
```

### Current Production Services

**Frontend**
https://ecommerce-frontend-3oyq.onrender.com

**Backend**
https://ecommerce-fullstack-qmt1.onrender.com

Production configuration uses environment variables for:

- Database connection
- Database credentials
- JWT secret
- JWT expiration
- Frontend API URL
- Server port

---

## 📈 Engineering Highlights

This project was built to go beyond a basic CRUD application and focuses on real-world backend and full-stack engineering concepts.

### Backend
- Layered Spring Boot architecture
- RESTful API design
- DTO-based request/response handling
- Repository pattern with Spring Data JPA
- Hibernate ORM
- JWT authentication
- Spring Security authorization
- Role-based access control
- Global exception handling
- Database relationships
- Transactional business operations
- Pagination and sorting
- Backend-side validation

### Frontend
- Component-based React architecture
- Type-safe TypeScript development
- React Router navigation
- Server-state management with React Query
- Axios API abstraction
- Protected routes
- Authentication state management
- Responsive UI
- Reusable components
- API error handling

### Deployment
- Separate frontend and backend services
- Production environment variables
- Managed cloud database
- Production REST API
- Cloud deployment through Render

---

## 🔮 Future Improvements

Potential future improvements include:

- Advanced admin analytics and dashboards
- Expanded product reviews and ratings UI
- Persistent wishlist improvements
- Product image upload and cloud storage
- Automated CI/CD pipelines
- Comprehensive integration testing
- End-to-end testing
- Structured application logging
- Production monitoring and observability
- Improved caching strategies
- Advanced search capabilities

---

## 👨‍💻 Author

**Ayush Kulshreshtha**

Full-stack developer focused on Java, Spring Boot, React, TypeScript, backend development, data structures & algorithms, and open-source engineering.

🔗 GitHub: [@Ayush0612005](https://github.com/Ayush0612005)
🔗 Repository: [ecommerce-fullstack](https://github.com/Ayush0612005/ecommerce-fullstack)
🌐 Live Project: [E-Commerce Platform](https://ecommerce-frontend-3oyq.onrender.com)

---

### ⭐ If you found this project interesting

Feel free to explore the repository, try the live application, or connect with me.

Built with Java, Spring Boot, React, TypeScript, and MySQL/TiDB.
