# Feature Proof

Feature Proof is a local Python-backed demo console for TiDB Cloud product feature proofs.

It helps architects select a cloud provider, product category, and feature, then run real TiDB-backed proof steps through a metadata-driven and pluggable State Pattern architecture.

## Architecture

Feature Proof uses a lightweight local web architecture:

- `app.py` provides the Python HTTP server, JSON API routing, static file serving, metadata CRUD endpoints, connection checks, and demo step dispatch.
- `db.py` manages the local SQLite metadata database and seed data.
- `feature_states.py` contains the shared State Pattern infrastructure, including `DemoContext`, `TiDBClient`, the `FeatureState` base class, connection parsing, connection testing, and the dynamic state loader.
- `feature_state_handlers/` contains one Python module per feature state.
- `static/` contains the vanilla HTML, CSS, and JavaScript UI.
- `feature_proof.sqlite3` is the local metadata database and is intentionally ignored by Git.

The metadata model separates product availability from feature implementation:

- `CloudVendor` stores cloud providers.
- `ProductCategory` stores TiDB Cloud product categories.
- `Feature` stores feature names.
- `CloudVendorProduct` controls which product categories are available under each cloud provider and stores the `ConnectWith` connection profile text.
- `ProductFeature` controls which features are available under each product category.
- `FeatureState` maps a feature to its `init_handler`, `calc_handler`, and `show_handler`.

## State Pattern Design

Each feature proof is implemented as a State object with a fixed lifecycle:

1. `init()` prepares demo data.
2. `calc()` executes the feature-specific operation.
3. `show()` returns display-ready results.

Feature Proof keeps this lifecycle stable while allowing each feature to own its own implementation. The handler name stored in `FeatureState` maps directly to a Python module in `feature_state_handlers/`.

For example:

- handler name `json` loads `feature_state_handlers/json.py`
- handler name `vector_search` loads `feature_state_handlers/vector_search.py`
- handler name `fts` loads `feature_state_handlers/fts.py`

Each handler file exports a standard class:

```python
class State(FeatureState):
    ...
```

This design has several advantages:

- New feature proofs can be added without modifying a large central state file.
- Each feature remains portable and easy to review.
- Feature metadata can change independently from feature execution code.
- The UI can execute all features through the same `Init`, `Start`, and optional `Show` flow.
- The backend validates handler names before dynamic import, reducing unsafe module loading risk.

## Add A New Feature State

To add a new feature proof:

1. Add the feature in Metadata Management, or insert it into the `Feature` table.
2. Relate the feature to one or more product categories through `ProductFeature`.
3. Add or update the `FeatureState` row. The handler values should match the Python filename under `feature_state_handlers/`.
4. Create `feature_state_handlers/<handler_name>.py`.
5. Define `class State(FeatureState)` with `init()`, `calc()`, and `show()`.
6. Add a custom frontend renderer only if the standard sections/table output is not enough.

Example:

```python
from feature_states import FeatureState, response


class State(FeatureState):
    def init(self):
        return response(
            "ok",
            "Demo data initialized.",
            sections=[
                {
                    "title": "Data Initialization",
                    "description": "Prepare sample rows for the proof.",
                    "columns": ["id", "name"],
                    "data": [{"id": 1, "name": "sample"}],
                    "sql": "CREATE TABLE ...",
                }
            ],
        )

    def calc(self):
        return response("ok", "Calculation completed.")

    def show(self):
        return response(
            "ok",
            "Result ready.",
            sections=[
                {
                    "title": "Operation 1",
                    "description": "Run the feature proof query.",
                    "columns": ["id", "result"],
                    "data": [{"id": 1, "result": "matched"}],
                    "sql": "SELECT ...",
                }
            ],
        )
```

If the new feature should hide the standalone `Show` button, add the feature name to the frontend hidden-show list in `static/app.js`.

## Local Deployment And Run

Clone the repository:

```bash
git clone https://github.com/utopiadf/feature_proof.git
cd feature_proof
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Initialize and run the app:

```bash
python3 -B app.py
```

Open:

```text
http://127.0.0.1:8000
```

Run tests:

```bash
python3 -m unittest -v
```

## Configuration Notes

The app creates `feature_proof.sqlite3` automatically in the project directory. This file stores local metadata and is ignored by Git.

Do not commit real TiDB Cloud credentials. Use Metadata Management to configure local test connections, or inject development-only seed data through local environment variables.

## TiDB Cloud Connections

Connection profiles are stored in the `CloudVendorProduct.ConnectWith` column. The value uses `.env` style keys:

```bash
DB_HOST=
DB_PORT=4000
DB_USERNAME=
DB_PASSWORD=
DB_DATABASE=
```

The app tests the selected cloud/product connection before enabling demo actions. If no matching profile exists, demo actions remain disabled and the UI shows `Connection profile is not configured`.

The older local `.env` `FP_*` format is still supported as a fallback for development.
