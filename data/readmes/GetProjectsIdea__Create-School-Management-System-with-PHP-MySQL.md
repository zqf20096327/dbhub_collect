# 🏫 School Management System (PHP & MySQL)

<div align="center">

[![Tutorial](https://img.shields.io/badge/Full%20Tutorial-GetProjects.org-4F46E5?style=for-the-badge&logo=googlechrome&logoColor=white)](https://getprojects.org/create-school-management-system-with-php-mysql/)
[![PHP](https://img.shields.io/badge/PHP-7.4%20%2F%208.x-777BB4?style=for-the-badge&logo=php&logoColor=white)](https://www.php.net/)
[![Database](https://img.shields.io/badge/Database-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<br/>

**A complete academic administration portal developed in PHP and MySQL for schools and colleges, featuring Student Information Management, Teacher Allocation, Class & Subject Rosters, and Attendance Logs.**

</div>

---

> 📖 **Read Full Setup Guide & Download**: [Complete School Management System Tutorial on GetProjects.org](https://getprojects.org/create-school-management-system-with-php-mysql/)

---

## 📋 Features & Functionalities
- 👨‍🎓 **Student Management**: Full CRUD operations for student admission, roll numbers, personal records, and section assignments.
- 👩‍🏫 **Teacher Directory**: Assign teachers to subjects and class schedules.
- 📚 **Classes & Subjects**: Flexible class levels, subject curriculums, and section mapping.
- 📅 **Attendance Tracking**: Daily student attendance logging with monthly reporting.
- 🔐 **Role-Based Authentication**: Secure login access for administrators and faculty.

---

## 🚀 Installation & Localhost Setup (XAMPP / WAMP)

### 1. Clone or Download Project
```bash
git clone https://github.com/GetProjectsIdea/Create-School-Management-System-with-PHP-MySQL.git
```
Move the project folder into your web root directory (e.g., `htdocs/` in XAMPP or `www/` in WAMP).

### 2. Import the Database
1. Open your browser and navigate to `http://localhost/phpmyadmin`.
2. Create a new database named `sms_db` (or as specified in the config).
3. Click on the **Import** tab and select the `.sql` file located in the `Database/` directory.

### 3. Configure Database Connection
Open `[Source Code] School Management System/config.php` (or database configuration file) and verify your MySQL credentials:
```php
$host = "localhost";
$username = "root";
$password = "";
$dbname = "sms_db";
```

### 4. Launch Application
Navigate to `http://localhost/Create-School-Management-System-with-PHP-MySQL/` in your browser.

---

## 🎓 Academic Submission & Viva Notes
- **Frontend**: Clean responsive HTML5, CSS3, JavaScript, and Bootstrap UI.
- **Backend**: Native PHP with PDO / MySQLi prepared statements preventing SQL injection vulnerabilities.
- **Database Schema**: Fully normalized tables (Students, Teachers, Classes, Attendance, Users) ideal for final-year ER diagrams.

---

<div align="center">

Maintained by **[GetProjects.org](https://getprojects.org)** • Curated by [@pardeeppatel](https://github.com/pardeeppatel)

</div>
