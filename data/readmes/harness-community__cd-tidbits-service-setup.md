# CD Tidbit — Harness Service Setup (Kubernetes) with Docker Artifact

**Create a reusable Harness CD Service** that bundles a Docker container image with Kubernetes manifests. A Service answers *"what are we deploying?"* — it's the definition you create once and reuse in every deployment pipeline.

In this tidbit, you'll define a Service for a Kubernetes deployment that pulls the public `nginx:stable` image from Docker Hub and applies a K8s manifest from Git. No environment setup, no pipeline configuration required — just the service definition itself.

## What you'll learn

- **What a Service is:** A versioned, reusable definition that answers "what are we deploying?"
- **What it bundles:** An artifact source (where your image comes from) + a manifest (what K8s objects to deploy).
- **How to reference artifacts:** Use `<+artifacts.primary.image>` in your manifest values to inject the resolved image at deploy time.
- **Two ways to define it:** Via the Harness UI (visual, easy for first-timers) or YAML (scriptable, repeatable).

## Service Architecture (Visual)

```
┌────────────────────────────────────────────────────────────────────┐
│                    HARNESS SERVICE (nginx_service)                 │
│                        [Kubernetes]                                │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────────────┐        ┌──────────────────────┐         │
│  │   ARTIFACT SOURCE    │        │   KUBERNETES         │         │
│  │                      │        │   MANIFEST           │         │
│  │  🐳 Docker Registry  │        │                      │         │
│  │  ─────────────────   │        │  📄 K8s Objects      │         │
│  │  Connector:          │        │  ─────────────────   │         │
│  │    account.Docker    │        │  Store: Git          │         │
│  │                      │        │  Repo: harnesscd-    │         │
│  │  Image Path:         │        │    example-apps      │         │
│  │    library/nginx     │        │  Branch: master      │         │
│  │                      │        │  Path: /default-k8s- │         │
│  │  Tag:                │        │    manifests/...     │         │
│  │    stable            │        │                      │         │
│  │                      │        │  Values File:        │         │
│  └──────────────────────┘        │    ng-values.yaml    │         │
│           │                      │                      │         │
│           │ Resolved Image:      │  image: <+artifacts  │         │
│           │ library/nginx:stable │    .primary.image>   │         │
│           │                      │                      │         │
│           └──────────────────────┼───────────────────┐  │         │
│                                  │                   │  │         │
│                                  └───────────────────┘  │         │
│                                   (Gets injected)       │         │
│                                                         │         │
└────────────────────────────────────────────────────────────────────┘

AT DEPLOY TIME:
The Docker artifact is resolved (library/nginx:stable) and injected
into the K8s manifest's values file, replacing <+artifacts.primary.image>.
```

## Concepts in 60 seconds

| Concept | What it is | Example |
|---|---|---|
| **Service** | *What* you deploy. A versioned, reusable definition of a workload. | `nginx_service` (Kubernetes) |
| **Artifact source** | Where the image/package comes from. `primary` is the main image; you can add `sidecars`. | `DockerRegistry` → `library/nginx:stable` |
| **Artifact expression** | Template that injects the resolved image into your manifest at deploy time. | `<+artifacts.primary.image>` |
| **Manifest** | The K8s objects (Deployment, Service, ConfigMap, etc.). Hosted in Git, Harness File Store, or Helm/Kustomize. | `K8sManifest` from Git repo |
| **Connector** | Stored credential that grants Harness access to an external system (Docker, Git, cloud provider, etc.). | `account.Docker`, `account.github_public` |
| **Deployment type** | The platform target shape. Determines which artifact and manifest types are available. | `Kubernetes`, `ECS`, `CloudFormation`, etc. |

## What is a Connector?

A **Connector** is a stored credential + configuration in Harness that grants access to an external system. Think of it as a reusable login: once you create it (e.g., "my Docker Hub credentials"), you reference it by name in services, pipelines, and other configs — no secrets hardcoded anywhere.

In this service:
- **Docker Registry connector** (`account.Docker`) — tells Harness how to authenticate with Docker Hub (or another Docker v2 registry) and pull images.
- **Git connector** (`account.github_public`) — tells Harness how to clone your Git repo and fetch manifests.

Connectors live in **Platform → Connectors** and are reusable across your entire Harness account.

## Artifact sources: Docker vs Artifactory

| | **Docker Registry** | **Artifactory (JFrog)** |
|---|---|---|
| `type` | `DockerRegistry` | `ArtifactoryRegistry` |
| Connector type | Docker Registry connector | Artifactory connector |
| Key fields | `connectorRef`, `imagePath`, `tag` | `connectorRef`, `repository`, `repositoryUrl`, `repositoryFormat: docker`, `artifactPath`, `tag` |
| Use when | Docker Hub, GHCR, ECR-as-docker, any Docker v2 registry | Images/packages stored in JFrog Artifactory |
| Example | `library/nginx:stable` | `docker-repo/myapp:v1.0.0` from Artifactory |

Both are shown in `.harness/service.yaml` (Docker is the active source; Artifactory
is in the commented alternative block).

## Prerequisites

To create this service, you'll need:

