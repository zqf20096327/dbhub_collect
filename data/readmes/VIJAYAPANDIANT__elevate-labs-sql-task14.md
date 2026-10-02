# 📊 Elevate Lab SQL Task 14: Stored Procedures and User-Defined Functions (UDFs)

A professional SQL project demonstrating the core concepts of MySQL Stored Procedures, User-Defined Functions (UDFs), and Error Handling. It covers creating subroutines to encapsulate complex logic, parameterized inputs/outputs, scalar functions for calculations, and robust error management using exception handlers.

## 📌 Project Objective
The primary goal of this task is to understand how to modularize SQL code for reusability and maintainability. It illustrates how to create and invoke stored procedures for database operations, implement custom scalar functions for data transformation, and safely handle unexpected SQL exceptions during execution.

## 🛠️ Technical Scope
- **Database Management System**: SQL (MySQL)
- **Core Concepts**: Stored Procedures (`CREATE PROCEDURE`), User-Defined Functions (`CREATE FUNCTION`), `DELIMITER`, `CALL`
- **Advanced Techniques**: Parameters (`IN`, `OUT`), Error Handling (`DECLARE CONTINUE HANDLER FOR SQLEXCEPTION`), Deterministic Functions

## 🗄️ Database Schema

### `employees` Table
| Column | Data Type | Constraint / Description |
| :--- | :--- | :--- |
| `emp_id` | INT | Primary Key, Auto-incremented |
| `emp_name` | VARCHAR(100) | Name of the employee |
| `department` | VARCHAR(50) | Department name |
| `salary` | DECIMAL(10,2) | Monthly salary |
| `bonus` | DECIMAL(10,2) | Performance bonus |

## 💻 SQL Implementations
Key operations demonstrated in the script:

- **Database & Schema Setup**: Creation of the `task14` database and the `employees` table.
- **Stored Procedures (IN Parameters)**: Implementation of `add_employee` to insert new employee records using input parameters.
- **Stored Procedures (OUT Parameters)**: Implementation of `get_employee_count` to calculate and return the total number of employees using an output variable.
- **User-Defined Functions (UDFs)**: Creation of deterministic scalar functions:
  - `calculate_tax`: Calculates a 10% tax on a given salary.
  - `total_income`: Computes total earnings by adding salary and bonus.
- **Error Handling in Procedures**: Implementation of `safe_insert_employee` showcasing how to use `DECLARE CONTINUE HANDLER FOR SQLEXCEPTION` to gracefully handle and report errors during `INSERT` operations.

## 🚀 Setup & Execution

- **Initialize**: Execute the script to create the `task14` database and `employees` table.
- **Test Stored Procedures**: Use the `CALL` statement to insert records via `add_employee` and retrieve counts via `get_employee_count`.
- **Test Functions**: Use the `SELECT` statement to query existing employee records while simultaneously invoking `calculate_tax` and `total_income` for computed columns.
- **Test Error Handling**: Execute `safe_insert_employee` and observe the custom error messages returned upon success or intentional failure.

> [!IMPORTANT]
> Stored Procedures and UDFs are essential for improving database performance, reducing network traffic, and enforcing business logic at the database layer. However, extensive use of procedural logic in the database can lead to vendor lock-in and harder-to-debug code compared to application-layer logic.

*Developed for Elevate Lab Internship Program - SQL Practice and Interview Preparation.*
