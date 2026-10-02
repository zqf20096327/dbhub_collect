# 📊 Elevate Lab SQL Task 10: Mastering SQL Views and Joins

A professional SQL project demonstrating the implementation of relational database structures, complex data retrieval using JOINs, and the creation, management, and limitations of SQL VIEWs.

## 📌 Project Objective
The primary goal of this task is to understand how to encapsulate complex relational queries using SQL Views. It illustrates the creation of tables with foreign key relationships, performing joins across these tables, creating views from these joins for simplified access, and explicitly exploring the restrictions around updating views that involve multiple base tables.

## 🛠️ Technical Scope
- **Database Management System:** SQL (MySQL / PostgreSQL / SQL Server compatible)
- **Core Concepts:** Relational Database Queries, Data Filtering, Sorting, Data Encapsulation
- **Advanced Techniques:** Complex JOINs, SQL VIEW Creation, DML Operations on Views, View Updatability Limitations

## 🗄️ Database Schema

### `departments` Table
| Column | Data Type | Constraint / Description |
| :--- | :--- | :--- |
| `dept_id` | INT | Primary Key |
| `dept_name` | VARCHAR(50) | Department Name (e.g., HR, IT) |

### `employees` Table
| Column | Data Type | Constraint / Description |
| :--- | :--- | :--- |
| `emp_id` | INT | Primary Key |
| `emp_name` | VARCHAR(50) | Full Name of Employee |
| `salary` | DECIMAL(10,2) | Employee Salary |
| `dept_id` | INT | Foreign Key referencing `departments(dept_id)` |

## 💻 SQL Implementations
Key operations demonstrated in the script:

**Schema Creation & Data Insertion:**
* Creation of the `task10` database.
* Creating the `departments` and `employees` tables with primary and foreign key constraints to establish a relationship.
* Populating both tables with sample records.

**Complex JOIN Query:**
* Executing a query that joins `employees` and `departments` to display comprehensive employee details alongside their respective department names.

**Creating a SQL VIEW:**
* Encapsulating the complex JOIN query into a reusable virtual table (`emp_department_view`) to simplify future data access.

**Querying, Filtering & Sorting Views:**
* Retrieving all data directly from the newly created view.
* Applying `WHERE` clauses to filter the view (e.g., fetching only employees in the 'IT' department).
* Applying `ORDER BY` to sort the view results (e.g., ordering by salary in descending order).

**View Updatability & Limitations:**
* Attempting to perform an `INSERT` operation directly through the view.
* Demonstrating and documenting why this fails: Views containing a `JOIN` across multiple base tables are generally not updatable. Data modifications must be performed on the base tables instead.

**Safe View Management:**
* Demonstrating the safe dropping and recreating of views using `DROP VIEW IF EXISTS`.

## 🚀 Setup & Execution
1. **Initialize:** Execute the script to create the `task10` database, `departments` table, and `employees` table.
2. **Populate Data:** Run the `INSERT` statements to load initial departmental and employee records.
3. **Execute JOINs:** Run the complex join query to verify the relational data.
4. **Create and Test View:** Create the `emp_department_view` and run the basic `SELECT` queries against it.
5. **Filter and Sort:** Test the filtered and sorted queries on the view to observe how views act like standard tables for data retrieval.
6. **Test Updatability (Intentional Failure):** Attempt to run the `INSERT` statement on the view to observe the database error regarding non-updatable join views.
7. **Recreate View:** Execute the drop and recreate statements to understand view lifecycle management.

> [!IMPORTANT]
> While SQL Views offer a highly secure and simplified way to present complex, joined data to end-users without exposing the underlying schema, understanding their strict limitations regarding `INSERT`, `UPDATE`, and `DELETE` operations is crucial. When a view involves joins, aggregations, or groupings, any data manipulation must typically be routed directly to the underlying base tables.

*Developed for Elevate Lab Internship Program - SQL Practice and Interview Preparation.*
