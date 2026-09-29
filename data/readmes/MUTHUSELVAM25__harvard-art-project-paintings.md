# Harvard Art Project – Paintings Classification

This project demonstrates API integration and data engineering using the Harvard Art Museums public API for the "Paintings" classification. The workflow fetches painting data, processes artifact metadata, media, and color information, and loads the results into TiDB Cloud MySQL tables for analysis, dashboarding, or further applications.

## Features

- Fetches painting artifacts from the Harvard Art Museums API (requires free API key)
- Extracts and organizes metadata, media, and color details into CSV files
- Inserts structured data into TiDB MySQL tables, ready for SQL queries/analysis
- Modular, well-commented Python scripts and Jupyter notebook
- Ready for future expansions (multiple classifications, Streamlit dashboard, etc.)

## Getting Started

1. **Clone the repository** and install dependencies (see requirements.txt if provided).
2. **Obtain a Harvard Art Museums API key** from [api.harvardartmuseums.org](https://api.harvardartmuseums.org).
3. **Edit the notebook or script** to include your API key.
4. **Run the notebook** to fetch, process, and save the data.
5. **Configure MySQL credentials** in the code before loading data to your own TiDB Cloud database.

## Repository Contents

- `HARVARD-S_PROJECT1.ipynb` – Main notebook for data collection and processing
- Example CSVs: `artifact_metadata.csv`, `artifact_media.csv`, `artifact_colors.csv`
- SQL schema/code for creating the required tables and inserting entries

## Example Workflow

- Fetch first 2,500 painting records with images from the Harvard Art Museums API
- Build DataFrames (pandas) for artifact metadata, media count, and color analysis
- Export DataFrames to CSV
- Connect to TiDB Cloud MySQL, create corresponding tables, and insert prepared data

## Next Steps

- Expand for 5+ classifications in future versions
- Add Streamlit UI visualization

---

*This repository is built as a learning and data-interfacing project for the Harvard Art Museums API. Contributions and feedback are welcome!*



