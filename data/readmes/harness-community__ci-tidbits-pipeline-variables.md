# CI Tidbit — Pipeline Variables

Define **pipeline variables** in a Harness CI pipeline and reference them inside a Run step with the expression `<+pipeline.variables.NAME>`. This tidbit shows a fixed-value variable, a required runtime input (`<+input>`), and a bonus stage variable — all echoed live to prove they resolve.

## What this skill accomplishes

Variables let you templatize a pipeline once and supply values per run (branch, environment, region, flags) instead of hardcoding them in every step. You declare them under `pipeline.variables` and reference them anywhere an expression is accepted using `<+pipeline.variables.NAME>`.

## What you will build

A single CI stage on Harness Cloud with one Run step that echoes:

- `greeting` — a **fixed-value** pipeline variable (has a default)
- `environment_name` — a **required runtime input** (`<+input>`, prompted on Run)
- `region` — a **stage variable** (bonus), referenced with `<+stage.variables.region>`

No git clone, no app, no delegate — fully self-contained.

## Prerequisites

- A Harness account with a **Project** (note its org + project identifiers).
- Permission to create and run pipelines.
- Harness Cloud build credits (default on Harness-hosted runners). No connector or delegate required for this tidbit.

## Variable reference cheat sheet

| Scope | Define under | Reference (same scope) | Reference (cross-scope) |
|-------|--------------|------------------------|--------------------------|
| Pipeline | `pipeline.variables` | `<+pipeline.variables.NAME>` | `<+pipeline.variables.NAME>` |
| Stage | `stage.variables` | `<+stage.variables.NAME>` | `<+pipeline.stages.STAGE_ID.variables.NAME>` |
| Project | Project Setup → Variables | `<+variable.NAME>` | — |
| Account | Account Resources → Variables | `<+variable.account.NAME>` | — |

Value types: a **fixed value**, another **expression**, or `<+input>` for a runtime input. Only pipeline/stage (entity-level) variables support `<+input>`; account/org/project variables are fixed-value only.

## Steps

1. **Fork / clone this repo.**
2. **Configure `.env`** (optional, for reference): `cp .env.example .env` and fill your org/project. The `.env` is git-ignored and not consumed by the pipeline — it only documents your swap points.
3. **Import the pipeline:**
   - In Harness, go to your project → **Pipelines** → **Create a Pipeline** → **Import From Git** *or* **Create** → switch to the **YAML** editor and paste `.harness/pipeline_variables.yaml`.
   - Edit the `# REPLACE:` lines: set `projectIdentifier` and `orgIdentifier` to yours.
4. **Run it:**
   - Click **Run**. Harness prompts for `environment_name` (the `<+input>` variable). Enter e.g. `staging`.
   - `greeting` and `region` already have defaults, so they are not prompted.
   - Click **Run Pipeline**.
5. **Expected success.** Open the **Echo Pipeline Variables** step log. You should see:
   ```
   Pipeline variable greeting: Hello from Harness University
   Pipeline variable environment_name: staging
   Stage variable region: us-east-1
   ```
   The build finishes **green**. Because Harness resolves expressions before the script runs, a green build proves every `<+...>` reference resolved correctly.

## Try it: change values without editing steps

- Re-run and enter a different `environment_name` — the echo changes, the step does not.
- Edit the `greeting` default in YAML, or override it at run time by changing its value type to runtime input.
- Add a third pipeline variable and echo it — same `<+pipeline.variables.NAME>` pattern.

## Troubleshooting

- **`Run` prompts for `environment_name` and you leave it blank → validation error.** It is `required: true` with `value: <+input>`. Supply a value, or give it a default to make it optional.
- **Expression printed literally (`<+pipeline.variables.greeting>` shown verbatim).** The variable name in the expression must exactly match a declared variable `name`, and the expression must live in a field that accepts expressions (the Run `command` does). Check indentation: `variables` must be aligned under `pipeline` (pipeline vars) or under `stage.spec` (stage vars).
- **`Stage variable region` is empty.** Stage variables must be declared in the stage you reference them from when using `<+stage.variables.NAME>`. From another stage use `<+pipeline.stages.echo_variables.variables.region>`.
- **Hyphens/periods in a name.** Avoid them. If unavoidable, use `<+pipeline.variables.get("my-var")>`.

## Reference

- Define variables: https://developer.harness.io/docs/platform/variables-and-expressions/add-a-variable
- Reference variables: https://developer.harness.io/docs/platform/variables-and-expressions/add-a-variable/#reference-variables
- Run step settings: https://developer.harness.io/docs/continuous-integration/use-ci/run-step-settings
