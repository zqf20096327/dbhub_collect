# OceanBase Multi-Model Demo for GenAI Agents

This project demonstrates OceanBase's multi-model capabilities for GenAI agents. It showcases how OceanBase can handle different data types (relational, vector, geospatial, JSON, full-text) in a single database, making it an ideal solution for GenAI applications that need to query diverse data sources.

## Key Features

- **Vector Similarity Search**: Store and query vector embeddings for semantic search
- **Geospatial Data**: Perform location-based queries with spatial functions
- **JSON Data**: Store and query semi-structured data with JSON functions
- **Full-Text Search**: Perform keyword-based searches with relevance ranking
- **Relational Data**: Use traditional SQL for structured data
- **Combined Multi-Model Queries**: Mix all data types in a single query

## Why This Matters for GenAI Agents

GenAI agents often need to access and combine data from multiple sources and formats. OceanBase's multi-model capabilities allow agents to:

1. **Simplify Architecture**: Use a single database instead of multiple specialized databases
2. **Reduce Latency**: Avoid network hops between different databases
3. **Improve Performance**: Execute complex queries efficiently in a single operation
4. **Enhance Capabilities**: Combine different query types for more powerful results
5. **Streamline Development**: Use a single SQL interface for all data access

## Demo Contents

- `run_demo.py`: Menu-driven demo launcher (interactive menu, or `--batch --component {setup,vector,mcp,all}` mode). Its subprocess calls target `setup_database.py`, `bedrock_vector_demo.py`, and `setup_database_mcp.py`, all three of which are included in this repo (see below).
- `setup_database.py`: Connects directly to OceanBase (via `mysql-connector-python`, using the `OB_*` variables from `.env`) and creates + populates two tables: `unified_properties` (queried by `run_family_friendly_query.py` and `run_luxury_waterfront_query.py`) and `property_listings` (queried by `interactive_mcp_demo.py`). Supports `--dry-run` to print every SQL statement without opening a connection.
- `bedrock_vector_demo.py`: Calls Amazon Bedrock's Titan Text Embeddings model (via `boto3`, using the `AWS_*` variables from `.env`) to generate real vector embeddings for each property's `description`, stores them in `unified_properties.embedding` (a `VECTOR(1024)` column), and runs a real `VECTOR_DISTANCE` nearest-neighbor search. This is the upgrade path from the simulated `CASE WHEN ... LIKE` vector scoring used elsewhere in this repo to real embeddings. Supports `--dry-run` to print the exact Bedrock/SQL calls without making them.
- `setup_database_mcp.py`: Sets up the same `unified_properties` schema/data as `setup_database.py`, but through the OceanBase MCP tool interface (`mcp_tools.use_mcp_tool()`) instead of a direct database connection — reads `MCP_SERVER_NAME`/`MCP_TOOL_NAME` from `.env`, matching the pattern already used by `interactive_mcp_demo.py` and the two `run_*_query.py` scripts.
- `mcp_tools.py`: Defines `use_mcp_tool()`, a self-contained simulated OceanBase MCP client that returns pattern-matched sample data for the queries in this repo — it does not open a real database connection. `setup_database_mcp.py` and the query scripts below all call through this module.
- `interactive_mcp_demo.py`: Standalone interactive CLI (`MCPDemo` class) with a 6-option menu that walks through investment, JSON/amenities, full-text, geospatial, and vector-similarity queries against a sample `real_estate_investments` schema (`property_listings` table).
- `run_family_friendly_query.py`: Single-run example that builds and explains one combined multi-model query (SQL + JSON + geospatial + full-text + simulated vector scoring) to find family-friendly homes under $800,000 in San Francisco.
- `run_luxury_waterfront_query.py`: Single-run example that builds, executes (via `mcp_tools.use_mcp_tool`), and explains a combined multi-model query for luxury waterfront properties with a pool and home theater within 10 miles of Seattle.
- `setup.sh`: Shell script that creates a Python virtual environment, installs `requirements.txt`, copies `.env.example` to `.env` if it doesn't already exist, and checks whether the OceanBase MCP server package is reachable via `npx`.
- `docs/hands_on_lab_guide.md`: Step-by-step guide for the hands-on lab.
- `docs/setup_guide.md`: Instructions for setting up the demo environment.

## Prerequisites

