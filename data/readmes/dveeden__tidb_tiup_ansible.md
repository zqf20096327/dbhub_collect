This prepares a Rocky Linux 9.5 host to be used by `tiup cluster`.

Use `tiup cluster check` to verify. See also: https://docs.pingcap.com/tidb/stable/check-before-deployment/

Rebooting after applying this is recommended to ensure that settings are made in a way that persists across reboots. A reboot is also needed for SELinux to go from enforcing or permissive to disabled.

To use this, update `hosts` with your inventory and run:
```
ansible-playbook tidb_basics.yml -i hosts
```

WARNING: This is only an example/demo use on your own risk.
