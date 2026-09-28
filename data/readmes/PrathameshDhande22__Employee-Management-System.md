# Employee Management System In Java Swing

![GitHub repo size](https://img.shields.io/github/repo-size/prathameshdhande22/Employee-Management-System?color=brown&logo=github&style=flat-square) &nbsp;
![IDE](https://img.shields.io/badge/IDE-Eclipse%202022--12-yellowgreen?logo=eclipse&style=flat-square) &nbsp;
![Language](https://img.shields.io/badge/Language-Java-blue?logo=java&style=flat-square) &nbsp;
![GitHub](https://img.shields.io/github/license/Prathameshdhande22/Employee-Management-System?logo=github)

This is a Java Swing application for managing employee information. This project was created using JDK 17 and Eclipse 2022-12.

It has the following functionalities:

**Add employee:** Allows you to add a new employee to the system by entering their personal and employment details. <br/>
**Delete employee:** Allows you to delete an existing employee from the system. <br/>
**Update employee:** Allows you to update the personal and employment details of an existing employee. <br/>
**Display employee:** Shows a list of all employees in a JTable, with their personal and employment details.

# Classes :

The application consists of the following classes:

**CreateConnection:** This class is responsible for establishing a connection with a database using JDBC. Edit the CreateConnection.java file to provide your database details. <br/>
**Operations:** This class contains methods for inserting, deleting, and updating employee records in the database. <br/>
**Query:** This class contains methods for retrieving employee records from the database. <br/>
**Windows:** This is the main GUI class, which handles user interactions and displays the employee information in a JTable. <br/>
**Employee:** This class stores the personal and employment details of a single employee. <br/>

# Prerequisites

**MySQL database:** The application uses a MySQL database to store employee records. The SQL script in [Resources/Script.sql](Resources/Script.sql) creates the required database, tables, and function.

**MySQL Connector library:** Add the MySQL connector JAR file from [Resources](Resources) to your project classpath or IDE libraries. This library is required to establish a connection with the MySQL database using JDBC.

# How to run the application :

1. Clone the repository to your local machine.
2. Open the project in an IDE such as Eclipse or IntelliJ.
3. Start MySQL and import the SQL script from [Resources/Script.sql](Resources/Script.sql) to create the database schema.
4. If you are using a locally installed MySQL server, make sure the MySQL service is running and that you have created the database and tables either by importing the script or by running the SQL manually.
5. Open the database connection class and update the URL, username, and password to match your local MySQL setup.
6. Add the connector JAR from [Resources](Resources) to your project libraries or classpath.
7. Build and run the main Java class from your IDE.
8. The application will open in a new window. Follow the prompts to add, delete, update, or display employees.

# Demo :

Demo Of this Project is Uploaded on Youtube. <br/>
Click Here 👉 [Youtube Link](https://youtu.be/8Mv5mN37nJM)

## Note :

This application is just a basic example of how to build an employee management system using Java Swing. You can modify and expand upon the code to add additional features and functionality as needed.

## Author : Prathamesh Dhande
