# Harness CD — Environment & Infrastructure Setup

Set up the **"where"** of a Harness deployment: an **Environment** (Dev/QA) with a **Kubernetes Infrastructure Definition** bound to it. Every CD pipeline needs this pair before it can deploy anything.

---

## How the pieces fit together

```
Environment  (type: PreProduction)
 └── Infrastructure Definition  (type: KubernetesDirect)
        ├── connectorRef  →  which cluster
        ├── namespace     →  where in the cluster
        └── releaseName   →  unique ID per release (auto-generated)
```

- One Environment can hold **many** Infrastructure Definitions (e.g. two clusters for the same QA env).
- One Infrastructure Definition belongs to **exactly one** Environment.

---

## Core concepts

| Concept | What it is |
|---|---|
| **Environment** | A logical target — Dev, QA, Staging, Prod. Holds variables and infrastructure. |
| **Environment type** | `PreProduction` (non-prod) or `Production`. Controls RBAC and freeze windows. |
| **Infrastructure Definition** | The concrete cluster + namespace inside an environment. |
| **K8s Direct** | Connection type using a Harness Kubernetes Cluster connector. |
| **connectorRef** | Reference to a pre-created Kubernetes Cluster connector. |

---

## Prerequisites

- Harness account with a project (CD module enabled)
- A **Kubernetes Cluster connector** already created (`account.<id>`, `org.<id>`, or project-scoped)
- An **existing namespace** in your cluster — `kubectl create namespace <name>`

> No connector yet? See [Kubernetes Cluster connector settings](https://developer.harness.io/docs/platform/connectors/cloud-providers/ref-cloud-providers/kubernetes-cluster-connector-settings-reference/).

---

## Files

| File | What it does |
|---|---|
| `.harness/environment.yaml` | Environment definition (Dev/QA, Pre-Production) |
| `.harness/infrastructure.yaml` | K8s Direct Infrastructure Definition bound to that environment |

Every value you must change is marked `# REPLACE:`.

---

## Steps

### Option A — Harness UI (recommended for first-timers)

1. **Create the Environment**
   Deployments → **Environments** → **New Environment**
   Set a name (e.g. `Dev`), type = **Pre-Production**, save.
   *(Want YAML? Switch the editor to YAML and paste `.harness/environment.yaml`, filling in the `# REPLACE:` lines first.)*

2. **Add the Infrastructure Definition**
   Open the environment → **Infrastructure Definitions** → **New Infrastructure Definition**
   - Deployment Type: **Kubernetes**
   - Infrastructure Type: **Direct Connection**
   - Connector: your Kubernetes Cluster connector
   - Namespace: your existing namespace
   - Release Name: leave as `release-<+INFRA_KEY_SHORT_ID>`
   - Save.
   *(Or paste `.harness/infrastructure.yaml` in YAML mode.)*

3. **Verify**
   The environment now shows one infrastructure definition. Any CD pipeline stage can use this pair as its deployment target.

### Option B — YAML

1. Edit the `# REPLACE:` lines in both `.harness/*.yaml`.
2. Import via **Environments → New Environment → YAML** (paste and save).
3. Repeat for the Infrastructure Definition inside the environment.

---

## Expected result

- One **Pre-Production** environment under Deployments → Environments
- One **Kubernetes (Direct)** infrastructure definition listed inside it
- Nothing is deployed — this is just the deployment target, ready to be referenced by a pipeline

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `Infrastructure references environment ... which does not exist` | Environment not yet created, or `environmentRef` typo | Create the environment first; check `environmentRef` matches the environment `identifier` exactly |
| `Invalid connectorRef` | Wrong scope prefix or wrong id | Use `account.<id>`, `org.<id>`, or just `<id>` for project scope |
| Save blocked by a policy | An OPA policy set is enforcing rules | Ask an admin to review Policy Sets under Project Settings → Governance |
| Namespace errors at deploy time | Namespace doesn't exist in the cluster | Run `kubectl create namespace <name>` — Harness won't create it for K8s Direct |

---

## Reference

- [Environments overview](https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/environments/environment-overview)
- [Create environments](https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/environments/create-environments)
- [Define Kubernetes target infrastructure](https://developer.harness.io/docs/continuous-delivery/deploy-srv-diff-platforms/kubernetes/define-your-kubernetes-target-infrastructure/)

---

## Video Script

> Quick to read aloud. ~90 seconds at a comfortable pace.

---

**[INTRO]**
In this video, we're setting up the "where" of a Harness deployment — an Environment and an Infrastructure Definition.

**[WHAT IS AN ENVIRONMENT?]**
An Environment is a logical target — Dev, QA, Staging, or Prod. It has a type: PreProduction for anything non-prod, Production for prod. That type controls who can deploy and when, through RBAC and freeze windows.

**[WHAT IS AN INFRASTRUCTURE DEFINITION?]**
Inside an Environment, you attach one or more Infrastructure Definitions. Each one points at a real cluster and a real namespace. Together, the Environment and the Infrastructure Definition tell Harness exactly where to drop your service.

**[THE RELATIONSHIP]**
Think of it this way — the Environment is the city. The Infrastructure Definition is the exact street address. Any CD pipeline that wants to deploy needs both.

**[PREREQUISITES]**
Before we start: make sure you have a Harness project with CD enabled, a Kubernetes Cluster connector already set up, and a namespace ready in your cluster.

**[STEP 1 — CREATE THE ENVIRONMENT]**
Go to Deployments, then Environments, then New Environment. Give it a name like "Dev", set the type to Pre-Production, and save. Or switch to YAML mode and paste the environment file from this repo.

**[STEP 2 — ADD THE INFRASTRUCTURE DEFINITION]**
Open that environment, click Infrastructure Definitions, then New Infrastructure Definition. Choose Kubernetes as the deployment type, Direct Connection as the type, pick your connector, enter your namespace, and save. Leave the release name expression as-is — Harness auto-generates a safe name.

**[VERIFY]**
You should now see your environment with one infrastructure definition listed inside it. That's your deployment target, ready to go.

**[WRAP UP]**
That's it. No pipeline, no service — just a clean, reusable deployment target that any CD stage can point at. Next, we'll attach a service and kick off an actual deployment.
