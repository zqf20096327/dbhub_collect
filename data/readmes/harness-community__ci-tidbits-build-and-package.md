# CI Tidbit — Build & Package

Install your app's dependencies and package it into a distributable artifact — a **Python wheel** — inside a Harness CI pipeline running on **Harness Cloud**. No delegate, no Kubernetes, no infrastructure to manage. This tidbit clones a repo, installs the build tooling, and runs `python -m build` to produce a `.whl` you can see in the logs. The same two-step pattern swaps cleanly to a Java JAR or a Node package.

## What this skill accomplishes

Build & Package is the atomic CI skill of turning source code into a shippable artifact. Harness clones your repo onto a Harness Cloud VM, you install whatever your build needs, then you run your ecosystem's package command. The result — here, `tidbit_calc-0.1.0-py3-none-any.whl` — is a real, installable artifact produced from the committed `sample-app/`, not a fabricated inline script. (Testing and publishing the artifact are separate tidbits.)

## What you will build

A single CI stage on Harness Cloud with two Run steps:

1. **Install Dependencies** — upgrades `pip` and installs the PEP 517 `build` frontend.
2. **Build Package** — `cd sample-app` and runs `python -m build`, producing `sample-app/dist/tidbit_calc-0.1.0-py3-none-any.whl` (plus the `.tar.gz` sdist), then lists `dist/`.

No delegate, no Kubernetes — Python is preinstalled on the Harness Cloud Linux image.

## Prerequisites

- A Harness account with a Project (free tier is fine).
- Permission to create and run pipelines.
- A **GitHub code connector** (this pipeline uses `account.github_public`, an Account-level connector on the public GitHub URL). Any healthy GitHub connector works; Connectivity Mode "Connect through Harness Platform" is required for Harness Cloud.
- Harness Cloud build credits (included on the free tier). No delegate needed.

## Language swap cheat sheet

| Ecosystem | Install step | Package command | Artifact lands in |
|-----------|--------------|-----------------|-------------------|
| **Python wheel** | `pip install build` | `python -m build` | `dist/*.whl` |
| **Java JAR** | (Maven/Gradle preinstalled) | `mvn -B package` or `./gradlew build` | `target/*.jar` |
| **Node package** | `npm ci` | `npm pack` | `*.tgz` |

Point the Build Package step's `cd` at the directory that holds that ecosystem's build file (`pyproject.toml`, `pom.xml`, `package.json`).

## Steps

1. Fork / clone this repo so the pipeline can clone *your* copy and build *your* `sample-app/`.
2. Configure `.env` (optional, for reference): `cp .env.example .env` and fill your connector ref, repo, and org/project. The `.env` is git-ignored and not consumed by the pipeline — it only documents your swap points.
3. **Create / confirm a GitHub connector** in Harness: **Project Settings → Connectors → New Connector → GitHub**. Note its reference (e.g. `account.github_public`), then run **Test Connection**.
4. **Import the pipeline:**
   - In your project → **Pipelines → Create a Pipeline → Import From Git**, or **Create → YAML** and paste `.harness/build_and_package.yaml`.
   - Edit every `# REPLACE:` line: `projectIdentifier` / `orgIdentifier`, `connectorRef`, `repoName` (your fork), and `branch`.
5. **Run it.** Click **Run**; provide `branch: main` if prompted.
6. **Expected success.** The build reaches **Success** in well under a minute. In the **Build Package** step log you'll see:
   ```
   Successfully built tidbit_calc-0.1.0.tar.gz and tidbit_calc-0.1.0-py3-none-any.whl
   ----- Built artifacts -----
   tidbit_calc-0.1.0-py3-none-any.whl
   tidbit_calc-0.1.0.tar.gz
   ```

## Try it locally first (optional sanity check)

```bash
cd sample-app
pip install build
python -m build
ls dist/   # tidbit_calc-0.1.0-py3-none-any.whl
```

## Try it: swap the language without changing the shape

- Replace the Build Package command per the cheat sheet above (`mvn -B package`, `npm pack`, …) and point `cd` at that build file's directory.
- Add a real dependency to `sample-app/pyproject.toml`, replace the install step with `pip install -r requirements.txt`, and watch it install before the build.

## Troubleshooting

- **`No module named build` in Build Package.** Step 1 (`pip install build`) didn't run or was deleted. Ensure it runs before Step 2.
- **`ERROR Multiple top-level packages discovered` / no `dist/` produced.** `python -m build` ran in the wrong directory, or your package layout doesn't match. `cd` into the dir holding `pyproject.toml`. This repo uses a `src/` layout declared via `[tool.setuptools.packages.find] where = ["src"]`.
- **Clone fails with `connector not found` / auth error.** `connectorRef` doesn't exist in scope or can't reach the repo. Use the exact identifier (account-scoped refs are prefixed `account.`), run **Test Connection**, and confirm `repoName` matches your fork.

## What this tidbit intentionally does NOT cover

Running tests, publishing/uploading the artifact to a registry, Docker image builds, and caching build dependencies. Those are separate tidbits. This one is only install + package.

## Reference

- CI Run step settings: https://developer.harness.io/docs/continuous-integration/use-ci/run-step-settings
- Configure codebase (clone): https://developer.harness.io/docs/continuous-integration/use-ci/codebase-configuration/create-and-configure-a-codebase
- Harness Cloud build infrastructure: https://developer.harness.io/docs/continuous-integration/use-ci/set-up-build-infrastructure/use-harness-cloud-build-infrastructure
