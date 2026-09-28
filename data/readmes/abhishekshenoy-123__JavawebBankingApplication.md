# Java Banking Application

> A role-based banking web app built with Java Servlets, JSP, and MySQL

![Java](https://img.shields.io/badge/Java-JDK%208%2B-blue?style=flat-square)
![Tomcat](https://img.shields.io/badge/Tomcat-9%2B-orange?style=flat-square)
![MySQL](https://img.shields.io/badge/Database-MySQL-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## Features

| Module | Description |
|---|---|
| Role-based auth | Admin, Manager, Customer access with secure HTTP sessions |
| Full CRUD | Create, read, update, delete for customers, branches & managers |
| Dynamic dashboards | Separate JSP dashboards tailored per role |
| Dual validation | Frontend JSP forms + backend Servlet validation |

---

## Architecture

This project follows an MVC-like pattern:

```
View  →  JSP + HTML/CSS     (dynamic pages, forms, dashboards)
  ↓
Controller  →  Java Servlets  (request handling, business logic, sessions)
  ↓
Model  →  MySQL + JDBC        (persistent data storage)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | JSP, HTML, CSS |
| Backend | Java Servlets (JDK 8+) |
| Database | MySQL |
| Server | Apache Tomcat 9+ |

---

## Project Structure

```
JavaBankingApplication/
├── src/
│   ├── Authentication/
│   │   ├── LoginServlet.java
│   │   └── LogoutServlet.java
│   └── NewUser/
│       ├── AddCustomerServlet.java
│       ├── AddManagerServlet.java
│       ├── AdminServlet.java
│       ├── CustomerOperationServlet.java
│       ├── ReportServlet.java
│       └── UpdateCustomerServlet.java
└── WebContent/
    ├── index.jsp
    ├── login.jsp
    ├── AdminDashboard.jsp
    ├── ManagerDashboard.jsp
    ├── CustomerDashboard.jsp
    ├── AddCustomer.jsp
    ├── CreateBranch.jsp
    ├── UpdateCustomer.jsp
    └── WEB-INF/
        └── web.xml
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/JavaBankingApplication.git
cd JavaBankingApplication
```

### 2. Set up the database

```sql
CREATE DATABASE banking_db;
```

Update JDBC credentials in your connection class:

```java
String url  = "jdbc:mysql://localhost:3306/banking_db";
String user = "root";
String pass = "your_password";
```

### 3. Deploy to Tomcat

Open the project in Eclipse / STS as a **Dynamic Web Project**, add Apache Tomcat 9+, and deploy.

### 4. Open in browser

```
http://localhost:8080/JavaBankingApplication
```

---

## Prerequisites

- Java JDK 8 or higher
- Apache Tomcat 9+
- MySQL Server
- Eclipse IDE or Spring Tool Suite (STS)

---

## License

This project is open source and available under the [MIT License](LICENSE).
