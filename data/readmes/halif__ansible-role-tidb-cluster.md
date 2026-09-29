# ansible-role-tidb-cluster

Ansible role for deploying a production-style, multi-host [TiDB](https://www.pingcap.com/tidb/)
cluster using [`tiup cluster`](https://docs.pingcap.com/tidb/stable/tiup-cluster/) —
PingCAP's own cluster orchestration tool for TiDB.

This is the **production-oriented counterpart** to
[`halif.tidb`](https://github.com/halif/ansible-role-tidb), which deploys a
single-host `tiup playground` cluster for development and testing. Use
`halif.tidb` for local dev/test; use this role when you need a real,
horizontally-scaled, fault-tolerant cluster across multiple hosts.

## How it works

The role runs on a single **control host** (the machine from which you
manage the cluster via `tiup`), not on each database host directly. It:

1. Installs `tiup` and the `cluster` component on the control host.
2. Renders a `topology.yaml` from the host lists you provide.
3. Runs `tiup cluster deploy` and `tiup cluster start`, which connect to
   the target hosts over SSH and do the actual multi-host orchestration.

`tiup cluster` requires an explicit version (no "latest" shortcut) — you
must pin `tidb_cluster_version` yourself, on purpose. This is a
production role; floating on "latest" between runs is not appropriate here.

## Recommended topology

For real fault tolerance you need **at least 3 hosts**, each running all
three roles (PD + TiKV + TiDB together):

- **TiKV** replicates data 3 times by default (`max-replicas: 3`) — those
  3 replicas need 3 physically separate hosts to actually protect against
  a host failure.
- **PD** uses Raft for its own consensus and needs an **odd** number of
  instances (1 or 3) to tolerate one node going down.
- **TiDB** itself is stateless and scales more freely.

Two hosts is not enough for genuine fault tolerance — TiKV cannot spread
3 replicas across only 2 machines without doubling up somewhere.

## Prerequisites

- **Passwordless SSH access** (key-based, root or NOPASSWD sudo user) from
  the control host to every target host in the cluster. The role does
  **not** set this up for you — it's a deliberate scope boundary, since
  bootstrapping cross-host trust is usually a separate, environment-specific
  step (cloud provider metadata, existing configuration management, etc.).
- Target hosts: Ubuntu 20.04/22.04 or RHEL/Rocky/Alma 8/9 (systemd).
- Enough resources per host — PD + TiKV + TiDB together need meaningfully
  more than a minimal VM (see PingCAP's hardware recommendations).

## Role Variables

See the full list with defaults in [`defaults/main.yml`](defaults/main.yml).

| Variable                       | Default            | Description                                    |
|----------------------------------|---------------------|--------------------------------------------------|
| `tidb_cluster_name`              | `"ansible-managed"` | Name TiUP uses to track this cluster             |
| `tidb_cluster_version`           | `""` (**required**) | TiDB version to deploy, e.g. `"v8.5.7"`          |
| `tidb_cluster_pd_hosts`          | `[]`                 | Hosts running PD                                 |
| `tidb_cluster_tikv_hosts`        | `[]`                 | Hosts running TiKV                               |
| `tidb_cluster_tidb_hosts`        | `[]`                 | Hosts running TiDB                               |
| `tidb_cluster_ssh_user`          | `"root"`             | User `tiup cluster` uses to bootstrap target hosts |
| `tidb_cluster_ssh_private_key`   | `"~/.ssh/id_rsa"`    | Private key path on the control host             |

## Example Playbook

```yaml
- hosts: tidb_control_node
  become: true
  roles:
    - role: halif.tidb_cluster
      vars:
        tidb_cluster_version: "v8.5.7"
        tidb_cluster_pd_hosts:
          - 10.0.1.1
          - 10.0.1.2
          - 10.0.1.3
        tidb_cluster_tikv_hosts:
          - 10.0.1.1
          - 10.0.1.2
          - 10.0.1.3
        tidb_cluster_tidb_hosts:
          - 10.0.1.1
          - 10.0.1.2
          - 10.0.1.3
```

After the role runs, connect to any TiDB host on port 4000 with any MySQL
client.

## Testing

CI runs a **single-host smoke test**: `tiup cluster deploy` for real,
with PD/TiKV/TiDB all pointed at `127.0.0.1` on one container (self-SSH).
This validates that the automation itself is correct — command syntax,
topology rendering, idempotency — but it does **not** exercise genuine
multi-host fault tolerance, since that requires real separate machines.
Before using this role against production, validate a real 3-host
deployment manually.

```bash
pip install ansible molecule "molecule-plugins[docker]" docker
molecule test
```

## License

MIT
