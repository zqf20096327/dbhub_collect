# ansible-role-tidb

Ansible role to install [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview/)
and deploy a local TiDB test cluster (`tiup playground`),
managed as a systemd service.

TiDB is open source (Apache 2.0), so installation does not require any license
keys or private repositories: the package is downloaded from a public mirror
PingCAP..

## Requirements

- Ansible >= 2.14
- Target OS: RHEL/Rocky/AlmaLinux 8/9, Ubuntu 20.04/22.04 (systemd)
- Internet access on the target machine (for downloading TiUP)

## Role Variables

See the full list with default values in [`defaults/main.yml`](defaults/main.yml).

| Variable                        | Default       | Description                             |
|---------------------------------|---------------|-----------------------------------------|
| `tidb_user`                     | `tidb`        | The user under whose identity TiUP runs |
| `tidb_create_user`              | `true`        | Whether to create the tidb_user         |
| `tidb_playground_enabled`       | `true`        | Whether to spin up a playground cluster |
| `tidb_playground_version`       | `""` (latest) | TiDB version for the playground         |
| `tidb_playground_db_count`      | `1`           | Number of TiDB instances                |
| `tidb_playground_kv_count`      | `1`           | Number of TiKV instances                |
| `tidb_playground_pd_count`      | `1`           | Number of PD instances                  |
| `tidb_playground_tiflash_count` | `0`           | Number of TiFlash instances             |

## Usage Example

```yaml
- hosts: tidb_servers
  become: true
  roles:
    - role: halif.tidb
      vars:
        tidb_playground_db_count: 1
        tidb_playground_kv_count: 3
        tidb_playground_pd_count: 1
```

After applying the role::

```bash
mysql --host <server_ip> --port 4000 -u root
```

The PD Dashboard is available at `http://<server_ip>:2379/dashboard`.

## Тестирование

The role is tested via [Molecule](https://molecule.readthedocs.io/) on
Ubuntu 22.04 и AlmaLinux 8:

```bash
pip install ansible molecule "molecule-plugins[docker]" docker
molecule test
```

## License

MIT

## Author

[halif](https://github.com/halif)
