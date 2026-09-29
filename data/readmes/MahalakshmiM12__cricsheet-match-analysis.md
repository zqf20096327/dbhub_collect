# Cricsheet Match Data Analysis (Python + SQL + Power BI)
A comprehensive cricket data analysis project that processes **4,776,439 ball-by-ball delivery records** across **T20, ODI, IPL, and TEST** formats from Cricsheet.org, performs deep SQL analysis, and creates interactive visualizations. This project demonstrates end-to-end **data engineering and analysis skills — from raw JSON parsing to a live Power BI dashboard**.

## Features
- Data Parsing: Automated JSON to structured CSV conversion using Pandas and tqdm for all four cricket formats
- Database Management: TiDB Cloud (MySQL 8 compatible) with optimized schema design and Foreign Key relationships
- SQL Analysis: 20 advanced analytical queries covering window functions, ranking, joins, and subqueries
- EDA Visualizations: 10 charts using Matplotlib, Seaborn, and Plotly (9 static PNG + 1 interactive HTML)
- Power BI Dashboard: 6 interactive visuals with a match-type slicer for T20 · ODI · IPL · TEST filtering
- Performance Optimized: Bulk inserts with chunksize=5000 for efficient 4.77M row loading

## Tech Stack
| Technology | Purpose |
|------------|----------|
| Python 3.10+ | Core Programming Language |
| Pandas | Data Processing & Analysis |
| SQLAlchemy | ORM & Database Management |
| PyMySQL | Database Connectivity |
| mysql-connector-python | Direct MySQL Connection |
| Matplotlib | Static Visualizations |
| Seaborn | Statistical Charts |
| Plotly | Interactive Visualizations |
| TiDB Cloud | MySQL Compatible Cloud Database |
| tqdm | Progress tracking during JSON parsing |

## Dataset Summary
| Format | Matches | Deliveries |
|---------|---------:|-----------:|
| T20 | 4,991 | 1,129,134 |
| ODI | 3,085 | 1,632,502 |
| IPL | 1,169 | 278,205 |
| TEST | 899 | 1,736,598 |
| **Total** | **10,144** | **4,776,439** |

## Data Source
The cricket data used in this project is sourced from **Cricsheet.org**, which provides ball-by-ball match data in JSON format. It provides JSON format match data for international and domestic cricket. You can download the raw JSON files from cricsheet.org/downloads and place them inside the data_files/ folder before running the pipeline.

### Download Dataset
https://cricsheet.org/downloads/

## How to Run this Project
- git clone https://github.com/MahalakshmiM12/cricsheet-match-analysis.git
- cd cricsheet-match-analysis
- pip install -r requirements.txt
- python cricsheet_data.py
- python db.py
- python bulk_insert_data.py
- python eda.py

## Power BI Dashboard
The complete Power BI dashboard is available in:
cricket_dashboard.pbix
https://drive.google.com/drive/folders/1JAw6hyil2TiAvxzqbFUbh_ic3Xq--iGa?usp=drive_link
