<div align="center">

# Expense Tracker System
   
</div>

A simple command-line Expense Tracker built with Python and SQLite.

This application helps users record, view, delete, and summarize their expenses. Expense data is stored locally in a SQLite database.

## Features

- Add new expenses with amount, category, description, and date
- View all saved expenses
- Delete expenses by ID
- View a monthly expense summary by category
- Store data locally using SQLite
- Validate user input before saving expenses

## Requirements

- Python 3.x
- matplotlib

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/codewithdhruba01/ExpenseTrackerSystem.git
cd ExpenseTrackerSystem
````

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows CMD:

```bash
.venv\Scripts\activate
```

On Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install matplotlib
```

## Usage

Run the application:

```bash
python expense.py
```

After running the app, you will see this menu:

```text
Expense Tracker
1. Add Expense
2. View Expenses
3. Delete Expense
4. View Monthly Summary
5. Exit
Enter your choice:
```

## Adding an Expense

When adding an expense, enter the following information:

```text
Enter expense amount:
Enter expense category:
Enter expense description:
Enter expense date (YYYY-MM-DD):
```

Example:

```text
Enter expense amount: 100
Enter expense category: Food
Enter expense description: Lunch
Enter expense date (YYYY-MM-DD): 2026-05-13
Expense added successfully!
```

## Input Rules

When adding an expense:

* Amount must be greater than `0`
* Category cannot be empty
* Description cannot be empty
* Date must follow the `YYYY-MM-DD` format

Example of a valid date:

```text
2026-05-13
```

## Database

The application uses SQLite for local data storage.

When you run the app, it automatically creates a database file named:

```text
expenses.db
```

This file stores your expense records locally.

## Project Structure

```text
ExpenseTrackerSystem/
│
├── expense.py      # Main application file
├── README.md       # Project documentation
└── expenses.db     # Local database file, created automatically after running the app
```

## Notes

* Do not manually create the database file; the app creates it automatically.
* The database file is for local use and should usually not be committed to GitHub.
* If you want to reset your local data, delete `expenses.db` and run the app again.
