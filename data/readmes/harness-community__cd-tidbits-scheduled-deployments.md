# CD: Scheduled Deployments — Time-Based Triggers for Non-Production Environments

> **Harness University Tidbit.** A 5–10 minute, self-paced micro-lesson backed by an executable repo.
> **Skill:** Wire a Cron Trigger to a CD pipeline so dev gets the latest build every night and staging is ready every morning — zero manual pipeline runs needed.

## What this skill accomplishes

- Creates a native Harness **Cron Trigger** to automatically run a CD pipeline on a schedule
- Deploys to dev every night at 2 AM so the environment always has the latest main-branch build
- Deploys to staging every weekday morning at 6 AM before the team starts work
- Uses a pipeline input YAML in the trigger so each schedule targets the right environment
- No cron jobs, no external schedulers, no API calls — Harness evaluates the schedule natively

## How it works

```
┌─── Harness Trigger Engine ─────────────────────────────────────────┐
│                                                                      │
│  Cron Trigger: "Nightly Dev Deploy"                                  │
│  Schedule: 0 2 * * *   (every day at 2 AM UTC)                       │
│  ─────────────────────────────────────────────────────────────────── │
│  Input YAML:  environment = dev                                       │
│               appVersion  = latest                                    │
│                         │                                             │
│                         ▼ fires                                       │
│              ┌─── Deploy Pipeline ────┐                               │
│              │  Stage: Deploy to dev  │                               │
│              └────────────────────────┘                               │
│                                                                       │
│  Cron Trigger: "Weekday Staging Deploy"                               │
│  Schedule: 0 6 * * 1-5   (Mon–Fri at 6 AM UTC)                       │
│  ─────────────────────────────────────────────────────────────────── │
│  Input YAML:  environment = staging                                   │
│               appVersion  = <+trigger.artifact.tag>                  │
│                         │                                             │
│                         ▼ fires                                       │
│              ┌─── Deploy Pipeline ────────┐                           │
│              │  Stage: Deploy to staging  │                           │
│              └────────────────────────────┘                           │
└──────────────────────────────────────────────────────────────────────┘
```

## Repo layout

```
cd-tidbits-scheduled-deployments/
├── README.md
├── .harness/
│   └── pipeline.yaml                  ← CD pipeline with runtime environment input
└── triggers/
    ├── trigger-nightly-dev.yaml       ← Reference: Cron trigger for dev (daily 2 AM)
    └── trigger-weekday-staging.yaml   ← Reference: Cron trigger for staging (Mon–Fri 6 AM)
```

> **Note**: Trigger YAML files in `triggers/` are reference definitions. In Harness, triggers are managed under **Pipelines → Triggers**. You can also import trigger YAML directly from the Triggers UI.

## Prerequisites

| Requirement | Details |
|---|---|
| Harness CD license | Required for pipeline triggers |
| CD pipeline | An existing pipeline with `environment` as a pipeline variable |
| Service with artifact tag | `appVersion` or image tag must be configurable as a pipeline input |
| Permissions | Need Pipelines: Execute permission to create triggers |

## Steps

### 1. Make your pipeline trigger-friendly

Your CD pipeline must accept environment and version as inputs, not hardcoded values. Open your pipeline and ensure:

- An `environment` **pipeline variable** with value `<+input>`
- An `appVersion` **pipeline variable** with value `<+input>` (or a fixed default like `latest`)

This lets each trigger override these values independently.

### 2. Create the nightly dev trigger

Navigate to your pipeline → **Triggers** → **New Trigger** → **Cron**.

Configure:
- **Name**: Nightly Dev Deploy
- **Timezone**: UTC (default) or set to your team's timezone if the feature flag `PIPE_SUPPORT_MULTIPLE_TIMEZONES_IN_CRON_TRIGGERS` is enabled
- **Schedule**: Use the **Custom** tab, select **UNIX Expression**, enter `0 2 * * *`
  - This fires at minute 0, hour 2, every day, every month, every day of week = 2:00 AM every night
- **Pipeline Input**: Set `environment = dev`, `appVersion = latest`

Click **Create Trigger**.

### 3. Create the weekday staging trigger

Navigate to your pipeline → **Triggers** → **New Trigger** → **Cron**.

Configure:
- **Name**: Weekday Staging Deploy
- **Schedule**: `0 6 * * 1-5`
  - Fires at 6 AM Monday through Friday
- **Pipeline Input**: Set `environment = staging`, `appVersion = latest`

Click **Create Trigger**.

### 4. Test a trigger manually

After creating a trigger, click the **Run Once** button next to it to fire it immediately and verify the pipeline runs correctly with the trigger's input values.

### 5. Monitor trigger history

Navigate to **Pipelines → Triggers**. The trigger list shows each trigger's last run time, status, and next scheduled run. Click a trigger to view its full invocation history.

## Cron expression reference

| Expression | Meaning |
|---|---|
| `0 2 * * *` | Every night at 2:00 AM UTC |
| `0 6 * * 1-5` | Weekdays (Mon–Fri) at 6:00 AM UTC |
| `0 22 * * 5` | Every Friday at 10:00 PM UTC (pre-weekend deploy) |
| `0 0 * * 0` | Every Sunday at midnight UTC (weekly cleanup) |
| `30 8 1 * *` | First day of every month at 8:30 AM UTC |
| `0 */4 * * *` | Every 4 hours |

> Cron expressions are evaluated in UTC. If you need a specific timezone, contact Harness Support to enable the `PIPE_SUPPORT_MULTIPLE_TIMEZONES_IN_CRON_TRIGGERS` feature flag.

## Key concepts

| Concept | Description |
|---|---|
| **Cron Trigger** | A native Harness trigger type that fires on a schedule. No external scheduler needed |
| **UNIX cron expression** | 5-field format: `minute hour day-of-month month day-of-week` |
| **Quartz expression** | 6-field format with seconds and optional year. Alternative to UNIX |
| **Trigger Input YAML** | A YAML block in the trigger that provides pipeline variable values when the trigger fires |
| **Run Once** | A button in the Triggers UI that fires the trigger immediately for testing |
| **Triggers freeze** | When a freeze window is active, scheduled trigger invocations are rejected |
| **Trigger disable** | Toggle a trigger off without deleting it — useful during incidents or maintenance |