- Python 3.7+
- To explore `interactive_mcp_demo.py`, `run_family_friendly_query.py`, and `run_luxury_waterfront_query.py` with sample data: nothing extra — `mcp_tools.py` simulates MCP responses locally, so these scripts run out of the box.
- To run `setup_database.py` or `setup_database_mcp.py` for real: a live OceanBase database, reachable using the `OB_*` variables in `.env` (see `.env.example`). For the MCP path, also point `mcp_tools.use_mcp_tool()` at a real OceanBase MCP server (e.g. `@modelcontextprotocol/server-oceanbase`, checked for by `setup.sh`).
- To run `bedrock_vector_demo.py` for real: an AWS account with Bedrock access to `amazon.titan-embed-text-v2:0`, plus `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_REGION` in `.env`.

> Every script that hits a real backend (`setup_database.py`, `bedrock_vector_demo.py`) supports `--dry-run` so you can inspect the exact SQL/Bedrock calls it would make without a live connection or credentials.

## Setup Instructions

1. Clone this repository:
   ```
   git clone https://github.com/zytbeyond/OceanbaseMultimodelDemo.git
   cd OceanbaseMultimodelDemo
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env` file:
   ```
   # OceanBase connection details
   OB_HOST=<YOUR_OB_HOST>              <!-- PLACEHOLDER: default localhost -->
   OB_PORT=<YOUR_OB_PORT>               <!-- PLACEHOLDER: default 2881 -->
   OB_USER=<YOUR_OB_USER>                <!-- PLACEHOLDER: default root -->
   OB_PASSWORD=<YOUR_OB_PASSWORD>        <!-- PLACEHOLDER: replace with your actual password -->
   OB_DATABASE=<YOUR_OB_DATABASE>        <!-- PLACEHOLDER: default test -->

   # MCP configuration (if using MCP)
   MCP_SERVER_NAME=oceanbase
   MCP_TOOL_NAME=execute_sql

   # AWS Bedrock credentials (for vector embeddings)
   AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY>       <!-- PLACEHOLDER: Replace with your AWS access key -->
   AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_KEY>   <!-- PLACEHOLDER: Replace with your AWS secret key -->
   AWS_REGION=us-east-1
   ```

4. Run the setup script (creates the virtual environment, installs dependencies, and creates `.env` from `.env.example` if needed):
   ```
   ./setup.sh
   ```

5. Run one of the demo scripts:
   ```
   python run_family_friendly_query.py
   # or
   python run_luxury_waterfront_query.py
   # or
   python interactive_mcp_demo.py
   ```
   These three run out of the box against simulated sample data — no live OceanBase instance is required.

6. To run against a real OceanBase instance and/or generate real vector embeddings:
   ```
   python setup_database.py          # direct connection: create tables + load sample data
   python bedrock_vector_demo.py     # generate real Bedrock embeddings for the sample data
   python setup_database_mcp.py      # same setup, but through the OceanBase MCP tool interface
   ```
   Or drive all of this from the menu-driven launcher:
   ```
   python run_demo.py
   # or
   python run_demo.py --batch --component all
   ```

## Running the Demo with MCP

The included `mcp_tools.py` module defines `use_mcp_tool()`, a lightweight stand-in for a real OceanBase MCP client — it returns pre-canned, pattern-matched results so the multi-model query scripts in this repo run without a live server. `setup_database_mcp.py` calls through the same module to create and populate `unified_properties`. To integrate with a real OceanBase MCP server instead:

1. Install and start the OceanBase MCP server (`setup.sh` checks for `@modelcontextprotocol/server-oceanbase` via `npx`)
2. Point `mcp_tools.use_mcp_tool()` at your real MCP client instead of the simulated responses
3. Run:
   ```
   python setup_database_mcp.py
   ```
   to create real tables/data through MCP, then run one of the query scripts, e.g.:
   ```
   python interactive_mcp_demo.py
   ```

## Generating Real Vector Embeddings with Bedrock

By default, the query scripts in this repo simulate vector similarity with a `CASE WHEN ... LIKE` scoring expression instead of calling a real embedding model. `bedrock_vector_demo.py` shows the upgrade path:

1. Run `python setup_database.py` first to create `unified_properties` with an empty `VECTOR(1024)` `embedding` column
2. Run `python bedrock_vector_demo.py` to call Amazon Bedrock (`amazon.titan-embed-text-v2:0`), embed each property's `description`, store the vectors, and run a real `VECTOR_DISTANCE` nearest-neighbor search
3. Use `--dry-run` on either script to inspect the exact calls without touching a real database or AWS account

