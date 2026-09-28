# Mixed Version Deployment

This directory contains a `tiup playground` based mixed-version deployment tool and reproducible mixed-version cases.

## Main Script

- `tiup-playground-mix-cluster.sh`
  Start a local mixed-version TiDB cluster with a low version for the initial playground cluster and a high version for later scale-out nodes.

## What The Script Covers

- starts a low-version base cluster with `tiup playground`
- scales out high-version `TiDB`, `TiKV`, `PD`, and `TiFlash`
- enables Prometheus and Grafana by default
- prefers default TiDB and PD ports by default and lets TiUP choose free ports if they are occupied
- checks required binaries before startup and downloads missing ones up front
- saves the tagged cluster topology in `mix-cluster-manifest.env`
- saves runnable per-instance commands in `mix-cluster-runtime.tsv`
- resumes a stopped tagged cluster from the saved topology and runtime state
- prints final mixed-version access information after the cluster is ready

## Fresh Cluster vs Existing Tag

There are two startup paths:

### Fresh cluster

For a new tag, `--low-version` and `--high-version` are required.

```bash
bash ./tiup-playground-mix-cluster.sh \
  --low-version v8.5.3 \
  --high-version v8.5.4
```

### Existing tag

If the tagged data dir already exists and contains `mix-cluster-manifest.env`, the script loads the saved topology first and ignores conflicting topology flags from the CLI.

```bash
bash ./tiup-playground-mix-cluster.sh --tag my-mix-cluster
```

This shortcut only works for an existing tagged cluster. For a brand-new tag, omitting `--low-version` and `--high-version` still fails.

You can still pass the original version flags when reusing an existing tag:

```bash
bash ./tiup-playground-mix-cluster.sh \
  --low-version v8.5.3 \
  --high-version v8.5.4 \
  --tag 853854
```

For an existing tag, the saved manifest wins.

## Preflight

Before startup, the script checks:

- required commands: `tiup`, `mysql`
- required low-version binaries
- required high-version binaries
- required monitor binaries when monitor is enabled

If anything is missing, the script downloads everything before cluster startup begins.

## Defaults

- monitor is enabled by default
- the default `port-offset` is `0`
- if counts are not specified, `PD`, `TiKV`, `TiDB`, and `TiFlash` each default to one low-version node and one high-version node
- if default ports are already in use, TiUP picks free ports automatically
- high-version PD scale-out waits `15s` between steps by default

## Common Examples

Basic mixed-version cluster:

```bash
bash ./tiup-playground-mix-cluster.sh \
  --low-version v8.5.3 \
  --high-version v8.5.4
```

Explicit per-component counts:

```bash
bash ./tiup-playground-mix-cluster.sh \
  --low-version v8.5.5 \
  --high-version v8.5.6-pre \
  --low-pd 3 \
  --high-pd 2 \
  --low-kv 3 \
  --high-kv 2 \
  --low-db 2 \
  --high-db 1 \
  --low-tiflash 1 \
  --high-tiflash 2
```

Disable monitor:

```bash
bash ./tiup-playground-mix-cluster.sh \
  --low-version v8.5.3 \
  --high-version v8.5.4 \
  --without-monitor
```

## Useful Options

- `--low-version VERSION`
- `--high-version VERSION`
- `--low-count N`
- `--high-count N`
- `--low-pd N --high-pd N`
- `--low-kv N --high-kv N`
- `--low-db N --high-db N`
- `--low-tiflash N --high-tiflash N`
- `--tag TAG`
- `--port-offset N`
- `--default-ports`
- `--with-monitor`
- `--without-monitor`
- `--start-timeout SECONDS`
- `--pd-stabilize SECONDS`

Run `bash ./tiup-playground-mix-cluster.sh --help` for the full option list.

## Output And Stop Behavior

`tiup playground` prints its own bootstrap output first. That only reflects the low-version base cluster. The script then performs the high-version `scale-out` steps and prints its own final `Mixed playground cluster is ready.` section.

After startup, the script prints:

- the final mixed-version matrix from `information_schema.cluster_info`
- all TiDB SQL access commands
- TiDB Dashboard URL
- Prometheus URL when enabled
- Grafana URL when enabled
- control commands for either fresh mode or resume mode

The script stays in the foreground.

- For a fresh cluster, `Ctrl-C` is forwarded to `tiup playground`
- For a resumed tagged cluster, `Ctrl-C` stops the saved component processes directly

## Saved State

Each tagged cluster stores:

- `mix-cluster-manifest.env`
  Saved topology and version choices for the tag
- `mix-cluster-runtime.tsv`
  Runnable component commands captured from the live cluster

The runtime file is now captured from the live component processes after the mixed cluster is ready, instead of rebuilding it only from log parsing.

## Cases

Concrete mixed-version reproductions live under `cases/`.

- `cases/issue_63965/`
  Reproduces the legacy `modify column` mixed-version cancel and owner handoff issue.

### One-command Reproduce

Reproduce issue `#63965` with one command:

```bash
bash ./cases/issue_63965/repro_63965.sh --tag issue-63965-demo
```

This command:

- starts or resumes the tagged mixed-version cluster in the background when needed
- runs the `#63965` reproduction automatically
- keeps the tagged cluster running after reproduction so you can inspect the stuck state

### Advanced Case Usage

If you want to split the case flow manually, the case script still supports:

```bash
bash ./cases/issue_63965/repro_63965.sh setup --tag issue-63965-demo
```

```bash
bash ./cases/issue_63965/repro_63965.sh repro --tag issue-63965-demo
```

See [cases/issue_63965/README.md](/Users/yichenhan/dev/kennedy8312/Tools/mixed_version_deployment/cases/issue_63965/README.md) for the case-specific steps.
