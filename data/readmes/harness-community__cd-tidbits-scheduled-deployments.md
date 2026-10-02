# CD: Scheduled Deployments — Time-Based Triggers for Non-Production Environments

> **Harness University Tidbit.** A 5–10 minute, self-paced micro-lesson backed by an executable repo.
> **Skill:** Wire a Cron Trigger to a CD pipeline so dev gets the latest build every night — zero manual pipeline runs needed.

## What this skill accomplishes

- Creates a native Harness **Cron Trigger** to automatically run a CD pipeline on a schedule
- Deploys to dev every night at 2 AM so the environment always has the latest main-branch build
- Uses a pipeline input YAML in the trigger so each schedule targets the right environment
- No cron jobs, no external schedulers, no API calls — Harness evaluates the schedule natively

## How it works

```
┌─── Harness Trigger Engine ─────────────────────────────────────────┐
│                                                                      │
│  Cron Trigger: "Nightly Dev Deploy"                                  │
│  Schedule: 0 2 * * *   (every day at 2 AM UTC)                       │
│  ─────────────────────────────────────────────────────────────────── │
│  Input YAML:  environment = env_dev_tid0062                            │
│  Pipeline:    appVersion  = latest                                    │
│                         │                                             │
│                         ▼ fires                                       │
│              ┌─── Deploy Pipeline ────┐                               │
│              │  Stage: Deploy to dev  │                               │
│              └────────────────────────┘                               │
└──────────────────────────────────────────────────────────────────────┘
```

## Repo layout

```
cd-tidbits-scheduled-deployments/
├── README.md
├── .harness/
│   ├── environment.yaml               ← Dev environment
│   ├── infrastructure.yaml            ← Reference Kubernetes infrastructure definition
│   ├── pipeline.yaml                  ← CD pipeline with runtime environment input
│   ├── service.yaml                   ← Kubernetes service backed by this Git repo
│   └── trigger-nightly-dev.yaml       ← Reference: Cron trigger for dev (daily 2 AM)
└── k8s/
    ├── deployment.yaml                ← Kubernetes Deployment manifest
    ├── namespace.yaml                 ← Kubernetes Namespace manifest
    ├── service.yaml                   ← Kubernetes Service manifest
    └── values.yaml                    ← Manifest values
```

> **Note**: The trigger YAML file in `.harness/` is a reference definition. In Harness, triggers are managed under **Pipelines → Triggers**. You can also import trigger YAML directly from the Triggers UI.

## Prerequisites

| Requirement | Details |
|---|---|
| Harness CD license | Required for pipeline triggers |
| Harness project | An organization and project where you can create the supplied service, environment, pipeline, and trigger |
| Connectors | A GitHub connector, Docker Registry connector, and Kubernetes Cluster connector |
| Kubernetes delegate | A Harness Delegate with access to the target Kubernetes cluster |
| Repository | A fork or copy of this repository on the branch referenced by `.harness/service.yaml` |
| Permissions | Pipeline creation/editing and pipeline execution permissions may both be required to create triggers, depending on the project's pipeline settings |

## Steps

### 1. Configure the supplied YAML

Fork or copy this repository, then update every value marked `REPLACE` in `.harness/environment.yaml`, `.harness/service.yaml`, `.harness/infrastructure.yaml`, and `.harness/pipeline.yaml`.

- In `.harness/service.yaml`, set the GitHub connector, repository name, branch, and Docker Registry connector.
- In `.harness/infrastructure.yaml`, set the Kubernetes Cluster connector. This file is a reference standalone infrastructure definition; the supplied pipeline defines its infrastructure inline.
- In `.harness/pipeline.yaml`, set the organization and project identifiers, set `serviceRef` to the service identifier from `.harness/service.yaml` (`svc_tid0062` by default), and set the Docker Registry and Kubernetes Cluster connector references. For the supplied nginx service, use `library/nginx` as the image path.
- In `.harness/trigger-nightly-dev.yaml`, keep `pipelineIdentifier` and the nested input YAML identifier aligned with the pipeline identifier, set `pipelineBranchName` to the branch that stores the pipeline, and change the `environment` input from `dev` to the environment identifier from `.harness/environment.yaml` (`env_dev_tid0062` by default).

Create the resources in this order: environment, service, pipeline, then trigger. The service reads the manifests directly from this repository's `k8s/` directory.

### 2. Make your pipeline trigger-friendly

Your CD pipeline must accept the environment, and any version that each schedule needs to override, as inputs. Open your pipeline and ensure:

- An `environment` **pipeline variable** with value `<+input>`
- An `appVersion` **pipeline variable** with value `<+input>` (or keep the supplied fixed default `latest`)

This lets each trigger override the runtime input values independently. The supplied pipeline only requires `environment` at runtime; change `appVersion` to `<+input>` if a trigger must override it.

### 3. Create the nightly dev trigger

Navigate to your pipeline → **Triggers** → **New Trigger** → **Cron**.

Configure:
- **Name**: Nightly Dev Deploy
- **Timezone**: UTC (default) or set to your team's timezone if the feature flag `PIPE_SUPPORT_MULTIPLE_TIMEZONES_IN_CRON_TRIGGERS` is enabled
- **Schedule**: Use the **Custom** tab, select **UNIX Expression**, enter `0 2 * * *`
  - This fires at minute 0, hour 2, every day, every month, every day of week = 2:00 AM every night
- **Pipeline Input**: Set `environment = env_dev_tid0062` (or your environment identifier). Set `appVersion = latest` only if you changed `appVersion` to `<+input>`.

Click **Create Trigger**.

You can instead copy `.harness/trigger-nightly-dev.yaml` into the trigger YAML editor after making the replacements described in step 1.

### 4. Create the weekday staging trigger (optional)

This repository does not include a staging environment or staging trigger definition. Create a staging environment first, then use the same process.

Navigate to your pipeline → **Triggers** → **New Trigger** → **Cron**.

Configure:
- **Name**: Weekday Staging Deploy
- **Schedule**: `0 6 * * 1-5`
  - Fires at 6 AM Monday through Friday
- **Pipeline Input**: Set `environment` to your staging environment identifier. Set `appVersion = latest` only if you changed `appVersion` to `<+input>`.

Click **Create Trigger**.

### 5. Test a trigger manually

After creating a trigger, click the **Run Once** button next to it to fire it immediately and verify the pipeline runs correctly with the trigger's input values.

### 6. Monitor trigger history

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
