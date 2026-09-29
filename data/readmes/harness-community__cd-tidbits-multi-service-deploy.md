# CD Tidbit — Multi-Service Deploy (Fan-out / Fan-in)

Deploy **two independent services in one pipeline run** using parallel stages that converge at the end.

```
              ┌─── Deploy Service A (cart-frontend) ───┐
  Pipeline ───┤                                         ├──► Converge
              └─── Deploy Service B (cart-backend)  ───┘
                   (both run at the same time)           (runs only after both succeed)
```

---

## How it works

1. **Fan-out** — Harness starts both Deploy stages at the same time (parallel block).
2. Each stage deploys its own service into the shared Kubernetes namespace independently.
3. **Fan-in** — The `Converge` stage starts only after both deploys succeed. If either fails, it rolls back that service and the pipeline stops.

> The shared infrastructure needs `allowSimultaneousDeployments: true` — without it, Harness serializes parallel stages on the same infra, and they run one after another instead of together.

---

## Prerequisites

| What you need | Default in this repo |
|---|---|
| Kubernetes Cluster connector (with delegate) | `account.k8s_delegate` |
| DockerHub connector (anonymous OK) | `account.Docker` |
| GitHub connector pointing to this repo | `account.GitHub` |
| Harness org + project | `default` / `project_1` |

---

## Files

```
.harness/
  pipeline.yaml        ← the pipeline (fan-out → fan-in)
  serviceA.yaml        ← Service A definition (cart-frontend, nginx:1.27-alpine)
  serviceB.yaml        ← Service B definition (cart-backend, nginx:stable-alpine)
  environment.yaml     ← shared Dev environment
  infrastructure.yaml  ← shared K8s infra (allowSimultaneousDeployments: true)

k8s/
  serviceA/            ← Go-templated K8s manifests for Service A
    namespace.yaml
    deployment.yaml
    service.yaml
    values.yaml
  serviceB/            ← Go-templated K8s manifests for Service B
    namespace.yaml
    deployment.yaml
    service.yaml
    values.yaml
```

The services pull manifests directly from this repo via a GitHub connector. No separate upload step needed.

---

## Setup

### 1. Replace placeholders

Search all `.harness/*.yaml` files for `# REPLACE:` and swap in your actual values:

- `orgIdentifier` — your Harness org
- `projectIdentifier` — your Harness project
- `connectorRef: account.GitHub` — your GitHub connector (pointing to this repo)
- `connectorRef: account.k8s_delegate` — your K8s connector
- `connectorRef: account.Docker` — your DockerHub connector
- `branch: main` — your default branch name
- Namespace `tidbit-0068` — whatever namespace you want

### 2. Import entities (in this order)

1. **Services** — `Deployments → Services → New Service → YAML` — import `serviceA.yaml`, then `serviceB.yaml`
2. **Environment** — `Deployments → Environments → New → YAML` — import `environment.yaml`
3. **Infrastructure** — open `env_dev_tid0068 → Infrastructure → New → YAML` — import `infrastructure.yaml`
4. **Pipeline** — `Pipelines → Create → Inline → YAML` — paste `pipeline.yaml`

### 3. Run

Hit **Run** on the pipeline. Both Deploy stages should start together and finish independently. `Converge` runs last.

---

## Verify it worked

```bash
kubectl -n tidbit-0068 get deployments
# Expected:
# cart-frontend-deployment   1/1   Ready
# cart-backend-deployment    1/1   Ready
```

The `Converge` stage logs will show:
```
Service A stage status: SUCCESS
Service B stage status: SUCCESS
```

---

## Troubleshooting

**Stages run one after another, not in parallel**
The infra is missing `allowSimultaneousDeployments: true`. Harness adds a resource-constraint step to every deploy stage — without this flag, two stages on the same infra are serialized.

**`namespace "tidbit-0068" not found`**
`namespace.yaml` must be listed **first** in each service's `paths[]` array. Also confirm `createNamespace: true` in `values.yaml`.

**One pod overwrites the other**
Each service must have a unique `name` in its `values.yaml` (`cart-frontend` vs `cart-backend`). This drives distinct Deployment names and `app:` label selectors.

**Converge runs even though a deploy failed**
Check the `when` condition on the Converge stage — it should be `stageStatus: Success` (the default). If changed, restore it.

---

## Learn more

- [Multi-service deployments](https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/advanced/multiserv-multienv/)
- [Run stages in parallel](https://developer.harness.io/docs/platform/pipelines/looping-strategies/run-stages-in-parallel/)
- [Sequential and parallel deployments](https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/sequential-and-parallel-deployments/)
