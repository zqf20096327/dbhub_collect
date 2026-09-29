# CI Tidbit — Custom Plugins in Harness CI

A **plugin** is a Docker container with an `ENTRYPOINT`. You can write the entrypoint in any language. Harness runs it via the native `Plugin` step and injects your `settings:` as `PLUGIN_*` env vars inside the container.

```
settings.operation  →  PLUGIN_OPERATION   (inside the container)
settings.values     →  PLUGIN_VALUES
```

Results come back the same way, in reverse: the plugin appends `KEY=value` lines to the file at `$DRONE_OUTPUT`, and Harness turns them into **output variables** for later steps.

Those two rules are the entire plugin contract.

This tidbit builds a **Python calculator plugin**, pushes it with `BuildAndPushDockerRegistry`, then **reuses that image** in later `Plugin` steps.

---

## Plugin step vs Run step

| | `Run` step | `Plugin` step |
|---|---|---|
| What it does | Runs a shell script inline | Runs a container's `ENTRYPOINT` |
| How you pass inputs | Env vars / inline shell | `settings:` → `PLUGIN_*` env vars |
| How you get outputs | `outputVariables:` on the step | Plugin writes to `$DRONE_OUTPUT` |
| Reuse | Copy/paste per pipeline | One image, any pipeline or team |
| Best for | One-off commands | Repeatable tasks (clone, publish, scan, calculate) |

**Rule of thumb:** if you're copying the same script into multiple pipelines, make it a plugin.

---

## What this repo demos

Pipeline `.harness/pipeline.yaml` runs 4 steps on **Harness Cloud** (no delegate needed):

| Step | Type | What it shows |
|------|------|---------------|
| 1 — Build and Push Custom Plugin | `BuildAndPushDockerRegistry` | Build `sample-plugin/Dockerfile` and push it — natively, no `docker build` in a shell |
| 2 — Calculator Plugin – Add | `Plugin` | Pull the just-pushed image and run `add` on `2,3,5` |
| 3 — Calculator Plugin – Multiply | `Plugin` | Reuse the **same** image with a different `operation` |
| 4 — Use Plugin Output Variables | `Run` | Read `RESULT` and `MESSAGE` from both plugin steps via expressions |

**The core skill is step 1 + the steps after it** — build once, then use the plugin in subsequent pipeline steps.

---

## The custom plugin (`sample-plugin/`)

Two files:

- **`Dockerfile`** — `python:3.12-alpine`, copies `entrypoint.py`, sets it as `ENTRYPOINT`.
- **`entrypoint.py`** — reads `PLUGIN_OPERATION` and `PLUGIN_VALUES`, prints a message, exports output variables.

### Inputs (`settings:` → `PLUGIN_*`)

| `settings:` key | Env var in container | What it does |
|---|---|---|
| `operation` | `PLUGIN_OPERATION` | `add`, `subtract`, `multiply`, or `divide` |
| `values` | `PLUGIN_VALUES` | Comma-separated numbers, e.g. `2,3,5` |

### Outputs (`$DRONE_OUTPUT` → output variables)

