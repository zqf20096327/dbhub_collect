<h1 align="center">Library Management System</h1>

<p align="center">
  <img 
    src="https://readme-typing-svg.herokuapp.com?size=36&duration=3000&color=1A81E2&center=true&vCenter=true&width=800&lines=Developed+By;Nojaid+Ad"
    alt="Developed By"
  />
</p>

---

## DESCRIPTION
The **Library Management System** is a **Java Swing desktop application** developed using **NetBeans IDE**.  
The project provides basic library operations for managing **users** and **books** without authentication (no login or registration).

The system allows the librarian to:
- Add, update, delete, and view users
- Add, update, delete, and view books
- Manage books using **ISBN**
- Display all users and all books in table format

The application uses **SQLite** as a lightweight local database and connects via the **SQLite JDBC Driver**.

---

## TECHNOLOGIES USED
- Java (JDK 8 or higher)
- Java Swing (GUI)
- NetBeans IDE
- SQLite Database
- SQLite JDBC Driver

---

## PROJECT FEATURES

### User Management
- Add new users  
- Update user information  
- Delete users  
- View all users in a tables

### Book Management
- Add new books  
- Update book information  
- Delete books  
- Search and manage books using **ISBN**  
- View all books in a table  

### General
- No login or registration system  
- Simple and clean Swing-based GUI  
- Local database using SQLite  

---

## DATABASE DETAILS

### Tables
- **Users Table**
  - user_id
  - name
  - email
  - phone

- **Books Table**
  - book_id
  - title
  - author
  - isbn
  - quantity

---

## REQUIREMENTS
- Java JDK 8 or higher  
- NetBeans IDE  
- SQLite  
- SQLite JDBC Driver  

---

## HOW TO RUN THE PROJECT

1. **Open the Project**
   - Open NetBeans IDE
   - Open the project folder

2. **Add SQLite JDBC Driver**
   - Add `sqlite-jdbc.jar` to project libraries

3. **Database Setup**
   - SQLite database file is stored locally
   - Tables are created automatically or via SQL file (if provided)

4. **Run the Application**
   - Run the main JFrame file
   - The Library Management System GUI will appear

---

