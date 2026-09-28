
---

# Advanced Student Management System

A **desktop-based student database management system** built using **Java** with a graphical interface and database connectivity using **MariaDB**.

This system allows administrators to **add, filter, view, and delete student records** through an interactive **GUI application**. The program connects to a relational database using the **MariaDB Java Client** to perform database operations.

The application demonstrates how **GUI applications interact with databases**, which is a fundamental concept in backend development and enterprise software systems.

---

# Project Repository

GitHub

[https://github.com/Abineshabee/Students-Database-Management-System](https://github.com/Abineshabee/Students-Database-Management-System)

---

# Project Overview

The **Advanced Student Management System** provides a graphical interface for managing student records stored in a relational database.
![My Image](./Screenshot%20from%202024-10-14%2017-01-32.png)


Users can:

• Add new student records
• View students in a table
• Filter students by multiple parameters
• Retrieve specific students using ID
• Delete student records
• Connect to a MariaDB database

The project demonstrates **full-stack desktop development using Java GUI and SQL databases**.

---

# System Architecture

The system follows a **three-layer architecture**.

```
User Interface (GUI)
        ↓
Application Logic (Java)
        ↓
Database Layer (MariaDB)
```

Components:

1. GUI Layer – Built using Java Swing
2. Business Logic – Java program logic
3. Database Layer – MariaDB database

---

# Graphical Interface

The program provides an interactive dashboard.

Main sections include:

• Student Information Form
• Student Table View
• Filtering System
• Student Retrieval
• Student Deletion

The interface displays all records in a **table view with multiple columns** such as:

ID
Name
Gender
Age
Year
Section
Course

---

# Features

## Student Record Management

The system supports full record operations:

Add Student
View Students
Get Student by ID
Delete Student

---

# Student Filtering System

The system allows filtering based on multiple parameters.

Filter options include:

• Year
• Gender
• Maximum Age
• Course
• Section

Example:

Filter all **3rd Year CSE students under age 22**.

---

# Student Table Display

All students are displayed in a table containing:

| Field   | Description       |
| ------- | ----------------- |
| ID      | Unique student ID |
| Name    | Student name      |
| Gender  | Male / Female     |
| Age     | Student age       |
| Year    | Academic year     |
| Section | Class section     |
| Course  | Degree program    |

---

# Database Integration

The application connects to a **MariaDB database** using **JDBC**.

Database operations include:

• INSERT student data
• SELECT records
• DELETE records
• FILTER queries

Database driver used:

```
mariadb-java-client-3.4.1.jar
```

---

# Technologies Used

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Java       | Core application development |
| Java Swing | Graphical User Interface     |
| MariaDB    | Database management          |
| JDBC       | Database connection          |
| Linux      | Development environment      |

---

# Project Structure

```
Students-Database-Management-System
│
├── StudentManagementGUI3.java
├── mariadb-java-client-3.4.1.jar
├── database.sql
└── README.md
```

---

# Database Schema

Example table structure:

```sql
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    year VARCHAR(20),
    section VARCHAR(20),
    course VARCHAR(50)
);
```

---

# Program Execution

Compile the program with the MariaDB driver.

```
javac -cp .:mariadb-java-client-3.4.1.jar StudentManagementGUI3.java
```

Run the program:

```
java -cp .:mariadb-java-client-3.4.1.jar StudentManagementGUI3
```

---

# Core Functional Modules

## 1 Add Student

Adds a new student record to the database.

Inputs:

Name
Age
Gender
Year
Section
Course

The data is inserted using SQL:

```
INSERT INTO students VALUES (...)
```

---

# 2 Filter Students

Allows filtering based on multiple criteria.

Example query:

```
SELECT * FROM students
WHERE year='3rd Year'
AND course='CSE'
AND age <= 22
```

---

# 3 Get Student by ID

Retrieves a specific student record.

Example query:

```
SELECT * FROM students WHERE id = ?
```

---

# 4 Remove Student

Deletes a student from the database.

Example query:

```
DELETE FROM students WHERE id = ?
```

---

# GUI Components

The application uses **Java Swing components**.

| Component   | Purpose                 |
| ----------- | ----------------------- |
| JFrame      | Main application window |
| JTable      | Display student data    |
| JTextField  | Input fields            |
| JComboBox   | Dropdown filters        |
| JButton     | Action buttons          |
| JScrollPane | Scrollable table view   |

---

# Example Workflow

Step 1
Start the program.

Step 2
View all students in the table.

Step 3
Add a new student using the form.

Step 4
Apply filters to find specific students.

Step 5
Retrieve student details using ID.

Step 6
Remove students from the database.

---

# Example Student Data

| ID | Name          | Gender | Age | Year     | Section | Course |
| -- | ------------- | ------ | --- | -------- | ------- | ------ |
| 1  | Alice Johnson | Female | 20  | 1st Year | A       | CSE    |
| 6  | Abinesh       | Male   | 22  | 1st Year | A       | IT     |
| 18 | Tharun        | Male   | 20  | 2nd Year | D       | CIVIL  |

---

# Educational Value

This project demonstrates:

• Java GUI application development
• Database connectivity using JDBC
• SQL query execution
• Desktop application architecture
• Real-world CRUD database operations

It is useful for students learning:

• Software engineering
• Database management systems
• Java desktop development

---

# Future Improvements

Possible improvements include:

• Student update feature
• Login authentication system
• Export data to CSV/Excel
• Advanced search filters
• REST API integration
• Web-based version using Spring Boot

---

# Author

Abinesh N

GitHub
[https://github.com/Abineshabee](https://github.com/Abineshabee)

---
