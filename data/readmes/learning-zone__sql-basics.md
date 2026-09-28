# MSSQL-Server 2025 Basics

> *Click &#9733; if you like the project. Your contributions are heartily ♡ welcome.*

<br/>

## Related Topics

* *[SQL Commands](sql-commands.md)*
* *[SQL Query Practice](sql-query-practice.md)*
* *[SQL Multiple Choice Questions](sql-mcq.md)*

<br/>

## Table of Contents

* [Introduction](#-1-introduction)
* [SQL Data Types](#-2-sql-data-types)
* [SQL Database](#-3-sql-database)
* [SQL Table](#-4-sql-table)
* [SQL Select](#-5-sql-select)
* [SQL Clause](#-6-sql-clause)
* [SQL Order By](#-7-sql-order-by)
* [SQL Insert](#-8-sql-insert)
* [SQL Update](#-9-sql-update)
* [SQL Delete](#-10-sql-delete)
* [SQL Keys](#-11-sql-keys)
* [SQL Join](#-12-sql-join)
* [SQL RegEx](#-13-sql-regex)
* [SQL Indexes](#-14-sql-indexes)
* [SQL Wildcards](#-15-sql-wildcards)
* [SQL Date Format](#-16-sql-date-format)
* [SQL Transactions](#-17-sql-transactions)
* [SQL Functions](#-18-sql-functions)
* [SQL View](#-19-sql-view)
* [SQL Triggers](#-20-sql-triggers)
* [SQL Cursors](#-21-sql-cursors)
* [SQL Stored Procedures](#-22-sql-stored-procedures)
* [DACPAC & Database Deployment](#-23-dacpac--database-deployment)
* [Miscellaneous](#-24-miscellaneous)

<br/>

## # 1. Introduction

<br/>

## Q. What is a database?

A database is a systematic or organized collection of related information stored in such a way that it can be easily accessed, retrieved, managed, and updated.

In SQL Server 2022, you create a database using `CREATE DATABASE`:

**Syntax:**

```sql
CREATE DATABASE database_name
[ ON PRIMARY (
    NAME = logical_name,
    FILENAME = 'path\file.mdf',
    SIZE = size,
    MAXSIZE = max_size,
    FILEGROWTH = growth_increment
  )
]
[ LOG ON (
    NAME = log_logical_name,
    FILENAME = 'path\file.ldf'
  )
];
```

**Example:**

```sql
CREATE DATABASE SalesDB
ON PRIMARY (
    NAME = SalesDB_Data,
    FILENAME = 'C:\SQLData\SalesDB.mdf',
    SIZE = 100MB,
    MAXSIZE = 1GB,
    FILEGROWTH = 10MB
)
LOG ON (
    NAME = SalesDB_Log,
    FILENAME = 'C:\SQLData\SalesDB_log.ldf',
    SIZE = 20MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 5MB
);

USE SalesDB;
GO
```

<div align="right">
    <b><a href="#table-of-contents">↥ back to top</a></b>
</div>

## Q. What is a database table?

A database table is a structure that organizes data into rows and columns. Each row represents a record and each column represents a field (attribute).

**Example:**

```sql
CREATE TABLE Employees (
    EmployeeID   INT           IDENTITY(1,1) PRIMARY KEY,
    FirstName    NVARCHAR(50)  NOT NULL,
    LastName     NVARCHAR(50)  NOT NULL,
    HireDate     DATE          NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    Salary       DECIMAL(10,2) NULL
);

SELECT * FROM Employees;
```

<div align="right">
    <b><a href="#table-of-contents">↥ back to top</a></b>
</div>

## Q. What is a database relationship?

Database relationships are associations between tables created using join statements. They improve table structure and reduce redundant data.

**Types of Database Relationships:**

**1. One-to-One:**

```sql
CREATE TABLE EmployeeContact (
    ContactID   INT PRIMARY KEY,
    EmployeeID  INT UNIQUE NOT NULL,
    Phone       NVARCHAR(20),
    CONSTRAINT fk_emp_contact FOREIGN KEY (EmployeeID)
        REFERENCES Employees(EmployeeID)
);
```

**2. One-to-Many:**

```sql
CREATE TABLE Departments (DeptID INT PRIMARY KEY, DeptName NVARCHAR(100) NOT NULL);

CREATE TABLE Staff (
    StaffID INT PRIMARY KEY,
    DeptID  INT NOT NULL,
    Name    NVARCHAR(100),
    CONSTRAINT fk_staff_dept FOREIGN KEY (DeptID) REFERENCES Departments(DeptID)
);
```

**3. Many-to-Many (junction table):**

```sql
CREATE TABLE Students (StudentID INT PRIMARY KEY, Name NVARCHAR(100));
CREATE TABLE Courses  (CourseID  INT PRIMARY KEY, Title NVARCHAR(100));

CREATE TABLE StudentCourses (
    StudentID INT NOT NULL,
    CourseID  INT NOT NULL,
    PRIMARY KEY (StudentID, CourseID),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID)  REFERENCES Courses(Course

[...截断...]

ID)
);
```

<div align="right">
    <b><a href="#table-of-contents">↥ back to top</a></b>
</div>

## Q. What is data Integrity?

Data Integrity defines the accuracy and consistency of data stored in a database. SQL Server enforces it through constraints and triggers.

**1. Entity Integrity** – unique, non-null row identifiers.

```sql
CREATE TABLE Products (
    ProductID   INT          PRIMARY KEY,
    ProductCode NVARCHAR(20) UNIQUE NOT NULL
);
```

**2. Referential Integrity** – relationships between tables stay valid.

```sql
ALTER TABLE OrderItems
ADD CONSTRAINT fk_product FOREIGN KEY (ProductID)
    REFERENCES Products(ProductID)
    ON DELETE CASCADE ON UPDATE CASCADE;
```

**3. Domain Integrity** – values stay within valid ranges.

```sql
ALTER TABLE Employees
ADD CONSTRAINT chk_salary   CHECK (Salary > 0),
ADD CONSTRAINT df_hiredate  DEFAULT GETDATE() FOR HireDate;
```

**4. User-Defined Integrity** – business rules via triggers.

```sql
CREATE TRIGGER trg_PreventNegativeStock
ON Inventory AFTER UPDATE
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE Quantity < 0)
    BEGIN
        RAISERROR('Stock cannot be negative.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
```

<div align="right">
    <b><a href="#table-of-contents">↥ back to top</a></b>
</div>

## Q. What are the two principles of the relational database model?

1. **Entity Integrity** – every table has a primary key that is unique and NOT NULL.
2. **Referential Integrity** – every foreign key value must match an existing primary key, or be NULL.

**Example:**

```sql
CREATE TABLE Categories (
    CategoryID   INT          NOT NULL PRIMARY KEY,   -- entity integrity
    CategoryName NVARCHAR(50) NOT NULL
);

CREATE TABLE Items (
    ItemID     INT           NOT NULL PRIMARY KEY,
    CategoryID INT           NOT NULL,
    ItemName   NVARCHAR(100) NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY (CategoryID)   -- referential integrity
        REFERENCES Categories(CategoryID)
);
```

<div align="right">
    <b><a href="#table-of-contents">↥ back to top</a></b>
</div>

## Q. What relational operations can be performed on a database?

| Operation | SQL Keyword | Description |
|-----------|-------------|-------------|
| Union | `UNION` | Combines result sets, removes duplicates |
| Intersection | `INTERSECT` | Returns rows common to both sets |
| Difference | `EXCEPT` | Rows in first set not in second |
| Cartesian Product | `CROSS JOIN` | Every row of A paired with every row of B |

**Example:**

```sql
CREATE TABLE #SetA (ID INT);
CREATE TABLE #SetB (ID INT);
INSERT INTO #SetA VALUES (1),(2),(3);
INSERT INTO #SetB VALUES (2),(3),(4);

SELECT ID FROM #SetA UNION     SELECT ID FROM #SetB;   -- 1,2,3,4
SELECT ID FROM #SetA INTERSECT SELECT ID FROM #SetB;   -- 2,3
SELECT ID FROM #SetA EXCEPT    SELECT ID FROM #SetB;   -- 1

SELECT a.ID AS A_ID, b.ID AS B_ID FROM #SetA a CROSS JOIN #SetB b; -- 9 rows
```

<div align="right">
    <b><a href="#table-of-contents">↥ back to top</a></b>
</div>

## Q. What is database normalization?

Normalization organizes a database to reduce redundancy and improve data integrity through a series of normal forms.

**Example – unnormalized → 3NF:**

```sql
-- 3NF: no transitive dependencies
CREATE TABLE Departments (
    DeptID   INT          PRIMARY KEY,
    DeptName NVARCHAR(100) NOT NULL
);

CREATE TABLE Employees_3NF (
    EmpID   INT          PRIMARY KEY,
    EmpName NVARCHAR(100) NOT NULL,
    DeptID  INT          NOT NULL REFERENCES Departments(DeptID)
);
```

<div align="right">
    <b><a href="#table-of-contents">↥ back to top</a></b>
</div>

## Q. What are the different types of normalization?

| Normal Form | Rule |
|-------------|------|
| 1NF | Atomic column values; no repeating groups |
| 2NF | 1NF + every non-key attribute fully depends on the whole PK |
| 3NF | 2NF + no transitive dependencies |
| BCNF | Every determinant is a candidate key |
| 4NF | BCNF + no multi-valued dependencies |
| 5NF | 4NF + no join dep