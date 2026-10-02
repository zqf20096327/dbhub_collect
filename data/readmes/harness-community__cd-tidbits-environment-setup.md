# Harness CD — Environment & Infrastructure Setup

This tidbit is about the **Environment**: the logical *where* of a Harness deployment. Dev, QA, Staging, and Prod are environments. The cluster and namespace sit one level down, on an Infrastructure Definition.

An environment names the destination, holds variables that apply to every deployment into it, and owns one or more **Infrastructure Definitions**. A pipeline stage points at an environment, then at an infrastructure definition inside it.

---

## How the pieces fit together

```
Pipeline stage
 ├── Service                     →  what you deploy
 └── Environment                 →  where you deploy (logical)
      └── Infrastructure Definition
             ├── connectorRef   →  which cluster
             ├── namespace      →  where in the cluster
             └── releaseName    →  unique ID per release (auto-generated)
```

- One Environment can hold **many** Infrastructure Definitions (two clusters for the same QA environment, for example).
- One Infrastructure Definition belongs to **exactly one** Environment. Its `environmentRef` must match that environment's `identifier`.
- The Service is chosen separately. The same service can deploy into many environments.
- `type` is `PreProduction` or `Production`. Production is the type that stricter RBAC and deployment freeze windows check.

---

## Core concepts

| Concept | What it is |
|---|---|
| **Environment** | A named destination — Dev, QA, Staging, Prod. Holds variables and infrastructure. |
| **Environment type** | `PreProduction` or `Production`. Production is checked by RBAC and freeze windows. |
| **Identifier** | Immutable after save. Infrastructure and pipelines reference it via `environmentRef`. |
| **Infrastructure Definition** | The concrete cluster + namespace inside one environment. |
| **K8s Direct** | Connection type that uses a Harness Kubernetes Cluster connector. Harness applies manifests itself. |
| **connectorRef** | Reference to a Kubernetes Cluster connector that already exists (`account.<id>`, `org.<id>`, or a project-scoped id). |

---

## Prerequisites

- Harness account with a project (CD module enabled)
- A **Kubernetes Cluster connector** already created (`account.<id>`, `org.<id>`, or project-scoped)
- An **existing namespace** in your cluster — `kubectl create namespace <name>`

> No connector yet? See [Kubernetes cluster connector settings](https://developer.harness.io/harness-platform/use-harness-platform/connectors/cloud-providers/add-a-kubernetes-cluster-connector/kubernetes-cluster-connector-settings-reference).

---

## Files

| File | What it does |
|---|---|
| `.harness/environment.yaml` | The environment (Dev/QA, `PreProduction`) |
| `.harness/infrastructure.yaml` | K8s Direct infrastructure bound to that environment |
| `.harness/service.yaml` | The workload deployed into the environment (nginx + Kubernetes manifests) |
| `.harness/pipeline.yaml` | One rolling deploy stage that references the service, environment, and infrastructure |

Values to fill in are marked `# REPLACE:` in the environment and infrastructure files, and as `<YOUR_…>` placeholders in the service and pipeline.

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

1. Edit the `# REPLACE:` lines in `.harness/environment.yaml` and `.harness/infrastructure.yaml`.
2. Import via **Environments → New Environment → YAML** (paste and save).
3. Repeat for the Infrastructure Definition inside the environment.

Create the environment before the infrastructure. `environmentRef` is checked against an environment that already exists.

---

## Also in this tidbit

These two files complete the deployment. They are here so the environment has something to receive and a stage that targets it. Fill in the `<YOUR_…>` placeholders before importing.

**`.harness/service.yaml`** — the *what*. A Kubernetes service whose primary artifact is `library/nginx` (`stable`) from a Docker registry connector. Manifests (`k8s/namespace.yaml`, `k8s/deployment.yaml`, `k8s/service.yaml`, and `k8s/values.yaml`) are read from a GitHub repo on `main`. `gitOpsEnabled` is `false`, so Harness applies the manifests.

Import: Deployments → **Services** → **New Service** → YAML.

**`.harness/pipeline.yaml`** — the *how*. One Deployment stage (`Deploy to Dev`) using the Rolling strategy. It sets `serviceRef`, `environmentRef`, and a single infrastructure identifier (`deployToAll: false`). The stage runs `K8sRollingDeploy` (dry run on, pruning off) and, on any error, rolls the stage back with `K8sRollingRollback`.

Import: Deployments → **Pipelines** → **Create a Pipeline** → Inline → YAML.

---

## Expected result

- One **Pre-Production** environment under Deployments → Environments
- One **Kubernetes (Direct)** infrastructure definition listed inside it
- Optionally, a Kubernetes service and a one-stage rolling pipeline that target that pair
- The environment is the deployment target; a deploy happens when that pipeline is run

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

**Environment and infrastructure**

- [Environments overview](https://developer.harness.io/continuous-delivery/use-continuous-delivery/cd-building-blocks/environments/environment-overview)
- [Create environments](https://developer.harness.io/continuous-delivery/use-continuous-delivery/cd-building-blocks/environments/create-environments)
- [Define Kubernetes target infrastructure](https://developer.harness.io/continuous-delivery/use-continuous-delivery/deploy-services-on-different-platforms/kubernetes/define-your-kubernetes-target-infrastructure)

**Service**

- [Services overview](https://developer.harness.io/continuous-delivery/use-continuous-delivery/cd-building-blocks/services/services-overview)
- [Kubernetes services](https://developer.harness.io/continuous-delivery/use-continuous-delivery/deploy-services-on-different-platforms/kubernetes/kubernetes-services)
- [Add Kubernetes manifests](https://developer.harness.io/continuous-delivery/use-continuous-delivery/deploy-services-on-different-platforms/kubernetes/cd-kubernetes-category/define-kubernetes-manifests)
- [Add container image artifacts](https://developer.harness.io/continuous-delivery/use-continuous-delivery/deploy-services-on-different-platforms/kubernetes/cd-kubernetes-category/add-artifacts-for-kubernetes-deployments)

**Connectors**

- [Connectors overview](https://developer.harness.io/harness-ai/use-harness-platform/connectors)
- [Add a Kubernetes cluster connector](https://developer.harness.io/harness-ai/use-harness-platform/connectors/cloud-providers/add-a-kubernetes-cluster-connector)
- [Kubernetes cluster connector settings](https://developer.harness.io/harness-platform/use-harness-platform/connectors/cloud-providers/add-a-kubernetes-cluster-connector/kubernetes-cluster-connector-settings-reference)
- [Docker Registry connector settings](https://developer.harness.io/harness-platform/use-harness-platform/connectors/artifact-repositories/ref-artifact-repositories/docker-registry-connector-settings-reference)
- [Connect to a code repository](https://developer.harness.io/harness-ai/use-harness-platform/connectors/code-repositories/connect-to-code-repo)
- [Git connector settings](https://developer.harness.io/harness-ai/use-harness-platform/connectors/code-repositories/ref-source-repo-provider/git-connector-settings-reference)

**Pipeline**

- [Create a Kubernetes rolling deployment](https://developer.harness.io/continuous-delivery/use-continuous-delivery/deploy-services-on-different-platforms/kubernetes/kubernetes-executions/create-a-kubernetes-rolling-deployment)
- [Kubernetes rollback](https://developer.harness.io/continuous-delivery/use-continuous-delivery/deploy-services-on-different-platforms/kubernetes/cd-k8s-ref/kubernetes-rollback)
- [Failure strategies](https://developer.harness.io/harness-ai/use-harness-platform/pipelines/failure-handling/define-a-failure-strategy-on-stages-and-steps)
