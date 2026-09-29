# 🧠 AI-Powered Text-to-SQL Generation & Database Query Validation

An **AI-assisted Text-to-SQL project** that converts natural-language business questions into executable SQL and validates the generated queries against a relational database.

The project uses **Kimi K2.6** for natural-language-to-SQL generation and **TiDB Cloud** for database creation, synthetic data population, query execution, and result validation.

The database models the operations of a dental practice, including patients, staff, appointments, medical procedures, insurance, billing, loans, expenses, inventory, and financial reporting.

---

## 📌 Project Overview

Writing SQL traditionally requires users to understand:

* Database schemas
* Table relationships
* JOIN operations
* Aggregations
* Date functions
* Filtering conditions
* SQL syntax

This project explores a different workflow:

```text
Natural-Language Question
          ↓
       LLM
     Kimi K2.6
          ↓
   Generated SQL
          ↓
      TiDB Cloud
          ↓
   Query Execution
          ↓
 Result Validation
```

Instead of manually translating every business question into SQL, an LLM receives the database context and generates an appropriate SQL query.

The generated query is then executed against a populated TiDB database to verify that it is syntactically valid and produces a meaningful result.

---

# 🎯 Objectives

The project demonstrates how AI can assist with database querying by:

* Translating English questions into SQL
* Providing database schema context to an LLM
* Generating relational database tables
* Populating tables with synthetic data
* Executing AI-generated SQL against real tables
* Validating query results
* Working with joins, aggregations, dates, and filtering
* Exploring the practical capabilities and limitations of Text-to-SQL systems

---

# 🛠️ Technologies Used

### AI

* **Kimi K2.6**
* Large Language Models
* Natural Language Processing
* Text-to-SQL

### Database

* **TiDB Cloud**
* SQL
* Relational Database Design
* Primary & Foreign Keys
* Database Indexes

### Concepts

* Prompt Engineering
* Text-to-SQL Generation
* SQL Query Validation
* Synthetic Data Generation
* Relational Data Modeling
* Business Intelligence Queries

---

# 🦷 Database Domain

The database models a new **dental practice** and its major business operations.

The system tracks:

* Staff
* Medical professionals
* Professional licenses
* Patients
* Appointments
* Treatment rooms
* Medical records
* Procedures
* Treatments
* Surgeries
* Insurance providers
* Insurance policies
* Insurance claims
* Billing
* Payments
* Business loans
* Startup expenses
* Monthly expenses
* Building leases
* Supplies and inventory
* Employee salaries
* Daily reports
* Monthly financial reports

---

# 🗄️ Database Schema

The generated database contains multiple related tables organized around several business areas.

## Staff & Patients

```text
staff_role
staff
patient_state
patient
```

The `staff` table tracks employees and medical professionals, including professional license expiration dates.

The `patient` table stores patient information and their current scheduling state.

---

## Scheduling

```text
room
appointment
```

Appointments associate:

```text
Patient
   +
Doctor / Hygienist
   +
Treatment Room
   +
Date & Time
```

This allows the practice to manage its eight treatment rooms and clinical schedules.

---

## Medical Records

```text
medical_record
procedure_code
procedure
treatment_code
treatment
surgery_code
surgery
```

Medical activity is separated into:

* Procedures
* Treatments
* Surgeries

Each medical event is associated with a patient's medical record and the staff member responsible for performing or prescribing it.

---

## Insurance & Billing

```text
insurance_provider
coverage_type
patient_insurance
insurance_claim
billing_record
payment
```

These tables support:

* Patient insurance policies
* Insurance providers
* Coverage information
* Insurance claims
* Patient billing
* Insurance payments
* Patient payments

---

## Finance & Operations

```text
loan
loan_payment
startup_cost
monthly_expense
lease_agreement
lease_payment
salary_payment
```

These tables model major financial obligations of the dental practice.

---

## Inventory

```text
supply_category
supply_inventory
supply_restock
```

These tables allow supplies such as medical equipment, drugs, needles, and general office supplies to be tracked and restocked.

---

## Reporting

```text
daily_report
monthly_financial_report
```

These tables support operational and financial reporting.

---

# 🏗️ System Workflow

```text
┌─────────────────────────────┐
│ Dental Practice Description │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Kimi K2.6            │
│                             │
│ Understand database context │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Database Schema / SQL    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         TiDB Cloud          │
│                             │
│ • Create tables             │
│ • Insert synthetic data     │
│ • Maintain relationships    │
└──────────────┬──────────────┘
               │
               ▼
       Natural-Language
       Business Question
               │
               ▼
┌─────────────────────────────┐
│        Kimi K2.6            │
│       Text-to-SQL           │
└──────────────┬──────────────┘
               │
               ▼
        Generated SQL
               │
               ▼
┌─────────────────────────────┐
│      Execute in TiDB        │
└──────────────┬──────────────┘
               │
               ▼
       Validate Results
```

