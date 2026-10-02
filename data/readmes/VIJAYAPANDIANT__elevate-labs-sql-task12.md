# 📊 Elevate Lab SQL Task 12: SQL Schema Demonstrating Constraint Usage

A professional SQL project demonstrating the practical application of SQL constraints to ensure data integrity and validation at the database level. It covers the creation of relational tables with various constraints, intentional violation testing, and an analysis of constraint enforcement order.

## 📌 Project Objective
The primary goal of this task is to understand the impact of constraints on data integrity. It illustrates how to define rules at the database level to prevent invalid data entry, demonstrating the use of `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK`, and `DEFAULT` constraints, while also highlighting the differences between database-level and application-level validation.

## 🛠️ Technical Scope
- **Database Management System:** SQL (MySQL / PostgreSQL / SQL Server compatible)
- **Core Concepts:** Data Integrity, Relational Database Schema, Database Constraints
- **Advanced Techniques:** Constraint Enforcement Order, Composite Unique Constraints, Database vs. Application-Level Validation

## 🗄️ Database Schema

### `users` Table
| Column | Data Type | Constraint / Description |
| :--- | :--- | :--- |
| `user_id` | `INT` | Primary Key, `AUTO_INCREMENT` |
| `email` | `VARCHAR(255)` | `UNIQUE`, `NOT NULL` |
| `age` | `INT` | `CHECK` (`age BETWEEN 18 AND 60`) |
| `gender` | `CHAR(1)` | `CHECK` (`gender IN ('M', 'F', 'O')`) |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |

### `orders` Table
| Column | Data Type | Constraint / Description |
| :--- | :--- | :--- |
| `order_id` | `INT` | Primary Key, `AUTO_INCREMENT` |
| `user_id` | `INT` | Foreign Key (References `users(user_id)`), `NOT NULL` |
| `order_amount` | `DECIMAL(10,2)` | `CHECK` (`order_amount > 0`) |
| `order_status` | `VARCHAR(20)` | `DEFAULT 'PENDING'`, `CHECK` (`order_status IN ('PENDING', 'PAID', 'CANCELLED')`) |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |
*Note: The `orders` table also includes a composite UNIQUE constraint on `(user_id, created_at)`.*

## 💻 SQL Implementations
Key operations demonstrated in the script:

- **Database & Schema Setup:**
  Creation of the `task12` database, alongside the `users` and `orders` tables with specific validation rules.
- **Constraint Applications:**
  Applying various constraints like `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK` (range and enum-style), and `DEFAULT` to enforce business logic directly within the database schema.
- **Intentional Constraint Violations:**
  Executing `INSERT` statements intentionally designed to fail in order to test and verify that the `CHECK` and `UNIQUE` constraints are actively rejecting invalid data (e.g., negative order amounts, out-of-range ages, duplicate emails).
- **Constraint Enforcement Order:**
  Analyzing the typical sequence in which databases evaluate constraints (`NOT NULL` -> `CHECK` -> `UNIQUE` -> `FOREIGN KEY`) to understand how overlapping validations are handled.
- **Database vs. Application Validation:**
  Providing a comparative analysis demonstrating why database-level constraints are mandatory for absolute truth and security, whereas application-level validation is complementary for user experience.
- **Constraint Management:**
  Demonstrating how to modify existing tables by dropping constraints (e.g., `DROP CHECK`, `DROP INDEX`, `DROP FOREIGN KEY`) when business requirements evolve.

## 🚀 Setup & Execution
1. **Initialize:** Execute the script to create the `task12` database, `users` table, and `orders` table.
2. **Review Constraints:** Observe the various constraints applied to the columns during table creation.
3. **Execute Violation Tests:** Run the intentional `INSERT` queries designed to violate constraints and observe the resulting database errors.
4. **Analyze Concepts:** Read through the embedded documentation regarding constraint enforcement order and the comparison between database and application-level validation.
5. **Manage Constraints:** Review the `ALTER TABLE` commands showing how to remove constraints if necessary.

## Important

> [!IMPORTANT]
> While application-level validation improves user experience by catching errors early, **database-level validation is mandatory** for ensuring truth and security. Application logic can be bypassed (e.g., via direct API calls or bulk imports), but database constraints are always enforced, acting as the final line of defense against invalid data.

*Developed for Elevate Lab Internship Program - SQL Practice and Interview Preparation.*
