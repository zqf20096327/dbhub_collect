# MoneyHubSport

<p align="center">
  <strong>Personal Expense Management System</strong>
</p>

<p align="center">
  <a href="#">📦 GitHub</a>
  ·
  <a href="#installation-guide">🚀 Installation</a>
  ·
  <a href="#features">✨ Features</a>
</p>

<p align="center">
<a href="#"><img src="https://img.shields.io/badge/Java-17+-ED8B00?style=flat&logo=java" alt="Java"></a>
<a href="#"><img src="https://img.shields.io/badge/MySQL-8+-4479A1?style=flat&logo=mysql" alt="MySQL"></a>
<a href="#"><img src="https://img.shields.io/badge/NetBeans-IDE-1B6AC6?style=flat" alt="NetBeans"></a>
<a href="#"><img src="https://img.shields.io/badge/Maven-Build-C71A36?style=flat&logo=apachemaven" alt="Maven"></a>
<a href="#"><img src="https://img.shields.io/badge/License-MIT-green" alt="License"></a>
</p>

---

# MoneyHubSport Personal Expense Management System

MoneyHubSport is a desktop-based personal finance and expense management application developed with Java and MySQL.

The system helps users track daily income and expenses, manage personal budgets, categorize transactions, and analyze spending habits through a simple and user-friendly interface.

The project focuses on financial organization, expense tracking, and data reporting for personal finance management.

---

# Core Features

## Transaction Management

* Add income and expense transactions
* Edit and delete transactions
* Manage transaction descriptions
* Track transaction history

## Expense Categories

* Food & Dining
* Entertainment
* Bills & Utilities
* Shopping
* Transportation
* Custom expense categories

## Reports & Analytics

* Daily expense reports
* Monthly financial reports
* Expense statistics by category
* Spending overview dashboard

## Data Export

* Export reports to CSV
* Export reports to PDF
* Backup financial data

## User Authentication

* Multiple user accounts
* Secure login system
* Separate financial management per user

---

# Technology Stack

## Backend

| Technology | Version | Description        |
| ---------- | ------- | ------------------ |
| Java        | 8+      | Main Programming Language |
| MySQL       | 5.7+    | Database System |
| Maven       | Latest  | Dependency Management |

## Development Tools

| Tool        | Description |
| ------------ | ---------------- |
| NetBeans IDE | Java Development Environment |
| MySQL Workbench | Database Management Tool |

---

# System Requirements

Before installation, ensure your system meets the following requirements:

* Java Development Kit (JDK) 8 or higher
* NetBeans IDE 12+
* MySQL Server 5.7+
* Maven
* Windows, macOS, or Linux

---

# Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/scoppy9201/He_thong_quan_ly_chi_tieu.git
cd he-thong-quan-ly-chi-tieu
```

---

## 2. Configure MySQL Database

Create a new database:

```sql
CREATE DATABASE expense_manager;
```

Create database user:

```sql
CREATE USER 'expense_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON expense_manager.* TO 'expense_user'@'localhost';
FLUSH PRIVILEGES;
```

Import database structure:

```bash
mysql -u expense_user -p expense_manager < database_setup.sql
```

---

## 3. Open Project in NetBeans

* Open NetBeans IDE
* Select `File > Open Project`
* Choose the cloned project folder
* Wait for Maven dependencies to install automatically

---

## 4. Configure Database Connection

Update database configuration inside:

```text
src/main/resources/db.properties
```

Configure:

```properties
db.url=jdbc:mysql://localhost:3306/expense_manager
db.username=expense_user
db.password=password
```

---

## 5. Run Application

Run the project directly from NetBeans IDE.

Or using Maven:

```bash
mvn clean install
mvn exec:java
```

---

# Project Structure

```bash
MoneyHubSport
├── src
│   ├── main
│   │   ├── java
│   │   ├── resources
│   │   └── ui
├── database
├── docs
├── reports
└── pom.xml
```

---

# Use Cases

MoneyHubSport is suitable for:

* Personal finance tracking
* Expense management
* Budget planning
* Student finance projects
* Java desktop application learning
* Academic projects

---

# Future Improvements

Upcoming planned features:

* Advanced analytics dashboard
* Budget goals & alerts
* Cloud synchronization
* Mobile companion application
* Multi-currency support
* Dark mode UI

---

# Contributing

Contributions are welcome.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

---

# Author

* Bùi Mạnh Hưng

---

# Contact

* Email: Buimanhhung3105@gmail.com
* GitHub: https://github.com/scoppy9201

---

# License

MIT License

---

# Support

If you like this project, please give it a ⭐ on GitHub!

---

<div align="center">
  Built with ❤️ using Java & MySQL
</div>
