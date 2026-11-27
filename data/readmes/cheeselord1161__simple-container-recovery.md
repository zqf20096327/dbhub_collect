# Simple Container Recovery

A starter template for a containerized database-backed service. It includes a Python and SQLite example workload, automatic container restarts, dynamic proxy discovery, and scheduled database backups.

## Start the lab

You can run the project with Docker Compose v2 or Podman Compose. For Podman, install a Compose provider such as `podman-compose`; `podman compose` is a wrapper around that provider. Copy `.env.example` to `.env` if you want to change the settings, then start the services with either engine:

```sh
podman compose up --build -d
# Or, with Docker Compose v2:
docker compose up --build -d
```

See the [Podman Compose documentation](https://docs.podman.io/en/latest/markdown/podman-compose.1.html) if you need to set up its provider.

Open <http://localhost:8080> (or the port set by `LAB_PORT`). Add a few records so there is data to protect.

The workload API is `POST /api/records` with JSON such as `{"value":"hello"}`; `GET /api/records` lists the latest 100 records.

## What runs

- `backend` serves the workload and stores its SQLite database in the container's writable layer. It has no database volume.
- `proxy` serves the app on localhost and reads its DNS server from the container's `/etc/resolv.conf`, so it works with different Podman or Docker network addresses and can resolve a changed backend IP again. The official Nginx image processes the config template at startup using its environment-substitution entrypoint.
- `backup` requests a consistent SQLite snapshot from the backend every 60 seconds and writes it to `backups/` on the host.

The backup service keeps the newest 60 snapshots by default. Set `BACKUP_INTERVAL_SECONDS` and `BACKUP_RETENTION` in `.env` to change that. Backups are separate from the backend container, so replacing the backend does not remove them.

The `always` restart policy starts the backend again after its process exits unexpectedly. A failed health check reports that the backend is unhealthy, but does not by itself restart it. Compose waits for the backend health check before starting the proxy and backup service. With Podman, `podman stop` and `podman kill` suppress the restart policy, so the crash exercise below terminates the app process from inside the container instead. After a host reboot, Podman restart behavior depends on its systemd restart service. See the [Podman restart policy documentation](https://docs.podman.io/en/stable/markdown/podman-run.1.html#--restartpolicy) and [Docker Compose service documentation](https://docs.docker.com/reference/compose-file/services/).

## Recovery behavior

- If the backend process or container restarts in place, its writable layer remains and its database is still there.
- If the backend container is replaced, its writable layer is lost. On startup, the app restores the newest valid snapshot from `backups/` if the database file is missing.
- Automatic backups run once per minute by default, so a sudden loss can leave up to about one minute of recent records outside the latest snapshot.
- The manual backup command creates an extra snapshot immediately:

  ```sh
  ./scripts/backup.sh
  ```

The script detects whether `workload-backup` is running under Podman or Docker. If both engines have a container with that name, set `CONTAINER_ENGINE=podman` or `CONTAINER_ENGINE=docker` before running it.

## Try it

1. Add a few records in the browser and wait for a backup. Check the `backups/` folder for snapshots.
2. Restart the backend in place and confirm its data remains:

   ```sh
   podman compose restart backend
   # Or: docker compose restart backend
   ```

3. Replace the backend container and confirm it restores from backup:

   ```sh
   ./scripts/backup.sh
   podman compose up --build -d --force-recreate --no-deps backend proxy
   # Or: docker compose up --build -d --force-recreate --no-deps backend proxy
   ```

4. Simulate a crash with the local-only endpoint:

   ```sh
   curl http://localhost:8080/internal/crash
   ```

   The endpoint replies before terminating the backend process. Check `podman compose ps` to confirm it restarts. The published port is bound to `127.0.0.1`, so other machines cannot call this crash endpoint.

5. Check status at <http://localhost:8080/health>. The response includes the record count and uptime.

To check the Nginx configuration without restarting it:

```sh
podman exec mini-cloud-nginx nginx -t
# Or: docker compose exec proxy nginx -t
```

Backups are stored locally; copy them elsewhere if you want protection from losing the host machine. This is a learning setup, not a hardened public service: the sample app has no user accounts, and the internal backup endpoint relies on the private Compose network. The web port is available only from the host machine.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
