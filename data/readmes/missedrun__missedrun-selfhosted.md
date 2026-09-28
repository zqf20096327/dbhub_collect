# MissedRun Self-hosted

Self-hosted cron and scheduled job monitoring for detecting silent failures.

MissedRun monitors recurring jobs such as cron scripts, backups, imports, ETL pipelines, billing syncs, cleanup tasks, and scheduled reports.

It works by giving each monitor a unique ping URL. Your job calls that URL when it runs, starts, finishes successfully, or fails. If the job does not check in within the expected interval plus grace period, MissedRun marks it as missing and can send an alert.

* Hosted version: [https://missedrun.com](https://missedrun.com)
* Self-hosted version: [https://github.com/missedrun/missedrun-selfhosted](https://github.com/missedrun/missedrun-selfhosted)
* License: AGPL-3.0

## Useful links

* Hosted version: [https://missedrun.com](https://missedrun.com)
* Cron job monitoring guide: [https://missedrun.com/cron-job-monitoring](https://missedrun.com/cron-job-monitoring)
* Cron command wrapper guide: [https://missedrun.com/cron-command-wrapper](https://missedrun.com/cron-command-wrapper)
* Detect missed cron jobs: [https://missedrun.com/missed-cron-job](https://missedrun.com/missed-cron-job)
* Self-hosted cron monitoring: [https://missedrun.com/self-hosted-cron-monitoring](https://missedrun.com/self-hosted-cron-monitoring)

## What problem does it solve?

Some production failures are not loud.

A job can stop running without throwing an exception. For example:

* cron did not run
* the server was down
* a Docker container stopped
* credentials expired before the job reached your alerting code
* a backup script never started
* an import stopped updating data
* a scheduled report was not generated
* a background worker silently stopped
* a job started but never sent a success signal

MissedRun is built to detect this kind of silent failure by tracking whether scheduled jobs check in when expected.

## Current V1 features

This repository is the V1 self-hosted version. It currently focuses on basic heartbeat-style monitoring for scheduled jobs.

Available now:

* Create monitors for scheduled jobs
* Generate unique ping URLs
* Success ping endpoint
* Optional start ping endpoint
* Optional failure ping endpoint
* Shell wrapper pattern for existing cron commands
* Track monitor status:
  * pending
  * running
  * healthy
  * failed
  * missing
  * paused
* Store monitor event history
* Background checker for missing jobs
* Basic email alert support
* Docker Compose setup
* FastAPI backend
* PostgreSQL storage

Not included in V1:

* Slack alerts
* Webhook alerts
* Discord alerts
* Telegram alerts
* Teams / workspaces
* Output metrics such as processed count, created count, or failed count
* Rules/assertions on job output
* Anomaly detection
* Historical volume comparison
* Public status pages
* Integration marketplace

## Screenshots

### Dashboard

<img src="docs/screenshots/dashboard.webp" alt="MissedRun dashboard" width="720">

### Monitor details and history

<img src="docs/screenshots/monitor-history.webp" alt="MissedRun monitor details and history" width="720">

### Ping URLs

<img src="docs/screenshots/ping-urls.webp" alt="MissedRun ping URLs" width="720">

### Create monitor

<img src="docs/screenshots/create-monitor.webp" alt="Create a MissedRun monitor" width="720">

### Email alert

<img src="docs/screenshots/email-alert.webp" alt="MissedRun email alert" width="520">

## Hosted vs self-hosted

This repository contains the self-hosted version of MissedRun.

Use the self-hosted version if you want to run the monitor on your own infrastructure.

Use the hosted version if you want MissedRun without managing servers, updates, SMTP, database backups, or deployment.

Hosted version: [https://missedrun.com](https://missedrun.com)

## Quick start

Clone the repository:

```bash
git clone https://github.com/missedrun/missedrun-selfhosted.git
cd missedrun-selfhosted
```

Create your environment file:

```bash
cp .env.example .env
```

Start MissedRun with Docker Compose:

```bash
docker compose up -d
```

Check that the API is running:

```bash
curl http://localhost:8008/health
```

Check that the database connection is working:

```bash
curl http://localhost:8008/db-health
```

The API should now be available at:

```text
http://localhost:8008
```

## Create a monitor

Create a monitor for a nightly backup that should run once every 24 hours, with a 60-minute grace period:

```bash
curl -X POST http://localhost:8008/api/monitors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nightly backup",
    "interval_minutes": 1440,
    "grace_minutes": 60
  }'
```

The response includes a `token`:

```json
{
  "id": 1,
  "name": "Nightly backup",
  "token": "YOUR_MONITOR_TOKEN",
  "interval_minutes": 1440,
  "grace_minutes": 60,
  "status": "pending"
}
```

## Ping a monitor

Send a success ping when the job finishes successfully:

```bash
curl -X POST http://localhost:8008/api/ping/YOUR_MONITOR_TOKEN
```

Example cron usage:

```cron
0 2 * * * /usr/local/bin/backup.sh && curl -fsS -X POST http://localhost:8008/api/ping/YOUR_MONITOR_TOKEN
```

This is the simplest setup.

It detects when the job stops checking in, but it does not tell MissedRun when the job started or whether it failed explicitly.

## Recommended wrapper script

For real jobs, it is better to report start, success, and failure.

You can copy the example wrapper from this repository:

```text
examples/missedrun-wrap.sh
```

Example usage:

```bash
./examples/missedrun-wrap.sh --token YOUR_MONITOR_TOKEN --timeout 30m -- /home/user/backup.sh
```

For a more detailed explanation of the wrapper approach, see:

[https://missedrun.com/cron-command-wrapper](https://missedrun.com/cron-command-wrapper)

The wrapper sends:

* a `/start` ping before the command runs
* a success ping if the command exits with code `0`
* a `/fail` ping if the command exits with an error
* a `/fail` ping if the command times out

Then run it from cron:

```cron
0 2 * * * /path/to/missedrun-selfhosted/examples/missedrun-wrap.sh --token YOUR_MONITOR_TOKEN --timeout 30m -- /home/user/backup.sh
```

This gives MissedRun more information:

* `/start` means the job began running
* success ping means the job completed successfully
* `/fail` means the job failed
* no check-in means the job may have been missed
* start without success/failure means the job may be stuck

## Start ping

Use a start ping when a job begins running:

```bash
curl -X POST http://localhost:8008/api/ping/YOUR_MONITOR_TOKEN/start
```

This changes the monitor status to `running`.

## Success ping

Use a success ping when a job finishes successfully:

```bash
curl -X POST http://localhost:8008/api/ping/YOUR_MONITOR_TOKEN
```

This changes the monitor status to `healthy`.

## Failure ping

Use a failure ping when a job fails:

```bash
curl -X POST http://localhost:8008/api/ping/YOUR_MONITOR_TOKEN/fail \
  -H "Content-Type: application/json" \
  -d '{"message":"Backup failed"}'
```

This changes the monitor status to `failed` and records the failure message.

## List monitors

```bash
curl http://localhost:8008/api/monitors
```

## View monitor history

```bash
curl http://localhost:8008/api/monitors/1/history
```

## Statuses

| Status    | Meaning                                                                  |
| --------- | ------------------------------------------------------------------------ |
| `pending` | The monitor was created but has not received a ping yet.                 |
| `running` | The job sent a start ping and has not completed yet.                     |
| `healthy` | The last success ping was received on time.                              |
| `failed`  | The job explicitly reported a failure.                                   |
| `missing` | The job did not check in within the expected interval plus grace period. |
| `paused`  | The monitor is paused and will not alert.                                |

## Environment variables

Copy `.env.example` to `.env` and edit the values.

```env
APP_NAME=MissedRun Self-hosted
APP_ENV=development
DATABASE_URL=postgresql://missedrun:missedrun@postgres:5432/missedrun
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

ALERT_EMAIL=

SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=MissedRun
SMTP_REPLY_TO=
```

If SMTP is not configured, alerts are printed in the container logs.

## Development

Start the stack:

```bash
docker compose up -d
```

View logs:

```bash
docker compose logs -f backend
docker compose logs -f checker
```

Stop the stack:

```bash
docker compose down
```

Reset the local database volume:

```bash
docker compose down -v
```

## API endpoints

| Method   | Endpoint                     | Description           |
| -------- | ---------------------------- | --------------------- |
| `GET`    | `/health`                    | API health check      |
| `GET`    | `/db-health`                 | Database health check |
| `POST`   | `/api/monitors`              | Create a monitor      |
| `GET`    | `/api/monitors`              | List monitors         |
| `GET`    | `/api/monitors/{id}`         | Get a monitor         |
| `PATCH`  | `/api/monitors/{id}`         | Update a monitor      |
| `DELETE` | `/api/monitors/{id}`         | Delete a monitor      |
| `POST`   | `/api/monitors/{id}/pause`   | Pause a monitor       |
| `POST`   | `/api/monitors/{id}/resume`  | Resume a monitor      |
| `GET`    | `/api/monitors/{id}/history` | View monitor history  |
| `POST`   | `/api/ping/{token}`          | Success ping          |
| `POST`   | `/api/ping/{token}/start`    | Start ping            |
| `POST`   | `/api/ping/{token}/fail`     | Failure ping          |

## Security

Do not commit your `.env` file.

Ping tokens should be treated as secrets. Anyone with a monitor token can send pings for that monitor.

For public or shared deployments, run MissedRun behind HTTPS and restrict access to the API/dashboard as needed.

## License

MissedRun Self-hosted is licensed under the GNU Affero General Public License v3.0.

See the `LICENSE` file for details.
