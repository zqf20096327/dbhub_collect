<!-- omit in toc -->
# SQL Bootcamp 2021 & Advanced Queries

<!-- omit in toc -->
## Description

Databases are systems that allow users to store and organize data and are useful when dealing with large amounts of data. On the other hand, spreadsheets are suitable for one-time analysis, quick charts, reasonable datasets, and allowing untrained people to work with data.

Databases are suitable for data integrity, handling large amounts of data, combining different datasets quickly, automating reuse steps, and supporting data for websites and applications.

A **database** is a collection of tables. **Tables** contain rows and columns, where the **rows** are known as **records** and the **columns** are known as **fields**. A **column** is a set of data values of a particular type, one value for each row of the database. A **row** represents a single data item in a table, and every row in the table has the same structure.

<!-- omit in toc -->
## Table of Contents
<!-- toc here -->
- [1. Overview](#1-overview)
  - [1.1. Course Curriculum](#11-course-curriculum)
  - [1.2. Challenges](#12-challenges)
- [2. Setup](#2-setup)
- [3. SQL Statement Fundamentals](#3-sql-statement-fundamentals)
  - [3.1. SELECT Statement](#31-select-statement)
  - [3.2. DISTINCT Keyword](#32-distinct-keyword)
  - [3.3. COUNT Function](#33-count-function)
  - [3.4. WHERE Clause](#34-where-clause)
  - [3.5. ORDER BY Clause](#35-order-by-clause)
  - [3.6. LIMIT Clause](#36-limit-clause)
  - [3.7. BETWEEN Operator](#37-between-operator)
  - [3.8. IN Operator](#38-in-operator)
  - [3.9. LIKE and ILIKE Operators & Pattern Matching](#39-like-and-ilike-operators--pattern-matching)
- [4. General Challenge 1](#4-general-challenge-1)
- [5. GROUP BY Statements & Aggregate Functions](#5-group-by-statements--aggregate-functions)
  - [5.1. Aggregation Functions - AVG, COUNT, MAX, MIN and SUM](#51-aggregation-functions---avg-count-max-min-and-sum)
  - [5.2. GROUP BY Statement](#52-group-by-statement)
  - [5.3. HAVING Clause](#53-having-clause)
- [6. Assessment Test 1](#6-assessment-test-1)
- [7. JOIN Clause](#7-join-clause)
  - [7.1. Aliases: AS Clause](#71-aliases-as-clause)
  - [7.2. (INNER) JOIN Keyword (Intersection)](#72-inner-join-keyword-intersection)
  - [7.3. FULL (OUTER) JOIN Keyword (Union and Symmetric Difference)](#73-full-outer-join-keyword-union-and-symmetric-difference)
  - [7.4. LEFT (OUTER) JOIN Keyword (A)](#74-left-outer-join-keyword-a)
  - [7.5. RIGHT (OUTER) JOIN Keyword (B)](#75-right-outer-join-keyword-b)
  - [7.6. UNION Operator](#76-union-operator)
  - [7.7. JOIN Challenges](#77-join-challenges)
- [8. Advanced SQL Commands](#8-advanced-sql-commands)
  - [8.1. Timestamps and Extract](#81-timestamps-and-extract)
    - [8.1.1. Displaying Current Time Information](#811-displaying-current-time-information)
    - [8.1.2. Extracting Time and Date Information](#812-extracting-time-and-date-information)
  - [8.2. Mathematical Functions and Operators](#82-mathematical-functions-and-operators)
  - [8.3. String Functions and Operators](#83-string-functions-and-operators)
  - [8.4. Subquery](#84-subquery)
  - [8.5. Self-Join](#85-self-join)
- [9. Assessment Test 2](#9-assessment-test-2)
- [10. Creating Databases and Tables](#10-creating-databases-and-tables)
  - [10.1. Data Types](#101-data-types)
  - [10.2. Primary and Foreign Key](#102-primary-and-foreign-key)
  - [10.3. Constraints](#103-constraints)
  - [10.4. CREATE TABLE Statement (TABLE)](#104-create-table-statement-table)
  - [10.5. INSERT INTO Statement (RECORD)](#105-insert-into-statement-record)
  - [10.6. UPDATE Statement (RECORD)](#106-update-statement-record)
  - [10.7. DELETE Statement (RECORD)](#107-delete-statement-record)
  - [10.8. ALTER TABLE Statement (TABLE AND COLUMN)](#108-alter-table-statement-table-and-column)
    - [10.8.1. RENAME, ADD, DROP, SET Statements (TABLE AND COLUMN)](#1081-rename-add-drop-set-statements-table-and-column)
    - [10.8.2. DROP Statement (COLUMN)](#1082-drop-st

[...截断...]

atement-column)
  - [10.9. CHECK Constraint](#109-check-constraint)
- [11. Assessment Test 3](#11-assessment-test-3)
- [12. Conditional Expressions and Procedures](#12-conditional-expressions-and-procedures)
  - [12.1. CASE ... END Statement](#121-case--end-statement)
  - [12.2. COALESCE() Function](#122-coalesce-function)
  - [12.3. CAST() Function](#123-cast-function)
  - [12.4. NULLIF() Function](#124-nullif-function)
  - [12.5. (CREATE) VIEW Statement](#125-create-view-statement)
- [13. Import and Export](#13-import-and-export)
- [14. PgSQL with Python](#14-pgsql-with-python)
- [15. SQL Window Function Part 1](#15-sql-window-function-part-1)
  - [15.1. Fundamentals, the Over Clause and Partition By](#151-fundamentals-the-over-clause-and-partition-by)
  - [15.2. Other examples and Row Number and Order By (inside Over Clause)](#152-other-examples-and-row-number-and-order-by-inside-over-clause)
  - [15.3. Window Functions: Rank, Dense Rank](#153-window-functions-rank-dense-rank)
  - [15.4. Window Functions: Lead and Lag](#154-window-functions-lead-and-lag)
- [16. SQL Window Function Part 2](#16-sql-window-function-part-2)
  - [16.1. First and Last Value](#161-first-and-last-value)
  - [16.2. Frame Clause](#162-frame-clause)
  - [16.3. Windows Clause](#163-windows-clause)
  - [16.4. N-th Value](#164-n-th-value)
  - [16.5. Ntile](#165-ntile)
  - [16.6. Cumulative Distribution Cume_Dist](#166-cumulative-distribution-cume_dist)
  - [16.7. Percent Rank](#167-percent-rank)
- [17. SQL With Clause and CTE (Common Table Expression) or Sub-Query Factoring](#17-sql-with-clause-and-cte-common-table-expression-or-sub-query-factoring)
- [18. Practice Complex SQL Queries](#18-practice-complex-sql-queries)
  - [18.1. Exercise 1](#181-exercise-1)
  - [18.2. Exercise 2](#182-exercise-2)
  - [18.3. Exercise 3](#183-exercise-3)
  - [18.4. Exercise 4](#184-exercise-4)
  - [18.5. Exercise 5](#185-exercise-5)
  - [18.6. Exercise 6](#186-exercise-6)
  - [18.7. Exercise 7](#187-exercise-7)
  - [18.8. Exercise 9](#188-exercise-9)
- [19. Misc Notes](#19-misc-notes)
  - [19.1. General Syntax](#191-general-syntax)
  - [19.2. Misc Notes from Revision](#192-misc-notes-from-revision)
- [20. Solutions to Codility Exercise](#20-solutions-to-codility-exercise)

<!-- update number, TOC -->

# 1. Overview

Overview of the course curriculum and challenges.

## 1.1. Course Curriculum

<details>
<summary>The course is divided in the following sections...</summary>

- Section 1
  - Databses and Table Basics
  - SQL Statement Fundamentals
  - GROUP BY Clause
  - Assessment Test 1
- Section 2
  - JOINS
  - Advanced SQL
  - Commands
  - Assessment Test 2
- Section 3
  - Create Database and Tables
  - Assessment Test 3
  - Views
  - PostgreSQL with Python

</details>

<details>
<summary>Typical database users...</summary>

- Analyst
  - Marketing
  - Business
  - Sales
- Technical
  - Data Scientist
  - Software Engineers
  - Web Developers

</details>

<details>
<summary>Database Platform Options:</summary>

- PostgreSQL (focus of the course)
  - Free (Open Source)
  - Widely used on internet
  - Multi platform
- MySQL & MariaSQL
  - Free (Open Source)
  - Widely used on internet
  - Multi platform
- MS SQL Server Express
  - Free, but with some limitations
  - Compatible with SQL Server
  - Windows only (-)
- Microsoft Access
  - Cost (-)
  - Not easy to use just SQL (-)
- SQLite
  - Free (Open Source)
  - Mainly command line (-)

</details>

SQL is the programming language used to communicate with our database. Example:

```sql
select customer_id, first_name, last_name
from sales
order by first_name;
-- the ; at the end of the query is optional is pgSQL
```

## 1.2. Challenges

Challenges are based on the scenario that we've just been hired as a SQL consultant for a DVD Rental Store. Challenges increase in difficult over the course.

<details>
<summary>Challenge structure...</summary>

- Business Situation
- Challenge Question
- Expected Answer
- Hints
- Solution

</