- **A Harness project** with the CD module enabled (where you'll create the service).
- **A Docker Registry connector** (credential to access Docker registries). This example uses `account.Docker` and pulls a public image (`library/nginx`), so you can use any valid Docker connector — even a dummy one with no credentials.
- **A Git connector** (credential to fetch manifests). This example uses `account.github_public` to pull manifests from the public `harness-community/harnesscd-example-apps` repo on GitHub.

> **Don't have connectors?** You can create them in Platform → Connectors:
> - [Docker Registry connector setup](https://developer.harness.io/docs/platform/connectors/cloud-providers/ref-cloud-providers/docker-registry-connector-settings-reference)
> - [Git connector setup](https://developer.harness.io/docs/category/code-repo-connectors)

## Files

| File | Purpose |
|---|---|
| `.harness/service.yaml` | The Service definition — Docker artifact source + Git K8s manifest. |
| `.harness/pipeline.yaml` | *Optional* minimal Deploy stage that references the service (needs an env + infra). |
| `.env.example` | Placeholder identifiers/connectors for optional API scripting. |

Every value you must change is flagged with a `# REPLACE:` comment.

## Steps

1. **Create a new service.**
   - Go to **Deployments** → **Services** → **New Service**.
   - Name it (e.g., `nginx_service`), then **Save**.

2. **Select the deployment type.**
   - In the **Service Definition** section, choose **Kubernetes** (this is the type of workload you'll deploy).

3. **Add an artifact source.**
   - **Artifacts** → **Add Artifact Source** → **Docker Registry** → **Continue**.
   - **Connector**: Select your Docker Registry connector (e.g., `account.Docker`).
   - **Artifact Source Name**: `nginx_public` (internal identifier).
   - **Image path**: `library/nginx` (public images use the `library/` prefix; private images use their full path).
   - **Tag**: `stable` (or `<+input>` to let users pick at deploy time).
   - **Submit**.

4. **Add the Kubernetes manifest.**
   - **Manifests** → **Add Manifest** → **K8s Manifest** → **Continue**.
   - **Connector**: Select your Git connector (e.g., `account.github_public`).
   - **Repository**: `harnesscd-example-apps` (or your repo name).
   - **Branch**: `master` (or your branch).
   - **Paths**: `/default-k8s-manifests/Manifests/Files/templates` (folder containing your K8s files).
   - **Values file**: `/default-k8s-manifests/Manifests/Files/ng-values.yaml` (the values file that will receive the artifact).
   - **Submit**.

5. **Wire the artifact into the manifest.**
   - Open the values file from your Git repo (or create one).
   - Add `image: <+artifacts.primary.image>` — this injects the Docker image you defined above into the manifest at deploy time.
   - Commit and push.

6. **Save the service.**
   - Review the service definition and click **Save**. It's now ready to use in any pipeline.

**Prefer YAML?** You can skip steps 1–6 and instead:
   - Click the **YAML** button in the Service editor.
   - Paste the entire content from `.harness/service.yaml`.
   - Edit the `# REPLACE:` comments with your values (org/project IDs, connector names, image path, repo, etc.).
   - **Save**.

## Expected result

After following the steps above, you should have:

- A new service named (e.g.) `nginx_service` in **Deployments** → **Services**.
- Its **Artifacts** tab shows `DockerRegistry` with the image `library/nginx:stable`.
- Its **Manifests** tab shows `K8sManifest` sourced from your Git repo (with the branch/paths/values file configured).
- The service is **ready to use** in any Deploy stage, but no deployment happens here — creating and validating the service definition **is** the skill.
- If you later need to deploy this service, you'll reference it in a pipeline with an **Environment** and **Infrastructure Definition** (the *where* to deploy), then run a **Deploy stage**.

## Optional: see it deploy

`.harness/pipeline.yaml` is a minimal Deploy stage that references the service.
To run it you also need an **Environment** + **Infrastructure Definition** (the
*where*) — see the sibling tidbit `cd-tidbits-environment-setup`. With a healthy
delegate that can reach your Git repo and cluster, the stage fetches the manifest,
resolves `<+artifacts.primary.image>`, and runs a `K8sRollingDeploy`.

## Manifest hosting alternatives

- **Git** (this repo): `store.type: Github|Gitlab|Bitbucket|Git`.
- **Harness File Store**: `store.type: Harness` with `files: [/Templates/deployment.yaml]`
  — good when you don't want an external repo. Upload the files under
  Project Settings → File Store first.
- **Helm / Kustomize**: separate manifest types for chart/overlay-based workloads.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Service Definition is not defined for service [...]` at deploy | The service was saved with only name/identifier — the `serviceDefinition` block didn't persist. | Re-save the service with the full YAML (artifacts + manifests). In the API, pass the whole definition in the `yaml` field. |
| `Unsupported Store Config type: [Inline]` on a K8s manifest | `store.type: Inline` is not valid for `K8sManifest`. | Use `Github`/`Git`/`Harness` (File Store). Inline manifest text is not a K8s manifest store. |
| `Delegate(s) unable to connect to GIT: ...` | The delegate can't reach the manifest repo. | Ensure the delegate has outbound access to the Git host, and the Git connector's repo/branch/URL are correct. |
| `Invalid connectorRef` / connector not found | Wrong scope prefix or id. | Use the full ref: `account.<id>`, `org.<id>`, or `<id>` for a project-scoped connector. |
| Image not found at deploy | Wrong `imagePath`/`tag`, or private image without creds. | Official public images use `library/<name>`; verify the tag exists; use a connector with pull rights for private images. |

## Reference

- [Harness Kubernetes services](https://developer.harness.io/docs/continuous-delivery/deploy-srv-diff-platforms/kubernetes/kubernetes-services/)
- [CD artifact sources (Docker, Artifactory, HAR)](https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/services/artifact-sources/)
- [Add container images as artifacts for K8s](https://developer.harness.io/docs/continuous-delivery/deploy-srv-diff-platforms/kubernetes/cd-kubernetes-category/add-artifacts-for-kubernetes-deployments/)
- [Services and Service overrides overview](https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/services/services-overview)
