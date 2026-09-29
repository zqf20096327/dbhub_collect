# CI | Tidbits | UI & YAML Editor

> **Bite-sized how-to** | ~5 min setup

---

## What are the UI and YAML editors?

Every Harness pipeline is one object with two equivalent views:

- **Visual** — a click-through diagram of stages and steps, with form-driven config.
- **YAML** — the same pipeline as a text file you can edit, diff, and commit to Git.

Both views read and write the same underlying pipeline definition. A change in Visual shows up in YAML on save; a change in YAML shows up in Visual on save. This tidbit walks you through building the *same* CI pipeline both ways, then proves the two are one object with a round-trip edit.

The sample pipeline is standard-shaped — three stages, two Run steps each, every step an `echo` — so you can focus on the editor mechanics, not the workload:

| Stage | Steps |
|---|---|
| **Build** | `Compile`, `Package` |
| **Test** | `Unit tests`, `Integration tests` |
| **Publish** | `Push artifact`, `Notify` |

Two pipeline variables (`build_version`, `notify_channel`) are referenced across stages, so you can watch interpolation work end-to-end and use them for the round-trip demo.

---

## Prerequisites

Before you start, make sure you have:

- A Harness account with a **Project** (note its org + project identifiers).
- Harness Cloud build credits (default on Harness-hosted runners). **No delegate, no Git connector, no codebase required** — the pipeline runs entirely on echo commands.

> **Note:** No repo fork needed. You can either paste the YAML from this repo into the Harness pipeline studio, or build the pipeline from scratch in Visual mode using the walkthrough below.

---

## Step 1 — Create an empty pipeline

In your Harness project:

1. Go to **Pipelines → Create a Pipeline**.
2. Name it `UI and YAML Editor Demo`.
3. Choose **Inline** and click **Start**.

You land in the pipeline studio with an empty Visual canvas. The **Visual / YAML** toggle sits at the top-right of the editor — you will use it a lot.

Pick one of the two paths below. Both produce the same pipeline.

---

## Step 2 — Build the pipeline

### Path A — Click through in Visual mode

Use this path if you prefer clicking to typing, or you want to see what fields Harness surfaces for each step type.

**Add the Build stage:**

1. On the empty canvas, click **Add Stage → Build**.
2. Stage Name: `Build`. Leave **Clone Codebase** off and Click **Set Up Stage**.
3. Under **Infrastructure**, choose **Cloud**, leave all other settings as default, and click **Continue**.
4. **Execution → Add Step → Run**:
   - Name: `Compile`
   - Command:
     ```sh
     echo "Compiling source for version <+pipeline.variables.build_version>..."
     echo "Build complete."
     ```
5. **Add Step → Run** again:
   - Name: `Package`
   - Command:
     ```sh
     echo "Packaging artifact: app-<+pipeline.variables.build_version>.tar.gz"
     echo "Artifact ready."
     ```

**Add the Test stage:**

6. Back on the pipeline canvas, click **+ Add Stage → Build**. Name it `Test`. Leave **Clone Codebase** off.
7. Choose **Propagate from an existing stage** and select **Stage [Build]**.
8. Add two Run steps:
   - `Unit tests` → `echo "Running unit tests..." && echo "142 passed, 0 failed."`
   - `Integration tests` → `echo "Running integration tests..." && echo "38 passed, 0 failed."`

**Add the Publish stage:**

9. Click **+ Add Stage → Build**. Name it `Publish`. Leave **Clone Codebase** off.
10. Choose **Propagate from an existing stage** and select **Stage [Test]**.
11. Add two Run steps:
   - `Push artifact` → `echo "Pushing app-<+pipeline.variables.build_version>.tar.gz to registry..." && echo "Push complete."`
   - `Notify` → `echo "Sending notification to <+pipeline.variables.notify_channel>..." && echo "Team notified."`

**Add the pipeline variables:**

12. Open the **Variables** panel (right side of the studio).
13. Add `build_version` (String, default `1.0.0`) and `notify_channel` (String, default `#ci-alerts`).

Save.

### Path B — Paste the YAML

Use this path if you already know what the pipeline looks like, or want to skip straight to the round-trip demo.

1. In the empty studio, toggle to **YAML** (top-right of the editor).
2. Paste the contents of [`pipeline.yaml`](./pipeline.yaml), replacing the stub.
3. Edit the `<YOUR_PROJECT_ID>` and `<YOUR_ORG_ID>` lines. (Harness may fill these in automatically on save — either works.)
4. Save.

Toggle back to Visual — you get the same pipeline Path A produced, just delivered as text.

