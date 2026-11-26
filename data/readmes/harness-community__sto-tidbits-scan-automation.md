# STO: Scan Automation — Gitleaks, Semgrep and Aqua Trivy in One Pipeline

> **Harness University Tidbit.** A 5–10 minute, self-paced micro-lesson backed by an executable repo.
> **Skill:** Scan a sample app end to end — secrets (Gitleaks) and SAST (Semgrep) in parallel, then build the Docker image, push it to **Harness Artifact Registry (HAR)**, and scan it for CVEs with Aqua Trivy.

## What this skill accomplishes

- Runs **Gitleaks** and **Semgrep** concurrently using a step group with `parallel:`
- Builds the sample app's `Dockerfile` and pushes it to **Harness Artifact Registry** — no Docker connector needed
- Scans the pushed image with **Aqua Trivy**, pulling it back from HAR
- Ships a deliberately vulnerable **sample app at the repo root** so every scanner has findings to show
- Each scanner has its own `fail_on_severity` gate
- All findings appear in the **Security Tests** tab of the execution

## How it works

One CI stage on Harness Cloud runs three steps in order:

```
 Stage: Scan and Build (CI, Harness Cloud)
 ┌──────────────────────────────────────────────┐
 │ 1. Step group: Parallel Code Scanners        │
 │     ┌───────────────┐   ┌───────────────┐    │
 │     │   Gitleaks    │   │    Semgrep    │    │
 │     │ hardcoded     │   │ SAST: SQLi,   │    │
 │     │ secrets       │   │ cmd injection │    │
 │     └───────────────┘   └───────────────┘    │
 │                    │                         │
 │                    ▼                         │
 │ 2. Build and Push: Dockerfile (repo root)    │
 │    ──► Harness Artifact Registry (HAR)       │
 │                    │                         │
 │                    ▼                         │
 │ 3. Aqua Trivy: pulls <registry>/<image>:<tag>│
 │    from HAR and scans it                     │
 └──────────────────────────────────────────────┘
```

## Scanner coverage at a glance

| Scanner | Step Type | Target | What it finds | Seeded in the sample app |
|---|---|---|---|---|
| **Gitleaks** | `Gitleaks` | Repository | Hardcoded secrets and tokens | Fake GitHub token in `app.py` |
| **Semgrep** | `Semgrep` | Repository | Insecure code patterns (SAST) | SQL injection, command injection, Flask debug mode in `app.py` |
| **Aqua Trivy** | `AquaTrivy` | Container image | OS and package CVEs in image layers | Old base image and pinned old libraries in `Dockerfile` / `requirements.txt` |

## Repo layout

The sample app sits **directly at the repo root** (no wrapper directory):

```
sto-tidbits-scan-automation/
├── app.py                  ← sample Flask app (intentionally insecure)
├── requirements.txt        ← old pinned dependencies (Trivy findings)
├── Dockerfile              ← built and pushed to HAR by the pipeline
├── .dockerignore
├── README.md
└── .harness/
    └── pipeline.yaml       ← single stage: code scans → build/push → image scan
```

> ⚠️ **The sample app is intentionally vulnerable and the token in `app.py` is fake.** Never deploy it, and never commit real secrets.

## Prerequisites

| Requirement | Details |
|---|---|
| Harness STO + CI licenses | STO for the scan steps, CI for the build and push step |
| Git connector | Points at this repo; set in the pipeline's codebase settings |
| HAR Docker registry | Create one under **Artifact Registries → New Artifact Registry → Docker** |
| Two Harness secrets | `har_username` (Harness user or service account) and `har_api_token` (Harness API token) — used by Trivy to pull the image from HAR |
| Harness Cloud | The pipeline's single stage runs on Harness Cloud (Linux/AMD64) |

## Steps

### 1. Import the pipeline

Create a pipeline in your project and paste in [.harness/pipeline.yaml](.harness/pipeline.yaml), or import it from this repo. When you run it you are prompted for the codebase connector, repo name, branch, and your HAR registry name.

### 2. Code scans: Gitleaks + Semgrep in parallel

Both steps use `mode: orchestration` (Harness runs the scanner and ingests the results in one step) and `target.type: repository`. Placing them under `parallel:` inside a step group starts both at the same time:

```yaml
- stepGroup:
    name: Parallel Code Scanners
    identifier: parallel_code_scanners
    steps:
      - parallel:
          - step: { type: Gitleaks, ... }
          - step: { type: Semgrep, ... }
```

Neither step needs a token. They scan the source cloned by the stage (`cloneCodebase: true`).

### 3. Build and push the image to Harness Artifact Registry

In the same **Build** (CI) stage, after the scanners, use the **Build and Push an image to Docker Registry** step. Leave the registry type as **Harness Artifact Registry**, pick your registry, enter the image name and tags. No connector is needed.

```yaml
- step:
    type: BuildAndPushDockerRegistry
    spec:
      registryRef: <+pipeline.variables.HAR_REGISTRY>
      repo: <+pipeline.variables.IMAGE_NAME>
      tags:
        - <+pipeline.variables.IMAGE_TAG>
      dockerfile: Dockerfile
      context: .
```

### 4. Scan the pushed image with Aqua Trivy

The last step runs Trivy with `image.type: docker_v2` against HAR. On Harness Cloud no Docker-in-Docker background step is needed:

```yaml
image:
  type: docker_v2
  domain: pkg.harness.io
  name: <account_id>/<registry>/<image>
  tag: <tag>
  access_id: <+secrets.getValue("har_username")>
  access_token: <+secrets.getValue("har_api_token")>
```

Open your registry in HAR and click **Setup Client** to confirm the exact host and path for your account.

### 5. Run and review

Run the pipeline, then open the **Security Tests** tab. Expect:

- Gitleaks: one finding (the fake GitHub token)
- Semgrep: findings for SQL injection, command injection and debug mode
- Trivy: CVEs from the old base image and pinned Python libraries; the step fails on any **Critical**

Findings are tracked per target and variant, so re-runs show what is new or fixed.

### 6. Watch resource usage

Parallel steps all run at once. If a runner runs out of CPU or memory, steps fail. On Harness Cloud this is rarely a problem for two scanners.

## Key concepts

| Concept | Description |
|---|---|
| **Step group + `parallel:`** | A named container for steps. Children under `parallel:` run concurrently |
| **Orchestration mode** | The STO step runs the scanner and ingests, normalizes and deduplicates the results |
| **Harness Artifact Registry** | Harness-native registry. CI can push to it without a connector |
| **Fail on severity** | Per-step threshold. A finding at that level or higher fails the pipeline |
| **Targets and variants** | A target is the thing scanned (repo or image); the variant is the branch or tag. STO compares variants against a baseline |

## References

- [Gitleaks step configuration](https://developer.harness.io/security-testing-orchestration/use-sto/sto-scanner-configuration/gitleaks-scanner-reference)
- [Semgrep step configuration](https://developer.harness.io/security-testing-orchestration/use-sto/sto-scanner-configuration/semgrep/semgrep-scanner-reference)
- [Aqua Trivy step configuration](https://developer.harness.io/security-testing-orchestration/use-sto/sto-scanner-configuration/trivy/aqua-trivy-scanner-reference)
- [Artifact Registry and CI integrations](https://developer.harness.io/artifact-registry/use-artifact-registry/platform-integrations/ci-ar-integrations)
