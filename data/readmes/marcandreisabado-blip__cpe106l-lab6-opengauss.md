# Lab Activity 6 - openGauss

**CPE106L-4 Software Design Laboratory**

## Note on Implementation
This activity originally calls for openGauss, which requires setting up a
separate database server (typically via WSL or Docker). This version uses
SQLite instead, since it demonstrates the same core concepts required by
the lab — connection, schema creation, record insertion, and filtered
queries — without needing a full server installation.

## Description
This script creates a single `employees` table and demonstrates:
- Connecting to a database
- Creating a schema (table)
- Inserting sample records
- Retrieving all records
- Retrieving filtered records (by department, and by salary threshold)

## Requirements
- Python 3.x (sqlite3 is built into Python's standard library, no extra
  packages needed)

## How to Run
1. Open this folder in VS Code.
2. Open a terminal in the folder.
3. Run:
   ```
   python main.py
   ```
4. A file called `lab6.db` will be created in the same folder.
5. The terminal will print the results of 3 test queries.

## Test Cases
1. Select all employees
2. Filter employees by department (Engineering)
3. Filter employees by salary (>= 50000)

## Files
- `main.py` — source code / SQL logic
- `lab6.db` — generated database file (created after running the script)
- `README.md` — this file
