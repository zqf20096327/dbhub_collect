# 📊 Elevate Lab SQL Task 6: Employee Management System

A professional SQL project demonstrating core database management techniques, including CRUD operations, data validation, safe deletions, and transaction management.

## 📌 Project Objective

The primary goal of this task is to implement essential database operations using SQL. This includes creating a database schema, populating it with bulk data, performing advanced filtering and conditional updates, practicing safe deletions, and managing transactions to ensure data integrity.

## 🛠️ Technical Scope

- **Database Management System:** SQL (MySQL / PostgreSQL / SQL Server compatible)
- **Core Operations:** CRUD (Create, Read, Update, Delete)
- **Advanced Techniques:** Conditional Filtering, Safe Updates (`SQL_SAFE_UPDATES`), Transaction Management (`START TRANSACTION`, `COMMIT`, `ROLLBACK`)

## 🗄️ Database Schema

### `employees` Table

| Column         | Data Type       | Constraint / Description         |
| :------------- | :-------------- | :------------------------------- |
| `emp_id`       | `INT`           | Primary Key, Auto-increment      |
| `emp_name`     | `VARCHAR(100)`  | Full Name of Employee            |
| `department`   | `VARCHAR(50)`   | Department (IT, HR, Sales, etc.) |
| `salary`       | `DECIMAL(10,2)` | Monthly/Annual Salary            |
| `joining_date` | `DATE`          | Date of Joining                  |
| `status`       | `VARCHAR(20)`   | Active/Inactive status           |

## 💻 SQL Implementations

Key operations demonstrated in the script:

1. **Schema & Data Creation:**
   - Creation of the `task6` database and `employees` table.
   - Bulk `INSERT` of multiple employee records.
2. **Data Retrieval (Read):**
   - Retrieving all records.
   - Filtering data conditionally (e.g., specific departments or salary ranges).
3. **Data Modification (Update):**
   - Conditional updates based on specific criteria (e.g., salary increments for the 'IT' department).
4. **Data Deletion (Delete):**
   - Removing records conditionally.
   - Demonstrating safe delete practices by utilizing primary keys and enforcing safe updates.
5. **Transaction Management:**
   - Utilizing `START TRANSACTION` and `ROLLBACK` to revert unwanted changes and maintain data integrity.
6. **Data Validation:**
   - Querying total record counts and dataset states before and after performing modifications.

## 🚀 Setup & Execution

1. **Initialize:** Execute the script to create the `task6` database and the `employees` table.
2. **Populate Data:** Run the `INSERT` statements to load initial records.
3. **Query Data:** Execute the `SELECT` statements to verify data filtering operations.
4. **Modify & Transact:** Step through the `UPDATE`, `DELETE`, and transaction blocks to observe how data manipulation and rollbacks are handled.

> [!IMPORTANT]
> Always ensure `WHERE` clauses are correctly applied in `UPDATE` and `DELETE` operations to prevent unintentional data loss or modification across the entire table.

---

*Developed for Elevate Lab Internship Program - SQL Practice and Interview Preparation.*
