# CI Tidbit — Docker Build & Push (with Tags, Best Practices & DLC)

> **Harness University Tidbit.** A 5–10 minute, self-paced micro-lesson backed by an executable repo.
> **Skill:** Package an app into a container image, tag it with build/branch/commit metadata, push it to a registry, and turn on **Docker Layer Caching (DLC)** to speed up rebuilds.

---

## What this skill accomplishes

In one Harness CI step (`BuildAndPushDockerRegistry`) you build a Docker image from a multi-stage Dockerfile and push it to a registry under **multiple tags** — an immutable build number plus moving pointers — with **layer caching** enabled so unchanged layers are reused across runs.

This is the day-to-day "ship a container" loop: every commit produces a traceable, cached image.

---

## Tag strategy (the important part)

Push **at least one immutable tag + one moving tag**. This repo pushes three:

| Tag | Expression | Mutability | Use it for |
|-----|-----------|------------|------------|
| Build number | `<+pipeline.sequenceId>` | Immutable (never reused) | Rollback target, audit trail |
| Branch | `<+codebase.branch>` | Moving | "Newest image for this branch" |
| `latest` | `latest` (literal) | Moving | Convenience pointer |

Other useful expressions:

- `<+codebase.commitSha>` — full Git SHA; **fully immutable and traceable to the exact commit**. Great as the canonical immutable tag.
- `<+codebase.shortCommitSha>` — 7-char SHA, friendlier to read.
- `<+codebase.sourceBranch>` — for **PR** builds (use instead of `branch`).

> **Gotcha:** Docker tags cannot contain `/`. A branch like `feature/login` would make `<+codebase.branch>` an invalid tag. For branches with slashes, prefer `<+codebase.shortCommitSha>` or `<+pipeline.sequenceId>`.

---

## DLC vs. Harness Cloud layer caching — the honest distinction

**Docker Layer Caching (DLC)** is a Harness CI Intelligence feature. You enable it with one field on the step:

```yaml
caching: true
```

What "DLC" means depends on **where your build runs**:

| Build infrastructure | What `caching: true` does | Storage you must provide |
|----------------------|---------------------------|--------------------------|
| **Harness Cloud** (this tidbit) | Layers cached in the **Harness-managed** cache store. Zero setup. | **None** — Harness manages it. |
| **Self-hosted delegate / Kubernetes** | Layers cached to your own object store (sometimes called *Delegate Local Cache*). On K8s, requires privileged mode. | **You** configure S3-compatible storage (S3 / GCS) in Default Settings first. |

So "DLC (Delegate Local Cache)" is the **self-hosted framing** of the same feature. On Harness Cloud there is no delegate and no bucket to manage — the **identical `caching: true` flag** gives you Harness-managed layer caching for free. This tidbit runs on Harness Cloud, so you just flip the flag.

> Cache retention on Harness Cloud is 15 days (resets on update). DLC requires S3 / GCS / S3-compatible storage on self-managed infra (Azure Blob is Cache-Intelligence-only).

---

## Best-practices Dockerfile

`sample-app/Dockerfile` is a **multi-stage** build (see `sample-app/main.go`, a tiny Go HTTP server):

```dockerfile
# Stage 1: build (toolchain stays here, never ships)
FROM golang:1.22-alpine AS builder      # pin a specific tag, never :latest
WORKDIR /src
COPY go.mod ./                           # deps first -> cacheable layer
RUN go mod download
COPY . .                                 # source after -> only this layer rebuilds on code change
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /out/app .

# Stage 2: runtime (tiny, no shell, non-root)
FROM gcr.io/distroless/static:nonroot
COPY --from=builder /out/app /app        # ship only the binary
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app"]
```

Why it matters:

1. **Multi-stage** — compiler (~300 MB) stays in stage 1; final image only has the static binary.
2. **Pinned base image** — `golang:1.22-alpine`, not `:latest` → reproducible builds, reliable cache keys.
3. **Layer ordering** — copy `go.mod` and resolve deps before copying source, so DLC reuses the dependency layer when only code changes.
4. **Minimal + non-root runtime** — `distroless/static:nonroot` has no shell/package manager and runs as uid 65532 → small attack surface.

---

## Prerequisites

- A Harness account with **CI** enabled (Free tier works) using **Harness Cloud** build infra.
- A **code connector** (e.g. GitHub) so the stage can clone a repo. The pipeline needs a real codebase so `<+codebase.branch>` / `<+codebase.commitSha>` resolve.
- A **Docker Registry connector** (username/password auth) pointing at your registry:
  - Docker Hub URL: `https://index.docker.io/v2/`
  - The connector references a **secret** (your registry password / access token) stored in Harness Secrets. **No secret is committed to this repo.**
- A registry repository you can push to, e.g. `<your-dockerhub-user>/ci-tidbits-docker-build-push`.

---

## Run it — step by step

> The pipeline **clones this repo and builds the real committed `sample-app/Dockerfile`** — there is no inline/generated Dockerfile. Point `codebase.repoName` at your fork so the clone contains `sample-app/`.

1. **Fork / clone** this repo so your fork contains `sample-app/` (the Dockerfile + Go app the pipeline builds).
2. **Create the Docker connector:** Project Settings → Connectors → New Connector → **Docker Registry**.
   - Docker Hub URL `https://index.docker.io/v2/`, username + a password/token secret.
   - Test the connection. Reference it as `account.<id>` (account scope) or a bare id (project scope).
3. **Import the pipeline:** Pipelines → New Pipeline → Import from `/.harness/docker_build_push.yaml`, or paste the YAML.
4. **Edit every `# REPLACE:`** line:
   - `connectorRef` (code + Docker), `repoName` (your fork), `repo` (your registry path), branch.
5. **Run** the pipeline (branch = `main`).
6. **Expected success:** the `Build and Push Image` step clones your fork, builds `sample-app/Dockerfile`, and logs the pushed image + digest. In your registry you'll see **three tags**: the build number (e.g. `4`), the branch (`main`), and `latest`.
7. **Run again** and watch the build step reuse cached layers (faster) thanks to `caching: true`.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Resource not found... Git resource` (fails in ~10s) | `repoName` / branch don't exist or connector can't reach the repo | Point `codebase.repoName` at a real, accessible repo + correct branch. |
| `unauthorized: authentication required` on push | Docker connector creds wrong, or `repo` namespace isn't yours | Re-test the connector; ensure `repo` starts with your registry username/namespace. |
| `invalid reference format` / tag rejected | A tag contained `/` (e.g. branch `feature/x`) or uppercase in repo | Use `<+pipeline.sequenceId>` or `<+codebase.shortCommitSha>`; keep repo names lowercase. |
| `<+codebase.branch>` is empty/null | Stage has no codebase (`cloneCodebase: false`) | Keep `cloneCodebase: true` with a configured codebase, or run a branch/PR build. |
| DLC seems to not cache on self-hosted | No S3 storage configured | DLC on delegates/K8s needs S3-compatible Default Settings storage (and K8s privileged mode). Not needed on Harness Cloud. |

---
