# node-problem-mitigator

[![Mitigation with a pre-mitigation Job](docs/terminate-standard.svg#play-0-a)](https://raw.githubusercontent.com/ClickHouse/node-problem-mitigator/refs/heads/main/docs/terminate-standard.svg)

A Kubernetes controller that responds to node problems with tainting, draining,
and custom Jobs. It watches Node conditions reported by [Node Problem
Detector](https://github.com/kubernetes/node-problem-detector) or another source.

## Configuration

Choose which Node conditions to watch and how to handle them in
`app.config.conditions`. No conditions are watched by default.
A condition taints and drains the node unless told otherwise.
This example taints and drains the node, then runs the `terminate` [mitigation Job](docs/jobs.md#mitigation-jobs):

```yaml
app:
  enabled: true
  config:
    conditions:
      KernelDeadlock:
        mitigationJob:
          name: terminate
```

`terminate` names a template in the `jobs` map; the [cloud examples](docs/jobs.md#cloud-termination)
define it for AWS, GCP, and Azure.

A mitigation runs these steps, each of which a condition can switch off or
leave unset:

1. Taint the node with `NoSchedule`.
2. Run a [pre-mitigation Job](docs/jobs.md#pre-mitigation-jobs), for example to capture diagnostics before workloads leave.
3. Drain the node, respecting PodDisruptionBudgets.
4. Run a [mitigation Job](docs/jobs.md#mitigation-jobs), for example to terminate the cloud instance.

To mitigate a node by hand, annotate it with `clickhouse.com/node-mitigated-condition=Manual`.
`Manual` is a default condition no node reports; any configured condition works the same way.

The controller has no cloud credentials. Give the Jobs the permissions they need
through ServiceAccount RBAC or a cloud identity binding.

## Installation

```sh
helm install node-problem-mitigator oci://ghcr.io/clickhouse/charts/node-problem-mitigator \
  --namespace node-problem-mitigator --create-namespace --values values.yaml
kubectl -n node-problem-mitigator logs deployment/node-problem-mitigator
```

Helm installs the latest release. Add `--version` to pin one.

The chart is disabled by default. Set `app.enabled: true` to enable it, as in the example above.
The [AWS](examples/aws.yaml), [GCP](examples/gcp.yaml), and
[Azure](examples/azure.yaml) examples enable cloud termination.
Before deploying them, configure identity for your cluster and review which conditions they watch.

## Safety

- Use the [`enabled` kill switch](docs/operations.md#kill-switch) to pause all mitigation, including work in progress.
- Use `dry-run` to log decisions without changing nodes or launching Jobs.
- Set `taint: false` to run only a pre-mitigation Job, without tainting or draining the node.
- The global cooldown starts at most one mitigation every 15 minutes by default. `taint: false` conditions are not counted.
- Set `for` to wait for a sustained failure.
- Use exclusions to protect nodes and namespaces.

A started mitigation that taints the node continues after the condition recovers or the configuration changes.
See [mitigation behavior](docs/mitigation.md) for the steps, drain timeouts, and stalls.

## Documentation

- [Configuration](docs/configuration.md): Helm settings, conditions, exclusions, and runtime configuration.
- [Mitigation](docs/mitigation.md): pipeline, cooldown, plan ownership, and lifecycle diagrams.
- [Jobs](docs/jobs.md): pre-mitigation Jobs, mitigation Jobs, cloud identity, and permissions.
- [Operations](docs/operations.md): pause controls, manual mitigation, metrics, alerts, and troubleshooting.
- [Development](docs/development.md): local builds, tests, CLI flags, and releases.

Licensed under the [Apache License 2.0](LICENSE).
