# CI | Tidbits | Looping Strategy

> **Bite-sized how-to** | ~20 min setup

---

## What is the Matrix Looping Strategy?

In a monorepo with multiple services written in different languages, the naive approach is to maintain a separate pipeline per service. Every time you add a service, you write a new pipeline. Every time you change the build process, you update every pipeline.

The Harness **Matrix Looping Strategy** solves this by letting a single stage definition fan out into multiple parallel executions at runtime — one per item in the matrix. You define the stage once, declare a list of values, and Harness creates N copies running in parallel, each with its own matrix variable injected.

**How it works:**

1. You define a `strategy.matrix` block on a stage with a list of values — in this case, service names.
2. Harness fans the stage out into one execution per value, all running in parallel (controlled by `maxConcurrency`).
3. Each execution gets `<+matrix.service>` populated with its value — `python-app`, `java-app`, or `node-app`.
4. Within the stage, `when:` conditions on each step ensure only the relevant build step runs for that iteration.
5. Shared steps — like `BuildAndPushDockerRegistry` — use `<+matrix.service>` dynamically, so one step definition handles all three images.

---

## What does this Tidbit demonstrate?

A monorepo with three services — Python, Java, and Node.js — built, tested, and pushed to Docker Hub in a single pipeline run using a Matrix Strategy:

1. **Matrix fans out** — one stage definition spawns three parallel builds.
2. **Conditional steps** — each iteration only runs the step matching its tech stack.
3. **Shared Docker push** — one `BuildAndPushDockerRegistry` step pushes the correct image for each service using `<+matrix.service>`.

---

## Project Structure

```
ci-tidbits-looping-strategy/
├── .harness/
│   └── pipeline.yaml                    — CI pipeline with Matrix Strategy
├── services/
│   ├── python-app/
│   │   ├── app.py                       — Python math utility
│   │   ├── test_app.py                  — pytest tests
│   │   ├── requirements.txt             — pytest dependency
│   │   └── Dockerfile
│   ├── java-app/
│   │   ├── pom.xml                      — Maven build with JUnit 5
│   │   ├── src/main/java/com/harness/App.java
│   │   ├── src/test/java/com/harness/AppTest.java
│   │   └── Dockerfile
│   └── node-app/
│       ├── index.js                     — Node.js math utility
│       ├── index.test.js                — Jest tests
│       ├── package.json                 — Jest dependency
│       └── Dockerfile
└── README.md
```

---

## Prerequisites

Before you start, make sure you have:

- A Harness project with CI enabled
- A Kubernetes cluster with a Harness Kubernetes connector configured
- A Harness delegate running inside the cluster
- A GitHub connector pointing to this repository
- A Docker Hub connector with push credentials

---

## Step 1 — Fork or Clone the Repository

Fork or clone this repository to your own GitHub account. You will point the Harness pipeline at your fork.

---

## Step 2 — Configure the Pipeline Placeholders

Open `.harness/pipeline.yaml` and replace the following placeholders:

| Placeholder | Replace with |
|---|---|
| `YOUR_PROJECT_ID` | Your Harness project identifier |
| `YOUR_ORG_ID` | Your Harness org identifier |
| `YOUR_GITHUB_CONNECTOR` | Your GitHub connector identifier |
| `YOUR_K8S_CONNECTOR` | Your Kubernetes connector identifier |
| `YOUR_DOCKERHUB_CONNECTOR` | Your Docker Hub connector identifier |
| `YOUR_DOCKERHUB_USERNAME` | Your Docker Hub username |

Commit and push the changes.

---

## Step 3 — Import the Pipeline

1. Go to **Pipelines → Import From Git**
2. Select your GitHub connector, point it to this repository, and select `.harness/pipeline.yaml`
3. Hit **Import**

---

## Step 4 — Run the Pipeline

1. Click **Run Pipeline**
2. Set the branch to `main` (or your working branch)
3. Click **Run**

Watch the **Build** stage fan out into three parallel executions — one per service. Each execution shows the service name in its stage label: `Build_python-app_0`, `Build_java-app_1`, `Build_node-app_2`.

Inside each execution:
- Only the matching **Build and Test** step runs (the other two are skipped via `when:` conditions)
- The **Build and Push Docker Image** step runs for all three, pushing to `YOUR_DOCKERHUB_USERNAME/ci-<service>:latest`

---

## How the Matrix Strategy Works — Pipeline Breakdown

The key section in the pipeline YAML is the `strategy` block at the bottom of the stage:

```yaml
strategy:
  matrix:
    service:
      - python-app
      - java-app
      - node-app
    maxConcurrency: 3
```

- `matrix.service` — the list of values to iterate over. Harness creates one stage execution per value.
- `maxConcurrency: 3` — all three run simultaneously. Set to `1` to run sequentially, or `2` to limit parallelism.
- `<+matrix.service>` — the variable injected into each execution, available in step commands, image names, Dockerfile paths, and Docker repo names.

The `when:` condition on each build step controls which step runs per iteration:

```yaml
when:
  stageStatus: Success
  condition: <+matrix.service> == "python-app"
```

The `BuildAndPushDockerRegistry` step has no `when:` condition — it runs for every iteration, using `<+matrix.service>` to dynamically resolve the image path and repository:

```yaml
repo: YOUR_DOCKERHUB_USERNAME/ci-<+matrix.service>
dockerfile: services/<+matrix.service>/Dockerfile
context: services/<+matrix.service>
```

---

## Common Issues & Tips

**Stage fan-out not appearing**
- Confirm the `strategy.matrix` block is indented at the stage level, not inside `spec` or `execution`.

**All three build steps run in every iteration**
- Check that each `Run` step has a `when:` block with the correct `condition` expression. The condition uses JEXL syntax — `==` not `=`.

**Docker push fails**
- Confirm `YOUR_DOCKERHUB_CONNECTOR` is set to your Docker Hub connector identifier in the pipeline YAML.
- Confirm the Docker Hub connector has push credentials configured.

**`maxConcurrency` not respected**
- `maxConcurrency` is set inside the `matrix` block, not alongside it. Verify the indentation in your YAML.

---

## Resources

- [Matrix Looping Strategy](https://developer.harness.io/docs/platform/pipelines/looping-strategies/looping-strategies-matrix-repeat-and-parallelism/)
- [Conditional Execution — When Conditions](https://developer.harness.io/docs/platform/pipelines/step-skip-condition-settings/)
- [Build and Push to Docker Registry](https://developer.harness.io/docs/continuous-integration/use-ci/build-and-upload-artifacts/build-and-push/build-and-push-to-docker-registry/)
