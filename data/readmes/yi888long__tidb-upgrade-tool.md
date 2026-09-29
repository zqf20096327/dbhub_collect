# TiDB Upgrade Radar

TiDB Upgrade Radar is an MVP upgrade impact analyzer. It compares a current TiDB
version with a target version, combines that with the cluster's effective
configuration, and generates a risk report.

This first version focuses on the core loop:

- version range matching
- effective configuration analysis
- target-version behavior prediction
- important bug / known issue matching
- Markdown and JSON reports

The bundled knowledge base is demo data only. Replace or extend
`knowledge/sample_kb.json` with reviewed TiDB release-note, docs, issue, and PR
records before using it for real upgrade decisions.

## Quick Start

Start the local Web UI:

```bash
python3 -m upgrade_radar web --port 8765
```

Then open:

```text
http://127.0.0.1:8765
```

Run the CLI:

```bash
python -m upgrade_radar analyze \
  --current v6.5.1 \
  --target v7.5.2 \
  --profile examples/cluster_profile.json \
  --config tidb=examples/tidb.toml \
  --knowledge knowledge/sample_kb.json \
  --format markdown \
  --out report.md
```

Print JSON instead:

```bash
python -m upgrade_radar analyze \
  --current v6.5.1 \
  --target v7.5.2 \
  --profile examples/cluster_profile.json \
  --config tidb=examples/tidb.toml \
  --format json
```

## Profile Input

`cluster_profile.json` can include runtime observations and feature flags:

```json
{
  "features": {
    "tiflash": true,
    "cdc": false,
    "br": true
  },
  "global_variables": {
    "tidb_cost_model_version": "1"
  },
  "persisted_variables": [
    "tidb_cost_model_version"
  ],
  "top_sql": [
    {
      "digest": "abc",
      "sql": "select /*+ INL_JOIN(t1, t2) */ * from t1 join t2 on t1.id=t2.id"
    }
  ]
}
```

The analyzer distinguishes:

- default value
- config-file explicit value
- persisted or explicit global variable
- runtime-observed value whose persistence is unknown
- predicted value after the target upgrade

That distinction is important because a default-value change is risky only when
the cluster is actually expected to inherit the target default.

## Knowledge Model

The MVP knowledge base has three record groups:

- `config_parameters`
- `issues`
- `behavior_changes`

See `knowledge/sample_kb.json` for the exact shape.

## Tests

```bash
python -m unittest discover -s tests
```
