# TiCard - TiDB Cardinality Estimation

This project demonstrates how to use machine learning models to improve the cardinality estimation of the TiDB database. It compares the predictions of TabPFN, Gradient Boosting Regressor (GBR), and Neurocard with TiDB's default optimizer estimates.

## Project Structure

```bash
.
├── docker-compose.yml      # Docker compose file for TiDB
├── paper-db.md             # The plan for this project
├── pyproject.toml          # Project dependencies
├── README.md               # This file
├── scripts/
│   ├── download_tpch.sh    # Script to download TPC-H data
│   └── load_tpch.sh        # Script to load TPC-H data into TiDB
└── src/
    └── ticard/
        ├── __init__.py
        ├── config.py           # Configuration for database and model
        ├── dataset.py          # Data loading and preparation
        ├── features.py         # Feature extraction from query plans
        ├── main.py             # Main script to run the experiment
        └── model.py            # Model training and evaluation
```

## Setup

### 1. Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [Docker](https://www.docker.com/)

### 2. Initialize the project

```bash
uv sync
```

> **Note:**
>
> If you want to load the test dataset and make the query plan and execution plan, you need to start the TiDB, prepare datasets and load the datasets. But if you just want to run the TiCard, we have already prepared the query plan we ran previously in `query_plans`. So you can run the TiCard without setting the database.

### 3. (Optional) Start TiDB

```bash
docker-compose up -d
```

Wait a few minutes for TiDB to be ready. Or you can use the [TiDB Cloud](https://tidbcloud.com/) as well.

### 4. (Optional) Prepare TPC-H dataset

Download and load the TPC-H dataset.

```bash
cd scripts/tpch

chmod +x download_tpch.sh
./download_tpch.sh

chmod +x load.sh
./load.sh

cd -
```

### 5. (Optional) Prepare JOB dataset

```bash
cd scripts
git clone --recurse-submodules https://github.com/Icemap/join-order-benchmark.git

cd join-order-benchmark/csv_files/
wget https://event.cwi.nl/da/job/imdb.tgz
tar -xvzf imdb.tgz
cd ..

./split_and_load_data.sh
cd ../..
```

## Run the experiment

Execute the main script to run the entire pipeline: data extraction, feature engineering, model training, and evaluation.

```bash
# Run with all algorithms (TabPFN, GBR, Neurocard)
uv run python -m ticard.main

# Run with specific algorithms
uv run python -m ticard.main -a tabpfn
uv run python -m ticard.main -a gbr
uv run python -m ticard.main -a neurocard

# Run with multiple algorithms
uv run python -m ticard.main -a tabpfn -a gbr
```

The script will output a comparison of the cardinality estimation Q-Error for:

- **TiDB's default optimizer estimates** (baseline)
- **TabPFN**: Tabular Prior-Fitted Network
- **GBR**: Gradient Boosting Regressor
- **Neurocard**: Deep autoregressive model (MADE) for cardinality estimation

### Algorithm Details

- **TabPFN**: A transformer-based model pre-trained on synthetic tabular data
- **GBR**: Gradient Boosting Regressor with 200 estimators
- **Neurocard**: MADE (Masked Autoencoder for Distribution Estimation) architecture from the [Neurocard paper](https://github.com/neurocard/neurocard)