## Demo Walkthrough

Each runnable script demonstrates a combined multi-model query against a properties table that mixes:

1. **Relational data**: standard SQL filtering (price, bedroom count) and functions like `SUBSTRING`
2. **JSON data**: `JSON_EXTRACT()` / `JSON_CONTAINS()` over a `features`/`amenities` JSON column
3. **Geospatial data**: `ST_Distance()`, `ST_Contains()`, `ST_Buffer()`, `ST_GeomFromText()` for radius/proximity searches
4. **Full-text / keyword matching**: `MATCH() AGAINST()` (in `interactive_mcp_demo.py`) or `LIKE`-based keyword filters (in the two `run_*_query.py` scripts)
5. **Vector-style similarity scoring**: a `CASE WHEN` scoring expression that ranks results by conceptual similarity in the query scripts, or a real `VECTOR_DISTANCE` search against Bedrock-generated embeddings via `bedrock_vector_demo.py`
6. **Combined ranking**: all of the above conditions and scores in a single `SELECT` statement

Run `run_family_friendly_query.py` or `run_luxury_waterfront_query.py` for a concrete, end-to-end example of each step, or `interactive_mcp_demo.py` to explore the individual query types one at a time. Run `setup_database.py` / `setup_database_mcp.py` / `bedrock_vector_demo.py` to see the same patterns against a real OceanBase (and optionally Bedrock) backend.

## Example Query

This is the actual combined multi-model query from `run_luxury_waterfront_query.py`:

```sql
SELECT
    property_id,
    address,
    price,
    JSON_EXTRACT(features, '$.bedrooms') AS bedrooms,
    JSON_EXTRACT(features, '$.amenities') AS amenities,
    SUBSTRING(description, 1, 150) as description_excerpt,
    ST_Distance(location, ST_GeomFromText('POINT(-122.3321 47.6062)')) / 1000 as distance_km,
    (CASE WHEN description LIKE '%modern%' AND description LIKE '%minimalist%' THEN 3
          WHEN description LIKE '%modern%' THEN 2
          WHEN description LIKE '%luxury%' THEN 1
          ELSE 0 END) as vector_score
FROM
    unified_properties
WHERE
    -- SQL (Relational) conditions
    JSON_EXTRACT(features, '$.bedrooms') >= 4

    -- JSON (NoSQL) conditions
    AND JSON_CONTAINS(JSON_EXTRACT(features, '$.amenities'), '"pool"')
    AND JSON_CONTAINS(JSON_EXTRACT(features, '$.amenities'), '"home theater"')

    -- Geospatial (GIS) conditions
    AND ST_Contains(
        ST_Buffer(
            ST_GeomFromText('POINT(-122.3321 47.6062)'),  -- Seattle
            16093.4  -- 10 miles in meters
        ),
        location
    )

    -- Full-text search conditions
    AND description LIKE '%luxury%'
    AND description LIKE '%waterfront%'
    AND description LIKE '%panoramic view%'

    -- Vector similarity conditions (simulated)
    AND (description LIKE '%modern%' OR description LIKE '%minimalist%')

ORDER BY
    vector_score DESC,
    distance_km ASC
```

## Troubleshooting

If you encounter issues:

1. If `setup_database.py` or `setup_database_mcp.py` fails to connect, verify `OB_HOST`/`OB_PORT`/`OB_USER`/`OB_PASSWORD`/`OB_DATABASE` in `.env`, and that your OceanBase version supports `POINT`/`SPATIAL INDEX`/`FULLTEXT INDEX`/`VECTOR` (the scripts fall back to plain tables if those index types are rejected)
2. If you're pointing `mcp_tools.py` at a real OceanBase MCP server, verify that the MCP server is running and that `MCP_SERVER_NAME`/`MCP_TOOL_NAME` in `.env` match its configuration
3. If `bedrock_vector_demo.py` fails, verify `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_REGION` in `.env` are correct and that your account has access to `amazon.titan-embed-text-v2:0` in Amazon Bedrock
4. Use `--dry-run` on `setup_database.py` or `bedrock_vector_demo.py` to see the exact SQL/Bedrock calls without needing a live connection
5. Check the console output for error messages — each script prints its query and execution status as it runs

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OceanBase for providing the multi-model database capabilities
- AWS for providing the Bedrock API for embeddings generation
