# Lab Activity 6: openGauss

## Student

BRAEDEN JOSH V. PILARO

## Description

This laboratory activity demonstrates how to connect a Python application
to an openGauss database, create a table, insert sample records, and retrieve
filtered results.

## Tools Used

- Anaconda
- Python 3.11
- Ubuntu WSL
- Docker Desktop
- openGauss
- psycopg2
- Visual Studio Code

## Project Structure

- `src/main.py` - Main Python database program
- `sql/schema.sql` - Table creation and sample records
- `sql/sample_queries.sql` - Sample SELECT queries
- `screenshots/` - Output and terminal screenshots
- `requirements.txt` - Python dependencies

## How to Run

1. Start Docker Desktop.
2. Open Ubuntu WSL.
3. Start the openGauss container:

   ```bash
   docker start opengauss-lab6