At runtime Harness sets `$DRONE_OUTPUT` to a temp file such as `/tmp/engine/xyz-output.env`. The plugin appends `KEY=value` lines to it, and Harness captures each key as an output variable on the step (visible on the step's **Output** tab).

| Output variable | Example value |
|---|---|
| `OPERATION` | `add` |
| `VALUES` | `2 3 5` |
| `RESULT` | `10` |
| `MESSAGE` | `I am going to add for the following numbers: 2 3 5 and final value is 10` |

Reference them in a later step in the same stage:

```yaml
echo <+steps.calculator_plugin_add.output.outputVariables.RESULT>
echo <+execution.steps.calculator_plugin_add.output.outputVariables.MESSAGE>
```

Or from another stage:

```yaml
<+stages.STAGE_ID.spec.execution.steps.calculator_plugin_add.output.outputVariables.RESULT>
```

> Output variable values in this plugin are space-separated, not comma-separated. Special characters such as `,` `.` `/` in output variable keys or values may not work on self-managed VM build infrastructures.

**Test it locally** — this is identical to how Harness runs it, with `DRONE_OUTPUT` faked:

```bash
cd sample-plugin
docker build -t my/ci-tidbit-custom-plugin:1.0 .
docker run --rm \
  -e PLUGIN_OPERATION=add \
  -e PLUGIN_VALUES="2,3,5" \
  -e DRONE_OUTPUT=/tmp/output.env \
  my/ci-tidbit-custom-plugin:1.0
```

Or without Docker:

```bash
PLUGIN_OPERATION=add PLUGIN_VALUES="2,3,5" DRONE_OUTPUT=/tmp/output.env \
  python3 sample-plugin/entrypoint.py && cat /tmp/output.env
```

---

## Prerequisites

- A Harness account with a CI project (Harness Cloud works out of the box — no delegate).
- A **repo connector** pointing at your fork of this repo (so `sample-plugin/` is available to clone).
  - Harness Code repo → `repoName:` only (no `connectorRef:`).
  - GitHub/GitLab → add a connector and set `connectorRef:`.
- A **Docker registry connector** (`account.Docker`) with push access — used by Step 1 to push the plugin image and by later Plugin steps to pull it back.

---

## Setup

1. **Fork this repo** so it includes `sample-plugin/`.
2. **Update every `# REPLACE:` line** in `.harness/pipeline.yaml`:
   - `projectIdentifier` / `orgIdentifier`
   - `repoName` → your fork
   - `repo:` in Step 1 → `<your-docker-user>/ci-tidbit-custom-plugin`
   - `image:` in Steps 2 and 3 → same image name
3. **Import the pipeline**: Harness → Pipelines → *Import From Git* (or paste the YAML into Pipeline Studio).
4. **Run** → pick **Git Branch → `main`**.

**Expected output:**
- Step 1 log: Dockerfile built, image pushed with digest.
- Step 2 log: `I am going to add for the following numbers: 2 3 5 and final value is 10`, plus the variables written to `$DRONE_OUTPUT`.
- Step 3 log: same for multiply, final value `30`.
- Step 2 and 3 **Output** tabs: `OPERATION`, `VALUES`, `RESULT`, `MESSAGE`.
- Step 4 log: both messages echoed from output variables.

---

## Reuse your plugin in any pipeline

Once pushed, drop these steps into any pipeline:

```yaml
# Build and push (do this once per release, or every run as in this tidbit)
- step:
    type: BuildAndPushDockerRegistry
    name: Build and Push Custom Plugin
    identifier: build_push_custom_plugin
    spec:
      connectorRef: account.Docker
      repo: <your-docker-user>/ci-tidbit-custom-plugin
      tags:
        - <+pipeline.sequenceId>
      dockerfile: sample-plugin/Dockerfile
      context: sample-plugin

# Run it as a native Plugin step
- step:
    type: Plugin
    name: Calculator Plugin
    identifier: calculator_plugin
    spec:
      connectorRef: account.Docker
      image: <your-docker-user>/ci-tidbit-custom-plugin:<+pipeline.sequenceId>
      settings:
        operation: add
        values: "2,3,5"

# Consume its output variables
- step:
    type: Run
    name: Use Result
    identifier: use_result
    spec:
      shell: Sh
      command: echo <+steps.calculator_plugin.output.outputVariables.RESULT>
```

To share your plugin publicly, submit a PR to the [Drone Plugin Index](https://github.com/drone/drone-plugin-index).

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Step 1 fails: `sample-plugin/Dockerfile` not found | Your codebase isn't pointing at this fork. The clone must contain `sample-plugin/`. |
| Step 1 fails to push | Your Docker connector doesn't have push access, or `repo:` isn't your namespace. |
| Later Plugin steps can't pull the image | The image tag must match what Step 1 pushed (all use `<+pipeline.sequenceId>`). Private images need the fully-qualified name. |
| Settings don't reach Python | Write `operation` in `settings:` — not `PLUGIN_OPERATION`. Harness adds the prefix. |
| Output variables are empty | Confirm the plugin appended to `$DRONE_OUTPUT` (the log prints the path). Not all build infrastructures support it. |
| Expression doesn't resolve | The step ID in `<+steps.STEP_ID.output.outputVariables.RESULT>` must match the Plugin step's `identifier`. |
| `unsupported operation` | Use `add`, `subtract`, `multiply`, or `divide`. |

---

## Docs

- [Write custom plugins](https://developer.harness.io/docs/continuous-integration/use-ci/use-drone-plugins/custom_plugins/)
- [Plugin step settings — Output variables](https://developer.harness.io/docs/continuous-integration/use-ci/use-drone-plugins/plugin-step-settings-reference#output-variables)
- [CI environment variables reference (`DRONE_OUTPUT`)](https://developer.harness.io/docs/continuous-integration/troubleshoot-ci/ci-env-var)
- [Build and Push to Docker Registry](https://developer.harness.io/docs/continuous-integration/use-ci/build-and-upload-artifacts/build-and-push/build-and-push-to-docker-registry)