---

# 💬 Natural Language → SQL

Five business questions were evaluated.

## 1️⃣ Loan Repayment

### Natural-Language Question

> How much of the $300,000 loan have we paid off so far?

The generated SQL needs to analyze the original loan principal and payments made toward the loan.

Conceptually:

```sql
SELECT
    l.principal_amount,
    SUM(lp.principal_portion) AS principal_paid
FROM loan AS l
JOIN loan_payment AS lp
    ON l.loan_id = lp.loan_id
GROUP BY
    l.loan_id,
    l.principal_amount;
```

This demonstrates:

* `JOIN`
* `SUM()`
* Financial aggregation
* `GROUP BY`

---

# 2️⃣ Staff License Expiration

### Natural-Language Question

> Which staff members' licenses will expire next year?

The query analyzes professional license expiration dates stored in the staff table.

Conceptually:

```sql
SELECT
    staff_id,
    first_name,
    last_name,
    license_number,
    license_expiry_date
FROM staff
WHERE YEAR(license_expiry_date) = YEAR(CURRENT_DATE) + 1;
```

This demonstrates:

* Date filtering
* `YEAR()`
* Current-date calculations
* Employee compliance tracking

---

# 3️⃣ Medical Procedure Count

### Natural-Language Question

> How many medical procedures did we perform last year?

The generated SQL counts procedure records from the previous calendar year.

Conceptually:

```sql
SELECT
    COUNT(*) AS procedures_performed
FROM procedure
WHERE YEAR(procedure_date) = YEAR(CURRENT_DATE) - 1;
```

This demonstrates:

* `COUNT()`
* Date-based filtering
* Aggregate queries

---

# 4️⃣ Insurance Providers

### Natural-Language Question

> Can we get a list of insurance companies that our patients are using?

This requires joining patient insurance records with insurance-provider information.

Conceptually:

```sql
SELECT DISTINCT
    ip.provider_name
FROM patient_insurance AS pi
JOIN insurance_provider AS ip
    ON pi.provider_id = ip.provider_id
ORDER BY ip.provider_name;
```

This demonstrates:

* Relational joins
* `DISTINCT`
* Foreign-key relationships
* Sorting

---

# 5️⃣ Upcoming Patient Visits

### Natural-Language Question

> How many patients are scheduled to visit during the next 3 months?

The query analyzes future appointments.

Conceptually:

```sql
SELECT
    COUNT(DISTINCT patient_id) AS scheduled_patients
FROM appointment
WHERE appointment_date >= CURRENT_DATE
  AND appointment_date < DATE_ADD(CURRENT_DATE, INTERVAL 3 MONTH)
  AND status = 'scheduled';
```

This demonstrates:

* Date ranges
* `DATE_ADD()`
* `COUNT(DISTINCT ...)`
* Appointment-state filtering

---

# 🧪 SQL Validation

Generating SQL is only one part of the problem.

A query can appear reasonable while still containing:

* Invalid table names
* Incorrect column names
* Incorrect JOIN relationships
* Unsupported SQL syntax
* Incorrect assumptions about the schema
* Logically incorrect filtering

For this reason, each generated query was **executed against the TiDB database**.

The workflow was:

```text
Generate SQL
     ↓
Inspect Query
     ↓
Execute in TiDB
     ↓
Check for SQL Errors
     ↓
Inspect Returned Data
     ↓
Validate Result
```

This execution-based validation is an important part of the project.

---

# 🗃️ Database Creation

The project includes a complete relational schema for the dental practice.

Example:

```sql
CREATE TABLE staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role_id INT NOT NULL,
    license_number VARCHAR(50),
    license_expiry_date DATE,
    hire_date DATE NOT NULL,
    salary DECIMAL(12, 2) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    FOREIGN KEY (role_id)
        REFERENCES staff_role(role_id)
);
```

Foreign-key relationships are used throughout the database to maintain relational integrity.

---

# 🔗 Example Relationship

Consider patient insurance:

```text
PATIENT
   │
   │ patient_id
   ▼
PATIENT_INSURANCE
   │
   │ provider_id
   ▼
INSURANCE_PROVIDER
```

This structure makes it possible to answer questions such as:

> Which insurance companies are our patients using?

without storing duplicate insurance-company information for every patient.

---

# 🧪 Synthetic Data

After creating the schema, the database was populated with synthetic records.

The synthetic data provides enough information to test queries involving:

* Patients
* Staff
* Licenses
* Appointments
* Procedures
* Insurance
* Loan payments
* Financial transactions

This allowed the AI-generated SQL to be tested against actual relational data rather than only reviewed visually.

