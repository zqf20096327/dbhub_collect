# CI Tidbit — Secrets Management

Store sensitive values (API tokens, passwords) as Harness **Text Secrets** and reference them safely in a pipeline. The secret value never appears in YAML and is automatically **masked with asterisks** in logs.

## The problem this solves

Hardcoding tokens in YAML or `.env` files leaks them into Git history and build logs. Harness Text Secrets store the value encrypted in a Secret Manager. Your pipeline only holds a reference — at runtime, Harness decrypts and injects the value, then masks it in every log line.

## What you will build

A single CI stage on Harness Cloud with one Run step that:

- Binds a Text Secret to an environment variable: `MY_SECRET: <+secrets.getValue("tidbit_demo_secret")>`
- Prints **only the length** of the secret — proving it resolved without revealing it
- Fails the build if the secret is empty (wrong id or wrong scope)

No git clone, no app, no delegate — runs entirely on Harness Cloud.

## Prerequisites

- A Harness account with a **Project** (you'll need its org + project identifiers)
- Permission to create Secrets and run pipelines
- Harness Cloud build credits (available by default on new accounts)

## Step 1 — Create the secret in the Harness UI

Harness intentionally does not let you type a secret value into YAML. You create it once in the UI:

1. Go to **Project Settings → Secrets → + New Secret → Text**
2. Keep the default **Harness Built-in Secret Manager**
3. Enter a **Name** — Harness auto-generates the **Id** (avoid hyphens in the id)
4. Select **Inline Secret Value**, paste your value, then **Save**

For this tidbit, create one secret to follow along:

| Name / Id | Value to paste | Expression to use in YAML |
|-----------|---------------|---------------------------|
| `tidbit_demo_secret` | any throwaway string (e.g. `dummy-not-a-real-token`) | `<+secrets.getValue("tidbit_demo_secret")>` |

Real-world examples created the exact same way:

| Purpose | Suggested Id | What to paste |
|---------|--------------|---------------|
| GitHub PAT | `github_pat` | a GitHub personal access token |
| Docker username | `docker_username` | your registry username |
| Docker password | `docker_password` | your registry password or access token |

## Step 2 — Understand scope prefixes

Secrets can live at project, org, or account level. The expression prefix tells Harness where to look:

| Secret lives at | Expression |
|----------------|------------|
| Project | `<+secrets.getValue("tidbit_demo_secret")>` |
| Org | `<+secrets.getValue("org.tidbit_demo_secret")>` |
| Account | `<+secrets.getValue("account.tidbit_demo_secret")>` |

## Step 3 — Import and run the pipeline

1. In your Harness project, go to **Pipelines → Create a Pipeline**
2. Switch to the **YAML** editor and paste the contents of `.harness/pipeline.yaml`
3. Edit the two `# REPLACE:` lines — set `orgIdentifier` and `projectIdentifier` to your values (or leave `<+input>` to supply them at run time)
4. If you used a different secret id, update `tidbit_demo_secret` in the `envVariables` block
5. **Save**, then click **Run → Run Pipeline**

## Expected output

Open the **Prove secret resolves** step log. You should see:

```
Checking secret length (value stays hidden)
len of secret: 22
SUCCESS: secret was injected.
```

A non-zero length confirms Harness decrypted and injected the secret. The build finishes green.

## Try it — see the masking in action

Uncomment the `echo "masked value: $MY_SECRET"` line in the YAML and re-run. Harness replaces the secret value with `****` in the log — even when you deliberately print it.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `len of secret: 0` / `FAIL: secret is empty` | Secret id doesn't match, or wrong scope | Check the **Id** (not Name) in Project Settings → Secrets; add `org.` or `account.` prefix if needed |
| Expression printed literally in logs | Typo or wrong YAML field | Confirm the expression is in `envVariables` or `command` with correct indentation |
| Value not masked after `base64 -d` or `cat` | Harness masks exact matches only | Decoded output is a different string — avoid piping secrets through transforms |
| Hyphens in the id cause errors | Shell/expression parser issue | Use underscores in secret ids, not hyphens |

> **Never export a secret as an output variable** — output variables are visible in build details and are not masked.

## Reference docs

- [Add and reference text secrets](https://developer.harness.io/docs/platform/secrets/add-use-text-secrets)
- [Secrets and log sanitization](https://developer.harness.io/docs/platform/secrets/secrets-management/secrets-and-log-sanitization)
- [Run step settings](https://developer.harness.io/docs/continuous-integration/use-ci/run-step-settings)
