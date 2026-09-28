# FinTrack

![Java](https://img.shields.io/badge/Java-21-orange)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.x-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![TiDB](https://img.shields.io/badge/Database-TiDB_Cloud-brightgreen)
![Render](https://img.shields.io/badge/Deployment-Render-purple)

### Personal Finance Management Platform

FinTrack is a full-stack web application that helps users manage personal finances through income and expense tracking, budget monitoring, financial analytics, automated reporting, and scheduled notifications.

---

## Live Demo

🌐 Frontend: https://fintrack-app-iz6p.onrender.com

⚙️ Backend API: https://fintrack-v1-kayy.onrender.com/api/v1.0

📘 Swagger Documentation: https://fintrack-v1-kayy.onrender.com/api/v1.0/swagger-ui/index.html

---

## Purpose

Tracking personal finances often involves managing income, expenses, budgets, and spending habits across multiple categories. FinTrack was built to provide a centralized platform that simplifies financial tracking while offering meaningful insights through analytics, reporting, and automated notifications.

---

## Features

* JWT-based authentication with email verification
* Dashboard with financial summaries and visual analytics
* Monthly budget tracking with spending indicators
* Income and expense management
* Custom categories with emoji support
* Transaction filtering and sorting
* Excel report generation and email delivery
* Scheduled financial summary notifications
* Profile image management using Cloudinary
* Swagger API documentation
* Unit testing with JUnit and Mockito

---

## Dashboard & Analytics

The dashboard provides a consolidated view of financial activity, including:

* Monthly budget utilization
* Income, expense, and remaining balance overview
* Recent transactions
* Recent income and expense records
* Pie chart visualization of financial distribution
* Budget threshold indicators

When spending approaches the configured monthly budget limit, the application highlights the budget status to improve spending awareness.

---

## Reports & Notifications

Users can generate financial reports for income and expenses.

Reports can be:

* Downloaded as Excel files
* Delivered directly through email

The application also includes a scheduled notification service that generates and sends daily financial summaries through email using Spring Scheduler. This functionality was implemented and tested in local environments.

---

## Tech Stack

| Layer         | Technologies                      |
| ------------- | --------------------------------- |
| Frontend      | React, Vite, Tailwind CSS         |
| Backend       | Spring Boot, Spring Security, JWT |
| Database      | TiDB Cloud / MySQL                |
| Integrations  | Brevo SMTP, Cloudinary            |
| Documentation | Swagger OpenAPI                   |
| Testing       | JUnit 5, Mockito                  |
| Deployment    |  Render                           |

---

## Architecture

FinTrack follows a client-server architecture where a React frontend communicates with secured Spring Boot REST APIs using JWT authentication. Financial data is stored in TiDB Cloud, while Brevo SMTP is used for email verification, report delivery, and scheduled notifications. Cloudinary is used for profile image management, and Swagger provides interactive API documentation.

---

## Application Workflow

1. Register an account and verify email.
2. Log in securely using JWT authentication.
3. Configure income and expense categories.
4. Record financial transactions.
5. Monitor budgets and financial activity through the dashboard.
6. Filter and review transaction history.
7. Download or email financial reports.
8. Receive automated financial summaries through scheduled notifications.

---
## Screenshots

### Landing Page

![Landing Page](screenshots/landingpage.jpeg)

---

### Authentication

![Authentication](screenshots/signuplogin.jpeg)

---

### Dashboard & Financial Overview

![Dashboard](screenshots/dashboard.png)

---

### Category Management

![Category Management](screenshots/category.jpeg)

---

### Income & Expense Tracking

![Income & Expense Tracking](screenshots/income.jpeg)

---

### Transaction Filtering & Sorting

![Transaction Filtering](screenshots/filter.jpeg)

---

### Scheduled Email Notification

![Scheduled Email Notification](screenshots/notification.jpeg)

---

### Swagger Documentation

![Swagger Documentation](screenshots/swagger-docs.jpeg)


## Local Setup

### Clone Repository

```bash
git clone https://github.com/matlanidimple26/FinTrack.git
```

### Frontend Setup

```bash
cd fintrackfrontend
npm install
npm run dev
```

### Backend Setup

```bash
cd fintrackbackend
./mvnw spring-boot:run
```

---

## Environment Variables

Configure the following environment variables before running the application.

```properties
# Database
spring.datasource.url=${DB_URL}
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}

# Mail
spring.mail.host=${MAIL_HOST}
spring.mail.port=${MAIL_PORT}
spring.mail.username=${MAIL_USERNAME}
spring.mail.password=${MAIL_PASSWORD}
spring.mail.properties.mail.smtp.from=${MAIL_FROM}

# JWT
jwt.secret=${JWT_SECRET}

# Cloudinary
cloudinary.cloud-name=${CLOUDINARY_CLOUD_NAME}
cloudinary.api-key=${CLOUDINARY_API_KEY}
cloudinary.api-secret=${CLOUDINARY_API_SECRET}

# URLs
money.manager.frontend.url=${FRONTEND_URL}
app.activation.url=${BACKEND_URL}
```

### Required Services

* TiDB Cloud / MySQL
* Brevo SMTP
* Cloudinary

---

## Testing

Unit tests were implemented using JUnit 5 and Mockito.

Covered modules include:

* Category Service
* Income Service
* Notification Service

---

## Future Improvements

* Month-over-Month Income & Expense Comparison
* Spending Trend Analytics
* Financial Goal Tracking
* Recurring Transaction Management
* Budget Forecasting
* PDF Report Generation
* Personalized Financial Insights

---

## Key Learnings

* Spring Security and JWT Authentication
* REST API Design and Documentation
* Database Integration using TiDB Cloud
* Financial Data Modeling
* Email Automation using Brevo SMTP
* Cloudinary Integration
* Excel Report Generation
* Unit Testing with JUnit and Mockito
* Cloud Deployment on Render

---

## Author

**Dimple Matlani**

Computer Engineering Student | Full-Stack Developer