---

# 🤖 Why Text-to-SQL?

Text-to-SQL systems attempt to bridge the gap between:

```text
Business User
     ↓
Natural Language
     ↓
Database Query
```

and:

```text
Database
     ↓
SQL
     ↓
Structured Result
```

For example, a non-technical user could ask:

```text
How many patients are scheduled for the next three months?
```

instead of manually writing:

```sql
SELECT COUNT(DISTINCT patient_id)
FROM appointment
WHERE appointment_date >= CURRENT_DATE
AND appointment_date <
    DATE_ADD(CURRENT_DATE, INTERVAL 3 MONTH);
```

The LLM acts as the translation layer between the user's intent and the relational database.

---

# ⚠️ Why Validation Matters

LLM-generated SQL should not automatically be assumed to be correct.

An LLM may generate syntactically valid SQL that:

* Uses the wrong relationship
* Misinterprets a business question
* Double-counts rows
* Uses an incorrect date range
* Assumes a nonexistent field
* Produces technically valid but logically incorrect results

This project therefore treats **query execution and result inspection as a validation step**.

```text
Natural Language
       ↓
      LLM
       ↓
Generated SQL
       ↓
Database Execution
       ↓
Result Inspection
       ↓
Validated Query
```

---

# 📁 Repository Structure

```text
ai-text-to-sql-validation/
│
├── README.md
├── .gitignore
│
├── database/
│   ├── database-requirements.txt
│   └── schema.sql
│
├── prompts/
│   ├── database-context.txt
│   ├── data-generation-prompt.txt
│   └── business-questions.txt
│
├── queries/
│   ├── 01-loan-payoff.sql
│   ├── 02-expiring-licenses.sql
│   ├── 03-procedure-count.sql
│   ├── 04-insurance-providers.sql
│   └── 05-upcoming-patients.sql
│
└── screenshots/
    ├── database-creation1.png
    ├── database-creation2.png
    ├── database-creation3.png
    ├── database-creation4.png
    ├── database-creation5.png
    ├── database-creation6.png
    ├── data-insertion.png
    ├── query-1.png
    ├── query-2.png
    ├── query-3.png
    ├── query-4.png
    ├── query-5_alternate.png
    └── query-5.png
```

---

# 📸 Screenshots

## 🗄️ Database Creation

![Database Creation](screenshots/database-creation1.png)
![Database Creation](screenshots/database-creation2.png)
![Database Creation](screenshots/database-creation3.png)
![Database Creation](screenshots/database-creation4.png)
![Database Creation](screenshots/database-creation5.png)
![Database Creation](screenshots/database-creation6.png)

## 📥 Synthetic Data Insertion

![Synthetic Data Insertion](screenshots/data-insertion.png)

## 💰 Loan Repayment Query

![Loan Repayment Query](screenshots/query-1.png)

## 🪪 Staff License Expiration Query

![Staff License Query](screenshots/query-2.png)

## 🦷 Medical Procedure Query

![Medical Procedure Query](screenshots/query-3.png)

## 🏥 Insurance Provider Query

![Insurance Provider Query](screenshots/query-4.png)

## 📅 Upcoming Patient Appointments

![Upcoming Patient Query](screenshots/query-5.png)
![Upcoming Patient Query](screenshots/query-5_alternate.png)

---

# 💡 What I Learned

Through this project, I gained hands-on experience with:

* Text-to-SQL generation using LLMs
* Translating business questions into database queries
* Prompting LLMs with database context
* Relational database design
* Creating normalized SQL tables
* Defining primary and foreign keys
* Creating database indexes
* Generating synthetic relational data
* Working with TiDB Cloud
* Executing and debugging generated SQL
* Validating LLM-generated database queries
* Writing aggregate SQL queries
* Working with SQL joins
* Performing date-based SQL analysis
* Understanding ambiguity in natural-language database questions
* Identifying potential failure modes in AI-generated SQL

---

# 🔑 Key Takeaway

The main lesson from this project is that **LLMs can dramatically simplify SQL generation, but generated queries still need database-grounded validation**.

The complete workflow is therefore not simply:

```text
English → SQL
```

but:

```text
English
   ↓
LLM
   ↓
Generated SQL
   ↓
Database Execution
   ↓
Result Validation
   ↓
Trusted Query
```

This combination of **AI-assisted generation and execution-based validation** provides a more reliable approach to using LLMs with relational databases.

---

# 👤 Author

**YOUR NAME**

* **LinkedIn:** [LinkedIn Profile](https://www.linkedin.com/in/aryansindhu/)
* **GitHub:** [GitHub Profile](https://github.com/aryansindhu8/)

---

⭐ If you found this project interesting, feel free to star the repository.
