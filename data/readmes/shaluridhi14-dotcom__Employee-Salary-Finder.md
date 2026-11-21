# Employee Salary Finder

A web-based application that helps users find employee salary information using a Flask backend and TiDB Cloud database.

## Features

- Find the highest-paid employee.
- Find the lowest-paid employee.
- Display the top 5 highest-paid employees.
- Calculate the average salary of all employees.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** TiDB Cloud (MySQL compatible)
- **Database Connector:** PyMySQL
- **API Communication:** REST APIs

## Project Structure

```text
Employee-Salary-Finder/
│
├── app.py
├── db.py
├── test_db.py
├── index.html
├── style.css
├── script.js
├── .gitignore
└── README.md
```

## Database

Database: `employee_salary_db`

Table: `employee`

Columns:
- emp_id
- emp_name
- department
- salary

## API Endpoints

| Endpoint | Description |
|---|---|
| `/highest-salary` | Highest-paid employee |
| `/lowest-salary` | Lowest-paid employee |
| `/top-5-employees` | Top 5 highest-paid employees |
| `/average-salary` | Average employee salary |

## How to Run Locally

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
pip install flask flask-cors pymysql python-dotenv
```

4. Configure your `.env` file with your TiDB Cloud credentials and CA certificate path.
5. Start the Flask backend:

```bash
python app.py
```

6. Open `index.html` using VS Code Live Server.

## Security

Database credentials and certificate files are kept outside the public repository using `.gitignore`.

## Author

Developed as a DBMS Mini Project.