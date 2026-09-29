# Tidbyt apps

Personal Tidbyt apps. The device only displays a rendered WebP; something has to re-render and push on a schedule. This repo does that locally for preview, and in AWS for always-on updates.

First app: **GitHub Status** — live GitHub.com platform status from [githubstatus.com](https://www.githubstatus.com/api/v2/summary.json).

## Local preview

1. `make setup` (installs [pixlet](https://github.com/tronbyt/pixlet) via Homebrew if needed, copies `.env.example` → `.env`)
2. Fill in `.env` from the Tidbyt phone app: **Settings → Get API Key**
3. `make preview APP=github-status` and open http://localhost:8080
4. `make push APP=github-status` once, or `make watch` to loop on your laptop

Add another app later as `apps/<name>/` with `app.json` + a `.star` file. `make push-all` and the Lambda both walk that folder.

## AWS (always-on)

One Lambda, once a minute, runs `scripts/push.sh --all`. GitHub Actions **deploys** that function; it does **not** refresh the Tidbyt (so a GitHub outage does not freeze the status monitor).

Estimated cost: about **$0–$1/month** for one app, **$0–$2** around eight.

### One-time AWS bootstrap

From a machine already logged into AWS (`aws sts get-caller-identity`):

```bash
aws cloudformation deploy \
  --template-file infra/github-oidc.yaml \
  --stack-name tidbyt-apps-gha-oidc \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides GitHubOrg=MichaelJ43 GitHubRepo=tidbyt-apps
```

If this account already has the `token.actions.githubusercontent.com` OIDC provider, add `CreateOidcProvider=false`.

Then copy the role ARN:

```bash
aws cloudformation describe-stacks \
  --stack-name tidbyt-apps-gha-oidc \
  --query "Stacks[0].Outputs[?OutputKey=='GitHubActionsRoleArn'].OutputValue" \
  --output text
```

### GitHub Actions secrets

Add these under **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | What it is |
|---|---|
| `AWS_ROLE_ARN` | IAM role ARN from the bootstrap stack output `GitHubActionsRoleArn` (looks like `arn:aws:iam::123456789012:role/tidbyt-apps-github-actions`) |
| `AWS_REGION` | AWS region for the stack, e.g. `us-east-1` |
| `TIDBYT_DEVICE_ID` | Device ID from the Tidbyt app: **Settings → Get API Key** |
| `TIDBYT_API_TOKEN` | API token from the same screen |

No other secrets are required. After those four are set, push to `main` (or run **Actions → Deploy → Run workflow**). The workflow builds the container, deploys stack `tidbyt-apps`, and EventBridge starts invoking the Lambda every minute.
