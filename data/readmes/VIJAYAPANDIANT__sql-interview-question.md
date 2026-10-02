# 🔹 SQL Interview Questions & Tasks Repository

Welcome to the ultimate **SQL Interview Preparation** repository! This collection is designed to take you from fundamental concepts to advanced analytical queries and system design.

## 📖 Table of Contents

- [🏗️ 1. Fundamentals & Architecture](#-1-fundamentals--architecture)
- [🔍 2. Querying & Manipulation](#-2-querying--manipulation)
- [⚙️ 3. Advanced SQL Concepts](#-3-advanced-sql-concepts)
- [🚀 4. SQL Performance](#-4-sql-performance)
- [📊 5. System Design & Analytics](#-5-system-design--analytics)
- [🛠️ Thematic SQL Tasks](#️-thematic-sql-tasks)
- [🚀 How to Use This Repository](#-how-to-use-this-repository)

---

## 🔹 Top SQL Interview Questions & Answers

### 🏗️ 1. Fundamentals & Architecture

**1. What is SQL? How is it different from MySQL or PostgreSQL?**

SQL (Structured Query Language) is a language used to store, manipulate, and retrieve data from relational databases.

| Feature | SQL | MySQL / PostgreSQL |
| :--- | :--- | :--- |
| **Type** | Query language | Database management systems |
| **Purpose** | Used to write queries | Used to store and manage data |

**Example:**
```sql
SELECT * FROM employees;
```

**2. Types of SQL Statements**

*   **DDL (Data Definition Language):** `CREATE`, `ALTER`, `DROP`, `TRUNCATE`
*   **DML (Data Manipulation Language):** `INSERT`, `UPDATE`, `DELETE`
*   **DQL (Data Query Language):** `SELECT`
*   **DCL (Data Control Language):** `GRANT`, `REVOKE`
*   **TCL (Transaction Control Language):** `COMMIT`, `ROLLBACK`, `SAVEPOINT`

**3. Difference Between `WHERE` and `HAVING`**

| `WHERE` | `HAVING` |
| :--- | :--- |
| Filters rows | Filters groups |
| Used before `GROUP BY` | Used after `GROUP BY` |
| Cannot use aggregate functions | Can use aggregate functions |

**Example:**
```sql
SELECT department, AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;
```

**4. Constraints**

*   **PRIMARY KEY:** Unique identifier for each row. `id INT PRIMARY KEY`
*   **FOREIGN KEY:** Links two tables. `FOREIGN KEY (dept_id) REFERENCES department(id)`
*   **UNIQUE:** Ensures values are unique.
*   **CHECK:** Limits allowed values. `salary INT CHECK (salary > 0)`

**5. `DELETE` vs `TRUNCATE` vs `DROP`**

| Feature | `DELETE` | `TRUNCATE` | `DROP` |
| :--- | :--- | :--- | :--- |
| **Action** | Deletes rows | Deletes all rows | Deletes table |
| **Condition** | Can use `WHERE` | No `WHERE` | Removes structure |
| **Speed** | Slower | Faster | Permanent |

**6. Normalization**

Process of organizing database to reduce redundancy.
*   **1NF:** No repeating groups
*   **2NF:** Remove partial dependency
*   **3NF:** Remove transitive dependency
*   **BCNF:** Stronger version of 3NF

**7. Denormalization**

Combining tables to improve query performance. Used in data warehouses and reporting systems.
*   **Tradeoff:** More redundancy but faster queries.

**8. `CHAR` vs `VARCHAR`**

| `CHAR` | `VARCHAR` |
| :--- | :--- |
| Fixed length | Variable length |
| Faster | Saves storage |

**9. ACID Properties**

*   **A – Atomicity:** All or nothing.
*   **C – Consistency:** Valid data state.
*   **I – Isolation:** Transactions are independent.
*   **D – Durability:** Data survives crashes.

**10. Types of JOIN**

*   **INNER JOIN:** Returns matching rows from both tables.
*   **LEFT JOIN:** All rows from left table, matching from right.
*   **RIGHT JOIN:** All rows from right table, matching from left.
*   **FULL JOIN:** All rows from both tables.

---

### 🔍 2. Querying & Manipulation

**11. Second Highest Salary**
```sql
SELECT MAX(salary)
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

**12. Department Average Salary**
```sql
SELECT department_id, AVG(salary)
FROM employees
GROUP BY department_id;
```

**13. Find Duplicate Records**
```sql
SELECT name, COUNT(*)
FROM employees
GROUP BY name
HAVING COUNT(*) > 1;
```

**14. Update with Calculation**
```sql
-- Add 10% tax
UPDATE products
SET price = price * 1.10;
```

**15. Delete Duplicate Rows**
```sql
DELETE FROM employees
WHERE id NOT IN (
    SELECT MIN(id)
    FROM employees
    GROUP BY name
);
```

**16. Customers with More Than 5 Orders**
```sql
SELECT customer_id, COUNT(*)
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;
```

**17. Join Three Tables**
```sql
SELECT o.order_id, c.name, p.product_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id;
```

**18. Subquery vs JOIN**

| Subquery | JOIN |
| :--- | :--- |
| Query inside another query | Combines tables |
| Often slower | Usually faster |

**19. Correlated Subquery**

Runs once for each row of the outer query.
```sql
SELECT name
FROM employees e1
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e2
    WHERE e1.department_id = e2.department_id
);
```

**20. Date Range Filter**
```sql
SELECT *
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';
```

---

### ⚙️ 3. Advanced SQL Concepts

**21. Window Functions**

Functions that operate on rows related to the current row.
*   `ROW_NUMBER()`
*   `RANK()`
*   `DENSE_RANK()`
*   `LAG()`
*   `LEAD()`

**22. `RANK` vs `DENSE_RANK` vs `ROW_NUMBER`**

| Function | Behavior |
| :--- | :--- |
| `ROW_NUMBER` | Unique sequential number |
| `RANK` | Skips numbers after ties |
| `DENSE_RANK` | No gaps after ties |

**23. CTE (Common Table Expression)**

Temporary result set defined within the execution scope of a single statement.
```sql
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) avg_sal
    FROM employees
    GROUP BY dept_id
)
SELECT * FROM dept_avg;
```

**24. Stored Procedures**

Saved SQL code that can be executed repeatedly.
```sql
CREATE PROCEDURE getEmployees()
BEGIN
    SELECT * FROM employees;
END;
```

**25. Trigger**

Automatically executes when a specific event (INSERT, UPDATE, DELETE) occurs.
```sql
-- Update stock after order
CREATE TRIGGER update_stock
AFTER INSERT ON orders
FOR EACH ROW
UPDATE products
SET stock = stock - NEW.quantity;
```

**26. View**

A virtual table based on the result-set of an SQL query.
```sql
CREATE VIEW high_salary AS
SELECT name, salary
FROM employees
WHERE salary > 50000;
```
*   **Pros:** Security, simplifies complex queries.
*   **Cons:** May reduce performance if not managed properly.

**27. Index**

Improves search speed at the cost of disk space and slower updates.
```sql
CREATE INDEX idx_name ON employees(name);
```

**28. Materialized View**

Stores the query result physically on disk. Used for expensive analytical queries.

**29. Transactions**

A group of SQL operations that are treated as a single unit of work.
*   `BEGIN;`, `COMMIT;`, `ROLLBACK;`, `SAVEPOINT sp1;`

**30. Aggregate Functions**

Examples: `COUNT()`, `SUM()`, `AVG()`, `MAX()`, `MIN()`.

---

### 🚀 4. SQL Performance

**31. Optimize Slow Queries**

*   Add appropriate **indexes**.
*   Avoid `SELECT *` (select only needed columns).
*   Use **JOINs** instead of subqueries where possible.
*   Analyze the **query plan** (`EXPLAIN`).
*   **Partition** large tables.

**32. `EXPLAIN`**

Shows how the database engine plans to execute a query.
```sql
EXPLAIN SELECT * FROM employees;
```

**33. Index Impact on Operations**

| Operation | Impact |
| :--- | :--- |
| `SELECT` | Faster |
| `INSERT` | Slightly slower |
| `UPDATE` | Slower |
| `DELETE` | Slower |

**34. Composite Index**

An index on multiple columns.
```sql
CREATE INDEX idx_name_dept ON employees(name, department_id);
```

**35. Normalization Overhead**

Too many joins can lead to slower queries.
*   **Solutions:** Denormalization, Materialized views, Caching.

**36. Avoid Cartesian Product**

Always use a `JOIN` condition to prevent `A x B` row multiplication.
*   **Bad:** `SELECT * FROM A, B;`
*   **Good:** `SELECT * FROM A JOIN B ON A.id = B.id;`

**37. Partitioning**

Splitting a large table into smaller, more manageable parts (Range, List, Hash).

**38. Deadlock**

Occurs when two transactions wait for each other to release locks.
*   **Prevention:** Consistent lock order, short transactions, proper indexing.

**39. Clustered vs Non-Clustered Index**

| Feature | Clustered Index | Non-Clustered Index |
| :--- | :--- | :--- |
| **Data Storage** | Data stored with index | Separate structure |
| **Count** | Only one per table | Multiple allowed |

**40. SQL Monitoring Tools**

MySQL Workbench, pgAdmin, SQL Server Profiler, `EXPLAIN`, Performance Schema.

---

### 📊 5. System Design & Analytics

**41. Student Course System Design**

*   **Tables:** `Students`, `Courses`, `Enrollments`, `Grades`.
*   **Relationship:** `Students ---< Enrollments >--- Courses` (Many-to-Many).

**42. Employee Attendance System**

*   **Tables:** `Employees`, `Attendance`, `Departments`.
*   **Columns:** `employee_id`, `date`, `check_in`, `check_out`.
*   **Optimization:** Index on `(employee_id, date)`.

**43. Library System**

*   **Overdue Query Example:**
```sql
SELECT * FROM borrow
WHERE return_date IS NULL AND due_date < CURRENT_DATE;
```

**44. Recovery After Failed Update**

Steps: Check transaction logs, restore from backup, use point-in-time recovery, reapply changes.

**45. Role-Based Access Control (RBAC)**
```sql
CREATE ROLE manager;
GRANT SELECT, INSERT ON employees TO manager;
```

**46. Cleaning Dirty Data (ETL)**

Steps: Load into staging table → Remove NULLs → Standardize formats → Validate constraints.

**47. Monthly User Retention**
```sql
SELECT DATE_TRUNC('month', login_date) AS month, COUNT(DISTINCT user_id)
FROM logins
GROUP BY month;
```

**48. Database Security**

Encryption, Access control, Row-level security, Audit logs, Regular backups.

**49. Backup & Restore Plan**

*   **Backup:** `mysqldump -u root -p dbname > backup.sql`
*   **Restore:** `mysql -u root -p dbname < backup.sql`

---

## 🛠️ Thematic SQL Tasks

The repository also contains hands-on task files (`Task1.sql` to `Task16.sql`) that provide detailed explanations and practice questions for specific topics:

*   **Tasks 1 - 5:** Fundamentals, database modeling, and basic syntax.
*   **Tasks 6 - 10:** Intermediate queries, grouping, subqueries, and relationships.
*   **Tasks 11 - 15:** Advanced querying, administration, triggers, and performance tuning.
*   **Task 16:** Business Intelligence (BI) and Analytics (Trends, high-value customers, time-based analysis).

---

## 🚀 How to Use This Repository

1.  **Start with the Core Guide:** Read through this `README.md` to build a strong theoretical foundation.
2.  **Practice by Tasks:** Open individual `TaskX.sql` files and test your knowledge.
3.  **Execute Queries:** Use a local database instance (MySQL/PostgreSQL) to run the queries discussed.
4.  **Prepare for System Design:** Focus on sections 5 and the later task files for architectural knowledge.

---
_Best of luck with your SQL interview preparation!_
