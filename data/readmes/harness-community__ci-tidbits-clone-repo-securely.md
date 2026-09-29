# CI Tidbit — Clone a Repo Securely

Clone your application code into a Harness CI pipeline using a **codebase connector**, so the Git credential lives in a Harness Secret — never in your pipeline YAML and never in your build logs. This tidbit shows a `connectorRef`, a `repoName` supplied at runtime (`<+input>`), and `cloneCodebase: true` — then proves the clone happened with a single Run step, including a `git remote -v` that has no token in it.

## What this skill accomplishes

Harness CI clones your source at the start of a build using a codebase connector. The connector holds the Git URL and references a Harness Secret for the credential; your pipeline only names the connector with `connectorRef`. The token is resolved at runtime by the Harness Platform — never written into the YAML, never committed to Git, never printed in logs. That is what "securely" means here.

## What you will build

A single CI stage on Harness Cloud with `cloneCodebase: true` and one Run step that prints:

- `pwd` — the workspace the repo was cloned into
- a file listing of the cloned repo root
- `git log -1 --oneline` — the latest commit, proving real content
- `git remote -v` — the remote URL, showing **no credential is embedded**

No app to build, no test to run, no delegate — the clone itself is the skill.

## Prerequisites

- A Harness account with a Project (note its org + project identifiers).
- Permission to create and run pipelines.
- A **code repo connector** (GitHub/GitLab/Bitbucket/Git) whose **Connectivity Mode is "Connect through Harness Platform"** (required for Harness Cloud). Its token must be stored as a Harness Secret.
- Harness Cloud build credits (default on Harness-hosted runners). No delegate required for this tidbit.

## Connector reference cheat sheet

| Connector URL type | `connectorRef` prefix | `repoName` required? | Example |
|--------------------|-----------------------|----------------------|---------|
| Account | `account.<id>` | **Yes** — connector points at the host root | `account.github_public` + `repoName: your-org/your-app` |
| Org | `org.<id>` | **Yes** | `org.github` + `repoName: your-org/your-app` |
| Project | `<id>` (bare) | Yes for Account/Org URL type | `github` + `repoName: your-org/your-app` |
| Repository | any of the above | No — connector already targets one repo | `github_myapp` |

The credential is always a **Harness Secret referenced by the connector** — it is never named in the pipeline YAML.

## Steps

1. Fork / clone this repo.
2. Configure `.env` (optional, for reference): `cp .env.example .env` and fill your connector id, repo name, and org/project. The `.env` is git-ignored and not consumed by the pipeline — it only documents your swap points.
3. **Create a code repo connector** (skip if you already have one):
   - In Harness: **Project Settings → Connectors → New Connector → GitHub** (or GitLab/Bitbucket/Git).
   - **URL Type:** `Account` or `Repository`.
   - **Connectivity Mode:** **Connect through Harness Platform** (required for Harness Cloud).
   - **Authentication:** Username + Personal Access Token — store the token as a **Harness Secret** when prompted. Save and **Test** the connection.
4. **Import the pipeline:**
   - In Harness, go to your project → **Pipelines → Create a Pipeline → Import From Git**, or **Create** → switch to the YAML editor and paste `.harness/clone_repo_securely.yaml`.
   - Edit the `# REPLACE:` lines: set `connectorRef` to your connector id, and `projectIdentifier` / `orgIdentifier` to yours.
5. **Run it:**
   - Click **Run**. Harness prompts for `repoName` (the `<+input>` value) and the build. Enter e.g. `harness-community/ci-tidbits-test-intelligence-intro`.
   - Set **Build Type: Git Branch** → **Branch: `main`**.
   - Click **Run Pipeline**. Notice it never asks you for a credential — the connector already has that covered.
6. **Expected success.** Open the **Prove the clone worked** step log. You should see:
   - `Cloned into: /harness` (the workspace)
   - a file listing of the cloned repo root
   - the latest commit from `git log -1 --oneline`
   - `git remote -v` with **no token in the URL**
   - The build finishes green. The credential was injected only for the clone — never persisted, never printed.

## Try it: clone a different repo without editing steps

- Re-run and enter a different `repoName` or branch — the clone target changes, the step does not.
- Point `connectorRef` at a private repo your connector's secret can read — same YAML, still no token on screen.
- Swap the `runtime` block for a Kubernetes infrastructure to run on your own delegates (see below).

## Run on your own infra (optional)

To use your own Kubernetes or VM delegates instead of Harness Cloud, replace the `runtime` block in the stage `spec` with:

```yaml
infrastructure:
  type: KubernetesDirect
  spec:
    connectorRef: <your_k8s_connector>   # REPLACE
    namespace: <your_namespace>          # REPLACE
```

## Troubleshooting

- **`repoName ... is required` at runtime.** Account/Org URL-type connectors point at the Git host root, not one repo, so `repoName` is mandatory. Supply it in the codebase block or at run time.
- **`Authentication failed` / `Bad credentials`.** The connector's secret token is wrong or expired. Re-create the PAT, update the Harness Secret the connector references, then **Test** the connector.
- **Clone step never runs.** `cloneCodebase` is `false`. Set `cloneCodebase: true` on the stage `spec` — that line is what triggers the implicit clone.
- **`Connector not connected through Harness Platform` on Harness Cloud.** The connector's Connectivity Mode is set to a delegate. Edit the connector → set **Connect through Harness Platform**.
- **A token appears in logs.** Never `echo` the credential or embed it in a URL. The connector injects it for the clone only; keep it out of your `command`.

## What this tidbit intentionally does NOT cover

Multi-codebase clones, the standalone **Git Clone step** (mid-pipeline clone), subdirectory/LFS clones, `.netrc` manual auth, and building or testing the cloned code. Those are separate tidbits. This one is only the secure clone.

## Reference

- Configure codebase: https://developer.harness.io/docs/continuous-integration/use-ci/codebase-configuration/create-and-configure-a-codebase
- Connect to a Git repo (connector URL type & `repoName`): https://developer.harness.io/docs/platform/connectors/code-repositories/connect-to-code-repo
- Run step settings: https://developer.harness.io/docs/continuous-integration/use-ci/run-step-settings
