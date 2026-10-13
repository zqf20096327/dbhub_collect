# 🌦️ Automated Weather ETL Pipeline: Data Validation & Quality Assurance

An automated end-to-end ETL pipeline that extracts live weather data from an API, validates and cleans it with Python & Pandas, and loads it into a TiDB Cloud (MySQL) database. The pipeline runs automatically every hour using GitHub Actions, with a focus on **data accuracy, data quality, and reliable automated runs**.

---

## 🚀 Project Overview

Because this pipeline runs unattended every hour, data quality and reliability matter: bad API responses, wrong data types, or failed loads must not silently corrupt the database. The workflow below shows where data is checked at each stage.

```
[Weather API]
     │
     ▼ (Extract)       → API response and JSON structure checks
[Python / Requests]
     │
     ▼ (Transform)     → Data type, format, and missing value checks
[Pandas Cleaning & Formatting]
     │
     ▼ (Load)          → Verify records inserted correctly
[TiDB Cloud MySQL]
     ▲
     └── Orchestrated hourly via GitHub Actions (cron)
```

### Key Features
* **Automated hourly runs:** GitHub Actions cron schedule, with every run visible in the Actions logs for monitoring and debugging.
* **Data transformation & validation:** parses JSON, fixes data types, and splits date/time fields using Pandas.
* **Cloud database integration:** securely loads into a cloud-hosted TiDB (MySQL) instance.
* **Secure configuration:** API keys and database credentials are stored in GitHub Repository Secrets, not in code.

---

## ✅ Quality Checks Across the Pipeline

| Stage | What to verify |
|-------|----------------|
| **Extract** | API returns a successful response and the JSON contains the expected fields |
| **Transform** | Correct data types, no unexpected nulls, date and time split correctly |
| **Load** | Records land in the database with the right values and no duplicates |
| **Automation** | Hourly workflow runs on schedule; failed runs are visible in GitHub Actions logs |

### Sample Validation Queries
Run these on the database after a pipeline run (adjust table and column names to your schema):

```sql
-- 1. Confirm data is arriving: latest records
SELECT * FROM weather_data ORDER BY date DESC, time DESC LIMIT 10;

-- 2. Duplicate check: should return no rows
SELECT city, date, time, COUNT(*)
FROM weather_data
GROUP BY city, date, time
HAVING COUNT(*) > 1;

-- 3. Null check on key columns: should return 0
SELECT COUNT(*) FROM weather_data WHERE temperature IS NULL;

-- 4. Range sanity check: values should look realistic
SELECT MIN(temperature), MAX(temperature) FROM weather_data;
```

---

## 🛠️ Tech Stack

* **Language:** Python 3.10
* **Data Processing:** Pandas
* **Database Connectivity:** SQLAlchemy, PyMySQL
* **Database:** TiDB Cloud (MySQL-compatible)
* **Automation / CI-CD:** GitHub Actions
* **API Testing & Data:** Live Weather API (JSON)

---

## 📂 Project Structure

```
live-weather-project/
│
├── .github/
│   └── workflows/
│       └── weather_etl.yml      # GitHub Actions automation workflow
│
├── extract.py                   # API data fetching
├── transform.py                 # Pandas cleaning and structuring
├── load.py                      # Database load script
├── main.py                      # Master pipeline script
├── config.py                    # Environment and variable setup
└── README.md                    # Project documentation
```

---

## ⚙️ Setup & Execution

1. **Clone the repository**
   ```bash
   git clone https://github.com/rohittinker/live-weather-project.git
   cd live-weather-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   Create a `.env` file in the root directory and add your `API_KEY` and database credentials.

4. **Run the pipeline**
   ```bash
   python main.py
   ```

5. **Verify the load**

   Run the validation queries above to confirm records, duplicates, nulls, and value ranges.

---

## 📊 Dashboard Analytics

![Live Weather Dashboard](assets/historical-climate-Analysis.png)

![Real-time Trend Analysis](assets/realtime-weather-trend&Variance.png)

![Historical Baseline](assets/historical-climate-Analysis.png)

![Comparison Summary](assets/live-hist-comparision.png)