---

## Step 3 — Run the pipeline (expect a GREEN build)

Click **Run** — from either the Visual or the YAML view; the button lives in both. Harness prompts for pipeline variable inputs — leave the defaults or override them — then click **Run Pipeline**.

Six echo commands run across three stages on Harness Cloud. Expected: green all the way through in under a minute.

Expand any step's log. The variables interpolate as expected — the `Notify` step, for example, prints `Sending notification to #ci-alerts...`.

**Green is the correct outcome.** It proves the pipeline you built (in either view) is well-formed and executable.

---

## Step 4 — Round-trip: edit in one view, watch it appear in the other

This is the point of the tidbit. Prove to yourself that Visual and YAML are the same object.

**UI → YAML.** In Visual, open the **Test** stage and add a third Run step called `Smoke tests` with `echo "smoke tests passed"`. Save. Toggle to YAML and scroll to the Test stage — the step is in the file.

**YAML → UI.** In YAML, change `notify_channel`'s default value from `#ci-alerts` to `#your-team`. Save. Toggle back to Visual → Variables panel → the new value is there.

**Re-run.** The `Notify` step's log now shows the new channel. One pipeline, two editors, one truth.

---

## When to reach for which

| Use Visual when… | Use YAML when… |
|---|---|
| You're new to a pipeline and want to see its shape. | You're editing many steps or stages at once. |
| You want form-driven config with field validation. | You want the change to go through code review. |
| You're onboarding a teammate. | You're storing the pipeline in Git (pipeline-as-code). |

Most day-to-day pipeline work involves *both* — quick edits in Visual, bulk changes in YAML.

---

## Pipeline YAML reference

The full pipeline lives at [`pipeline.yaml`](./pipeline.yaml). Key shape:

```yaml
pipeline:
  name: UI and YAML Editor Demo
  stages:
    - stage:   # Build
        type: CI
        spec:
          cloneCodebase: false
          runtime: { type: Cloud, spec: {} }
          execution:
            steps:
              - step: { name: Compile, type: Run, spec: { command: "echo ..." } }
              - step: { name: Package, type: Run, spec: { command: "echo ..." } }
    - stage: { name: Test,    ... }   # Unit tests + Integration tests
    - stage: { name: Publish, ... }   # Push artifact + Notify
  variables:
    - { name: build_version,  type: String, value: "1.0.0"    }
    - { name: notify_channel, type: String, value: "#ci-alerts" }
```

Every step is a `Run` step with `shell: Sh` on Harness Cloud runtime. No connectors, no codebase, no secrets — the whole thing runs on echoes.

---

## Common Issues & Tips

**The Visual toggle is greyed out.** You have unsaved YAML with a syntax error. Fix it (Harness inlines the error) or click **Discard** to revert to last save.

**Pipeline saves but Run does nothing.** Check that your project has Harness Cloud build minutes available. **Project Settings → Resources → Build Credits** should show a non-zero balance.

**Variable references show `<+pipeline.variables.foo>` in logs instead of the value.** The variable is defined but the reference has a typo. Copy the expression directly from the Variables panel — Harness shows the exact string next to each variable.

**Visual and YAML seem out of sync.** You have unsaved changes in one editor. Save on that side; the two views resync on the next toggle.

**I edited YAML and my Visual layout jumped around.** Harness reserializes on save — step order in YAML is authoritative, but formatting (indentation, key order inside a step) is normalized. That's expected.

---

## What's next?

- **Store the pipeline in Git.** Move `pipeline.yaml` into a `.harness/` folder in a real repo, connect the repo via a Git connector, and set the pipeline to **Remote** storage. Every future YAML edit becomes a PR.
- **Add real work to the echoes.** Swap `Compile` for `mvn package` or `npm run build`, `Unit tests` for `pytest`, and turn on `cloneCodebase: true` with a codebase connector. Same pipeline shape, real workload.
- **Template a stage.** Right-click a stage in Visual → **Save as Template**. Reuse it across pipelines. Templates round-trip between Visual and YAML too.

---

## Resources

- [Harness YAML overview](https://developer.harness.io/docs/platform/pipelines/harness-yaml-quickstart)
- [Run step settings](https://developer.harness.io/docs/continuous-integration/use-ci/run-step-settings/)
- [Pipeline variables & expressions](https://developer.harness.io/docs/platform/variables-and-expressions/harness-variables/)
- [Harness Cloud build infrastructure](https://developer.harness.io/docs/continuous-integration/use-ci/set-up-build-infrastructure/use-harness-cloud-build-infrastructure/)
