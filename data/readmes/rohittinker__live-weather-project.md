# 🌦️ Automated Live Weather ETL Pipeline

An automated, production-ready end-to-end data engineering pipeline that extracts real-time weather data via API, transforms it using Python & Pandas, and loads it into an online TiDB Cloud (MySQL) database. The entire process is fully automated to run every hour using GitHub Actions.

---

## 🚀 Project Overview

This project demonstrates a complete ETL (Extract, Transform, Load) workflow built for scalability and cloud deployment. Instead of running scripts manually, the pipeline is fully self-sustaining on cloud infrastructure.



[Data Source: Weather API]
│
▼ (Extract)
[Python Script / Requests]
│
▼ (Transform)
[Pandas Data Cleaning & Formatting]
│
▼ (Load)
[TiDB Cloud MySQL Database] 💻 (Orchestrated Hourly via GitHub Actions)

### Key Features:
* **Automated Orchestration:** Runs on a cron schedule every hour via GitHub Actions.
* **Cloud Database Integration:** Securely connects to a cloud-hosted TiDB MySQL instance.
* **Robust Data Transformation:** Handles data parsing, data type formatting, and separates date/time coordinates dynamically using Pandas.
* **Security First:** Environment variables and database credentials are fully secured using GitHub Repository Secrets.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10
* **Data Manipulation:** Pandas
* **Database Connectivity:** SQLAlchemy, PyMySQL
* **Database:** TiDB Cloud (MySQL-compatible)
* **Automation/CI-CD:** GitHub Actions
* **API:** Live Weather API (JSON Data Extraction)

---

## 📂 Project Structure
```
text
live-weather-project/
│
├── .github/text
│   └── workflows/
│       └── weather_etl.yml      # GitHub Actions automation workflow
│
├── extract.py                   # API Data Fetching logic
├── transform.py                 # Pandas cleaning and structuring
├── load.py                      # Database push script
├── main.py                      # Master pipeline execution script
├── config.py                    # Environment & variable setup
└── README.md                    # Project documentation

```

## 🛠 Setup & Execution
1. **Clone the repository:**
```bash
   git clone [https://github.com/rohittinker/live-weather-project.git](https://github.com/rohittinker/live-weather-project.git)
   cd live-weather-project
```
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   
3. **Configure Environment:**
   ```
   Create a .env file in the root directory.
   Add your API_KEY and DB_CREDENTIALS (if applicable).
   
4. **Run the pipeline:**
   ```
   python main.py

### Dashboard Analytics

![Live Weather Dashboard](assets/historical-climate-Analysis.png)

![Real-time Trend Analysis](assets/realtime-weather-trend&Variance.png)

![Historical Baseline](assets/historical-climate-Analysis.png)

![Comparison Summary](assets/live-hist-comparision.png)
