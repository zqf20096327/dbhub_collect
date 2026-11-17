# Database Quality Investigator

A Python-based database quality and security investigation project that uses MySQL and TiDB Cloud to identify data quality issues and unusual database activity using machine learning.

## Project Overview

Database Quality Investigator analyzes database records to identify data quality problems and investigate potentially unusual database activity.

The project combines data profiling, data cleaning, audit logging, and machine learning-based anomaly detection.

It supports both local MySQL and TiDB Cloud, allowing the application to work with a local database or a cloud-hosted database.

## Key Features

### 1. Database Connection
- Connects Python applications to MySQL and TiDB Cloud.
- Uses SQLAlchemy for database operations.
- Supports switching between local and cloud databases.
- Loads database configuration from environment variables.
- Uses SSL/TLS certificates for secure TiDB Cloud connections.

### 2. Data Profiling
- Analyzes database records and columns.
- Identifies missing values.
- Detects duplicate records.
- Reports column data types.

### 3. Data Quality Detection
- Identifies missing student information.
- Detects duplicate student IDs.
- Checks invalid email addresses.
- Identifies suspicious age values.

### 4. Audit Logging
- Records database activities.
- Captures usernames, IP addresses, actions, and timestamps.
- Classifies records as REAL or TEST.

### 5. Data Preprocessing
- Cleans audit log data.
- Handles duplicate records and missing values.
- Extracts time-based features.
- Preserves record source information.

### 6. Security Anomaly Detection
- Identifies high-impact database actions.
- Analyzes activity by username and IP address.
- Uses Isolation Forest to flag unusual activity.
- Generates security investigation reports.

### 7. Data Quality Recommendations
- Provides suggestions for missing values.
- Identifies duplicate records and IDs.
- Highlights invalid email addresses.
- Recommends verification of suspicious age values.

## Technologies Used

- Python
- MySQL
- TiDB Cloud
- Pandas
- SQLAlchemy
- Scikit-learn
- Isolation Forest
- PyMySQL
- Python-dotenv

## Project Structure

```text
DatabaseQualityInvestigator/
│
├── .venv/
├── certs/
│   └── isrgrootx1.pem
│
├── database/
│   ├── __init__.py
│   └── audit_logger.py
│
├── preprocessing/
│   └── data_cleaning.py
│
├── data/
│   ├── processed/
│   └── reports/
│
├── db_connection.py
├── detection.py
├── profiling.py
├── recommendations.py
├── test_tidb_connection.py
├── create_cloud_tables.py
├── migrate_to_tidb.py
├── .env
├── .gitignore
└── README.md
```

## Installation

1. Clone or download the project.
2. Open the project folder in a terminal.
3. Create a virtual environment.

```bash
python -m venv .venv
```

4. Install the required packages.

```bash
pip install pandas sqlalchemy pymysql python-dotenv scikit-learn
```

5. Configure the database credentials in a `.env` file.

## Database Configuration

The project supports two database modes.

### Option 1: Local MySQL

Configure the following environment variables:

```text
DB_MODE=local
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=your_database
DB_PORT=3306
```

### Option 2: TiDB Cloud

Configure the following environment variables:

```text
DB_MODE=cloud
TIDB_HOST=your_tidb_host
TIDB_PORT=4000
TIDB_USER=your_tidb_username
TIDB_PASSWORD=your_tidb_password
TIDB_DATABASE=sys
TIDB_SSL_CA=certs/isrgrootx1.pem
```

The application connects to the `database_quality_investigator` database in TiDB Cloud.

The `TIDB_DATABASE` variable is retained for the connection test configuration; the main application uses `database_quality_investigator`.

Download the appropriate CA certificate and place it inside the `certs` folder.

**Important:** Never upload your `.env` file or database passwords to GitHub.

## Database Migration

The project includes scripts for setting up and migrating data to TiDB Cloud.

1. Test the TiDB Cloud connection:

```bash
python test_tidb_connection.py
```

2. Create the cloud database tables:

```bash
python create_cloud_tables.py
```

3. Migrate existing local MySQL records:

```bash
python migrate_to_tidb.py
```

The migration script checks that the cloud tables are empty before copying records.

The migration preserves the local MySQL database.

## Running the Project

Run commands from the project root directory.

### 1. Data Profiling

```bash
python profiling.py
```

### 2. Data Quality Recommendations

```bash
python recommendations.py
```

### 3. Audit Logging

```bash
python -m database.audit_logger
```

Note: Running the audit logger's sample script inserts additional TEST records.

### 4. Audit Log Preprocessing

```bash
python -m preprocessing.data_cleaning
```

### 5. Data Quality and Security Detection

```bash
python detection.py
```

Run preprocessing before detection so that the cleaned audit log CSV file is available.

On Windows, if virtual environment activation is unavailable, commands can be run using:

```powershell
.\.venv\Scripts\python.exe profiling.py
```

For the preprocessing module:

```powershell
.\.venv\Scripts\python.exe -m preprocessing.data_cleaning
```

## Investigation Reports

The security investigation report is generated at:

```text
data/reports/security_investigation_report.csv
```

The report includes:
- Anomaly status
- Anomaly scores
- Activity details
- Record source information

## Record Classification

| Source | Description |
|---|---|
| REAL | Actual audit records |
| TEST | Simulated records created for testing |

## Machine Learning

The project uses the Isolation Forest algorithm from Scikit-learn to identify unusual database activity.

Anomaly detection results are indicators for further investigation and do not independently establish malicious activity.

## Future Enhancements

- Interactive investigation dashboard.
- Real-time security monitoring.
- Advanced anomaly detection models.
- Automated investigation recommendations.
- More detailed audit analytics.

## Author

Developed as a Python, MySQL, and TiDB Cloud database investigation project.