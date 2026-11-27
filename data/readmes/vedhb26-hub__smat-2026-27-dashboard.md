# SMAT 2026/27 Dashboard

Streamlit dashboard for the Syed Mushtaq Ali Trophy 2026/27 (Indian domestic T20),
served from a live MySQL-compatible TiDB Cloud database.

- Batting / bowling leaderboards with team filters and player drill-downs
- Full match scorecards
- Group-wise points table
- Data refreshed daily from Cricsheet ball-by-ball JSON

## Stack
- Streamlit + pandas + PyMySQL
- TiDB Cloud Starter (free tier) database, loaded from https://cricsheet.org/downloads/sma_male_json.zip

## Run locally
pip install -r requirements.txt
Add your DB credentials to .streamlit/secrets.toml (see Streamlit Cloud app secrets for the format), then:
streamlit run app.py

Data © Cricsheet — credit required when reusing the data.
