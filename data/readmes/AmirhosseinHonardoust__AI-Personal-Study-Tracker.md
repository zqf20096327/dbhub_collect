## AI-Powered Personal Study Tracker

An intelligent productivity analytics app built with **Python**, **SQLite**, **Machine Learning**, and **Streamlit**.  
It empowers learners to track, visualize, and improve their study habits while using AI to estimate their expected productivity.
  
---

## Overview

The **AI-Powered Personal Study Tracker** transforms daily study logs into actionable insights.  
It leverages a **Random Forest Regressor** to model productivity based on mood, distractions, study duration, caffeine intake, and more.

You can:
- Log study sessions (with mood, focus level, and caffeine)
- Analyze study performance trends and patterns
- Estimate expected productivity before studying
- View aggregated insights and KPIs

---

## Project Structure

```
ai-study-tracker/
├── app/
│   └── streamlit_app.py         # Main Streamlit dashboard
├── src/
│   ├── generate_sample.py       # Generate synthetic study sessions
│   ├── ingest.py                # Load CSV into SQLite
│   ├── train_model.py           # Train RandomForestRegressor
│   └── utils.py                 # Helper functions
├── sql/
│   └── schema.sql               # Database schema
├── data/
│   ├── sessions.csv             # Study session data
│   └── study.db                 # SQLite database
├── models/
│   └── pipeline.joblib          # Saved ML model
└── README.md
```

---

## Dashboard Preview

### Productivity Overview
<img width="1342" height="665" alt="Screenshot 2025-10-29 at 14-50-23 AI Study Tracker" src="https://github.com/user-attachments/assets/c820a28f-e44d-4503-b475-bed81e5cabc7" />

### Session Log and Estimator
<img width="1364" height="644" alt="Screenshot 2025-10-29 at 14-51-54 AI Study Tracker" src="https://github.com/user-attachments/assets/1f61d191-8200-46e2-b199-152c24032d62" />

---

## Quickstart

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-study-tracker.git
cd ai-study-tracker

# Set up a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python src/generate_sample.py --days 28 --sessions_per_day 2 --out data/sessions.csv

# Import to SQLite
python src/ingest.py --csv data/sessions.csv --db data/study.db --schema sql/schema.sql

# Train the ML model
python src/train_model.py --db data/study.db --out models/pipeline.joblib

# Launch the dashboard
streamlit run app/streamlit_app.py
```

---

## Tech Stack

| Layer | Technology |
|:--|:--|
| **Frontend** | Streamlit + Plotly |
| **Backend** | SQLite |
| **ML Model** | RandomForestRegressor (scikit-learn) |
| **Data Handling** | pandas, SQLAlchemy |
| **Language** | Python 3.10+ |

---

## Key Features

- Log daily study sessions with mood, distractions, caffeine, and techniques  
- Predict productivity with ML model  
- Visualize time trends and subject-wise averages  
- Local SQLite database (portable and private)  
- Add new sessions interactively via the Streamlit sidebar  
- Estimate productivity in real-time  

---

## Data Schema

| Column | Description |
|:--|:--|
| `date` | Session date (YYYY-MM-DD) |
| `start_time` / `end_time` | HH:MM 24h format |
| `duration_min` | Computed from start–end times |
| `subject` | Math, Physics, CS, Biology, History |
| `technique` | Pomodoro, Active Recall, etc. |
| `distractions` | Number of interruptions |
| `mood` | 1-5 scale |
| `caffeine_mg` | Caffeine intake (mg) |
| `productivity` | Self-rated (1-5) |

---

## Machine Learning

The app uses **RandomForestRegressor** from `scikit-learn` trained on historical study logs.

**Features used for prediction:**
- Duration (minutes)
- Subject
- Technique
- Distractions
- Mood
- Caffeine (mg)

**Target:**
- Productivity (1–5 scale)

The model is modular, you can upgrade it to **XGBoost** or **Neural Networks**.

---

## Example Insights

- Productivity tends to **increase with mood** and **decrease with distractions**  
- “Active Recall” and “Spaced Repetition” correlate with higher productivity  
- Optimal caffeine range: 100–200 mg  

---

## UI Highlights

- Clean, interactive Streamlit interface  
- Real-time productivity estimation  
- KPI tiles for total minutes, average mood, and average productivity  
- Line chart: *Study Minutes Over Time*  
- Bar chart: *Average Productivity by Subject*  
