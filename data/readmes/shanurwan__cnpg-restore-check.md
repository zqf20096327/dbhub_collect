# cnpg-restore-check

Scheduled restore checks for [CloudNativePG](https://cloudnative-pg.io) backups.

A successful backup does not prove that you can restore it. `cnpg-restore-check`
restores your real backups on a schedule into a temporary cluster, verifies the
data, measures how long recovery took and how old the newest restored data is,
and alerts when a restore fails or misses its objectives.

From the end-to-end suite, where `walgap` restores a backup with one WAL
segment deleted from the archive:

```console
$ kubectl get restorechecks
NAME       SCHEDULE   PHASE       LAST RESULT   REASON            RECOVERY   DATA AGE   LAST SUCCESS
guard                             Failed        InvalidSpec
healthy                           Succeeded                       56s        10s        79s
walgap                            Failed        ObjectiveMissed   55s        1h0m11s
```

The `walgap` restore came up Ready in 55 seconds and looked healthy. Only the
data age shows that it is missing the last hour.

It works with backups made by [plugin-barman-cloud](https://github.com/cloudnative-pg/plugin-barman-cloud)
(S3, GCS, Azure Blob and compatible stores). This is a community project, not
part of CloudNativePG.

## Why

Restores fail for reasons that never show up as a failed backup:

- **A WAL segment is missing from the archive.** Recovery to the latest point
  stops at the gap and promotes *without an error*. The restored database looks
  fine and is missing everything after the gap. The e2e suite here reproduces
  this: one deleted segment, a restore that comes up Ready, and data an hour old.
- A backup taken on a standby of a quiet database ends in a WAL segment that is
  not archived yet, so the "completed" backup cannot be restored until the
  primary switches WAL
  ([plugin-barman-cloud#652](https://github.com/cloudnative-pg/plugin-barman-cloud/issues/652)).
  The e2e suite reproduces this too.
- Recovery across a timeline switch after a failover fails
  ([cloudnative-pg#10422](https://github.com/cloudnative-pg/cloudnative-pg/issues/10422)).
- Settings, credentials, bucket policies or images changed since anyone last restored.

The only way to know is to restore. This makes that routine and measured.

## What a run does

1. Checks that the source ObjectStore exists and that no Cluster in the
   namespace writes to it (see [Safety](#safety)).
2. Creates a one-instance CloudNativePG `Cluster` that bootstraps by recovery
   from the backup: the same path a real recovery takes.
3. Measures **recovery time** from creating that Cluster to it being Ready.
4. Runs checks against the restored primary:
   - **amcheck** on every database (B-tree indexes; optionally every heap page
     and heap-to-index consistency);
   - **SQL assertions** you write (`select count(*) > 0 from orders`);
   - **freshness**: a query returning the newest timestamp in the data, which
     gives the **data age** (your real recovery point).
5. Fails the run on a failed check, a failed recovery, a timeout, or a missed
   objective, then records the result in status, Events and Prometheus metrics
   and deletes the temporary cluster.

## Try it

The [quickstart](docs/quickstart.md) runs on kind in about 10 minutes and ends
with breaking a backup on purpose.

## Install

Requirements: CloudNativePG 1.26 or later with plugin-barman-cloud.

```sh
helm install cnpg-restore-check oci://ghcr.io/shanurwan/charts/cnpg-restore-check \
  --namespace cnpg-restore-check --create-namespace \
  --set prometheusRule.enabled=true --set metrics.serviceMonitor.enabled=true
```

Or with plain manifests:

```sh
kubectl apply --server-side -f https://github.com/shanurwan/cnpg-restore-check/releases/latest/download/install.yaml
```

## Quickstart

In the namespace of the source cluster, or a separate one with the same access
controls, create an ObjectStore that **only reads** the bucket, and a RestoreCheck:

```yaml
apiVersion: barmancloud.cnpg.io/v1
kind: ObjectStore
metadata:
  name: pg-main-readonly
  namespace: payments
spec:
  configuration:
    destinationPath: gs://acme-pg-backups/
    googleCredentials:
      gkeEnvironment: true      # Workload Identity, bound to roles/storage.objectViewer
---
apiVersion: restorecheck.shanurwan.github.io/v1alpha1
kind: RestoreCheck
metadata:
  name: orders
  namespace: payments
spec:
  schedule: "0 3 * * *"            # daily, 03:00 UTC
  source:
    objectStoreName: pg-main-readonly
    serverName: pg-main            # the source cluster's server name in the bucket
  cluster:
    storageSize: 50Gi
    parameters:
      max_connections: "200"       # at least the source's value
  checks:
    amcheck: {}
    sql:
      - name: orders-present
        database: app
        query: "select count(*) > 0 from orders"
    freshness:
      database: app
      query: "select max(ts) from heartbeat"
  objectives:
    recoveryTime: 30m              # RTO
    dataAge: 10m                   # RPO
    successAge: 26h                # alert if no success for a day
```

The freshness check needs something in the database that is written often. A
heartbeat table updated every minute works well; see
[examples/heartbeat.yaml](examples/heartbeat.yaml).

Run a check now, outside the schedule:

```sh
kubectl annotate restorecheck -n payments orders --overwrite \
  restorecheck.shanurwan.github.io/run-now="$(date +%s)"
```

More examples: [examples/](examples/).

## Safety

A restore test must never write into the backups it is testing.

- The temporary cluster never gets `spec.plugins` or `spec.backup`, so it cannot
  archive WAL or take backups. Unit tests check the generated object.
- The controller refuses an ObjectStore that a Cluster in the same namespace
  references for archiving or backups, unless
  `spec.source.allowSharedObjectStore` is set. Give the RestoreCheck its own
  ObjectStore with read-only credentials.
- It never reads or changes the source cluster.
- It reads Secrets without caching them, and only creates and deletes
  CloudNativePG Clusters. `watchNamespaces` limits it to chosen namespaces.
- Runs have a timeout (default 2h), and `maxConcurrentRuns` (default 1) bounds
  how many restored instances exist at once.

A restored cluster holds production data. Run checks where the same people and
policies already have access, and restrict port 5432 there to the controller.

## Monitoring

Metrics (all with `namespace` and `name` labels):

| Metric | Meaning |
| --- | --- |
| `cnpg_restore_check_last_run_success` | 1 if the last run succeeded |
| `cnpg_restore_check_last_success_timestamp_seconds` | when the last success finished |
| `cnpg_restore_check_recovery_duration_seconds` | measured recovery time |
| `cnpg_restore_check_data_age_seconds` | measured age of the newest restored data |
| `cnpg_restore_check_run_in_progress` | 1 while a run is in progress |
| `cnpg_restore_check_runs_total{result,reason}` | finished runs |
| `cnpg_restore_check_objective_*_seconds` | the objectives from the spec |

Alerts (`prometheusRule.enabled=true`), each with a [runbook](docs/runbooks.md):

| Alert | Severity | Fires when |
| --- | --- | --- |
| `CNPGRestoreCheckFailed` | critical | the last run failed |
| `CNPGRestoreCheckDataAgeAboveObjective` | critical | restored data is older than `objectives.dataAge` |
| `CNPGRestoreCheckRecoveryTimeAboveObjective` | warning | recovery took longer than `objectives.recoveryTime` |
| `CNPGRestoreCheckStale` | warning | no success within `objectives.successAge` |
| `CNPGRestoreCheckRunStuck` | warning | a run has been in progress for 6h |

## Reference

`kubectl explain restorecheck.spec` documents every field. Main ones:

| Field | Default | Meaning |
| --- | --- | --- |
| `schedule` | none | cron (UTC). A new check runs once right away, then on schedule. Without a schedule, it runs once. |
| `source.objectStoreName`, `source.serverName` | required | where the backup is |
| `target` | latest | `backupID`, `targetTime` or `targetImmediate` |
| `cluster` | 1 instance, 10Gi | `imageName`, `storageSize`, `storageClass`, `resources`, `parameters`, `nodeSelector` |
| `checks` | connect only | `amcheck`, `sql`, `freshness` |
| `objectives` | none | `recoveryTime`, `dataAge`, `successAge` |
| `timeout` | 2h | maximum time for a run |
| `keepFailedClusters` | false | keep the cluster of a failed run until the next run |
| `suspend` | false | stop scheduled runs |

Failure reasons in `status.lastRun.reason`: `RecoveryFailed`, `Timeout`,
`CheckFailed`, `ObjectiveMissed`, `InvalidSpec`, `ClusterLost`.

## How it is tested

- **Unit tests:** the generated Cluster (never archives, correct recovery
  source), scheduling (missed slots, run-now), every failure path of the run
  state machine, objectives and the concurrency limit.
- **Alert tests:** `promtool test rules` for every alert, firing and not firing.
- **End-to-end tests** ([test/e2e](test/e2e)) against a real cluster with
  CloudNativePG, plugin-barman-cloud and an S3 server:
  - a healthy backup passes amcheck, an assertion and freshness, and its metrics are exported;
  - after deleting one archived WAL segment, the restore still comes up Ready
    but the run fails with `ObjectiveMissed` and a data age of about an hour;
  - a standby backup of a quiet database (plugin-barman-cloud#652) misses a 3m
    recovery objective while its last WAL segment is unarchived, and passes in
    under a minute after a WAL switch on the primary;
  - a wrong server name fails with `RecoveryFailed`;
  - an ObjectStore that the source writes to is refused before anything is created.

  Last local run, on k3s v1.35 with CloudNativePG 1.30.1 and plugin-barman-cloud
  v0.16.0: all pass. The healthy restore took 56 s with data 10 s old; the WAL
  gap restore took 55 s with data 1h0m11s old; the quiet standby backup took
  6m55s to restore, against 54 s after the WAL switch. CI runs the same suite on kind.

The design, including the safety model and alternatives, is in
[docs/design.md](docs/design.md).

## Development

```sh
make test            # unit tests
make test-alerts     # promtool
make manifests       # regenerate CRD and RBAC after changing api/ or RBAC markers
make e2e             # needs a cluster; see test/e2e/README.md
```

## Contributing

Bug reports from real setups are the most useful contribution: every storage
provider and cluster layout finds different failures. See
[CONTRIBUTING.md](CONTRIBUTING.md); commits need a DCO sign-off (`git commit -s`).
Issues labelled [good first issue](https://github.com/shanurwan/cnpg-restore-check/labels/good%20first%20issue)
are scoped for a first change. Questions go to
[Discussions](https://github.com/shanurwan/cnpg-restore-check/discussions).

Using it? Add yourself to [ADOPTERS.md](ADOPTERS.md).

## License

Apache License 2.0
