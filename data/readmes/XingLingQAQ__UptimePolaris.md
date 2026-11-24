<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/overview-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/readme/overview-light.svg">
  <img src="assets/readme/overview-light.svg" width="100%" alt="Uptime Polaris">
</picture>

<strong>English</strong> · <a href="README-zh-CN.md">简体中文</a> · <a href="README-zh-TW.md">繁體中文（台灣）</a> · <a href="README-zh-HK.md">繁體中文（香港）</a> · <a href="README-ja-JP.md">日本語</a> · <a href="README-ko-KR.md">한국어</a> · <a href="README-fr-FR.md">Français</a> · <a href="README-pt-BR.md">Português (Brasil)</a> · <a href="README-ru-RU.md">Русский</a>

# Uptime Polaris

An all-in-one self-hosted monitoring and status page: uptime checks, host agents, AI model monitoring and public status subscriptions in one place.<br>
Runs on Cloudflare Workers or a Go backend, with a public status page and an admin console, in 9 languages.

<p>
  <a href="https://developers.cloudflare.com/workers/"><img src="https://img.shields.io/badge/Cloudflare-Workers-F38020?style=flat-square&amp;logo=cloudflare&amp;logoColor=white" height="20" alt="Cloudflare Workers"></a>
  <a href="backends/go/README.md"><img src="https://img.shields.io/badge/Go-Backend-00ADD8?style=flat-square&amp;logo=go&amp;logoColor=white" height="20" alt="Go Backend"></a>
  <a href="frontend/README.md"><img src="https://img.shields.io/badge/React-TypeScript-3178C6?style=flat-square&amp;logo=react&amp;logoColor=white" height="20" alt="React + TypeScript"></a>
  <a href="https://github.com/XingLingQAQ/Polaris-Agent"><img src="https://img.shields.io/badge/Rust-Agent-93450A?style=flat-square&amp;logo=rust&amp;logoColor=white" height="20" alt="Rust Agent"></a>
  <a href="docs/configuration.md"><img src="https://img.shields.io/badge/Storage-D1%20%2F%20SQLite%20%2F%20PostgreSQL-4169E1?style=flat-square&amp;logo=postgresql&amp;logoColor=white" height="20" alt="Storage"></a>
</p>

<p><a href="#features">Features</a> · <a href="#backend-options">Backends</a> · <a href="#quick-deploy">Deploy</a> · <a href="#host-agent">Agent</a> · <a href="#documentation">Documentation</a></p>

</div>

## Features

- **Uptime and heartbeat checks**: HTTP, TCP and Push heartbeats, with optional SSL certificate, domain expiry and DNS checks. The Go backend also probes UDP, ICMP, DNS, TLS and WebSocket natively, and internal services can be checked through an Agent.
- **Subscription-based monitoring**: subscribe to public website and model status published by other sites and fold it into your own page. The [official subscription repository](https://github.com/XingLingQAQ/UptimePolaris-Subscriptions) ships templates for Uptime Kuma, Polaris, Statuspage and plain JSON; third-party repositories and custom JSON descriptors are supported too.
- **Host agent**: [polaris-agent](https://github.com/XingLingQAQ/Polaris-Agent) is a small Rust agent for Linux, macOS, Windows and Docker. It reports CPU, memory, disk, load and network, with resource-threshold alerts and side-by-side machine comparison.
- **AI model monitoring**: OpenAI Chat Completions, OpenAI Responses, Anthropic Messages and Gemini protocols, including gateways and local models. Import models from a channel, send custom request parameters and publish a dedicated model page.
- **Multiple public pages and themes**: a monitor page (`/`), a machine page (`/servers`) and an AI model page (`/ai`), each switchable, bindable to its own domain, switched to a maintenance page during windows, and themeable with third-party packages.
- **Notifications across channels**: Telegram, Feishu, Slack, Discord, Webhook, Apprise and ServerChan, routed by global rules or explicit channel selection, with messages in 9 languages.

## Backend options

Both backends share the same frontend and the `/admin` console; pick one for your environment.

| | Cloudflare Worker | Go |
| --- | --- | --- |
| Runtime | Cloudflare Workers | Your own server / Docker |
| Database | D1 or PostgreSQL | SQLite or PostgreSQL |
| Direct probe protocols | HTTP, TCP (UDP and ICMP via an Agent) | HTTP, TCP, UDP, ICMP, DNS, TLS, WebSocket |
| Shortest interval | 60 seconds | 5 seconds |
| Large-scale batching | Optional Cloudflare Queue | In-process scheduler |
| Theme storage | R2 (optional) | Local data directory |

The full comparison is in [backend options](docs/backends.md).

## Quick deploy

### Cloudflare Workers

1. Fork this repository, then import it in the Cloudflare console under **Workers & Pages → Create application → GitHub**, with `npm run build` as the build command and `npm run deploy` as the deploy command.
2. Open `/setup` after deploying and follow the checks to add the required configuration under the Worker's **Settings**:
   - KV binding `CONFIG`
   - Analytics Engine binding `UPTIME`
   - Secret `ADMIN_TOKEN` (a long random string)
   - Optional: D1 binding `DB` (PostgreSQL is used when absent), R2 binding `THEMES` (third-party themes), Queue binding `CHECK_QUEUE` (batched checks)
3. Return to `/setup` to verify the database and create the administrator.

You can also deploy with the button below, which creates a separate repository rather than a fork:

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/XingLingQAQ/UptimePolaris)

Manual deployment, custom domains and PostgreSQL migration are covered in the [deployment guide](docs/deployment.md).

### Self-hosted Go

Download the build for your platform from [Releases](https://github.com/XingLingQAQ/UptimePolaris/releases) and start it:

```sh
chmod +x polaris   # Linux / macOS
./polaris --data-dir ./data
```

```powershell
.\polaris.exe --data-dir .\data
```

It listens on `127.0.0.1:8080` by default. Open `/setup` and use the setup key from the `setup_key` field in the startup log to create the administrator. Docker deployment can start from [`backends/go/compose.yaml`](backends/go/compose.yaml); flags, environment variables and managed updates are in the [Go backend guide](backends/go/README.md).

## Host agent

Sign in to `/admin`, open **Agent management** and add a machine. Copy the install command for its platform and run it there, then manage the service with `pa`:

```sh
pa status
pa restart
pa logs -f
pa update
```

Configuration, remote commands and removal are in the [Agent guide](docs/agents.md).

## Documentation

| Document | Contents |
| --- | --- |
| [Backend options](docs/backends.md) | Worker and Go capability comparison |
| [Deployment](docs/deployment.md) | Cloudflare setup, domains, PostgreSQL and D1 migration |
| [Go backend](backends/go/README.md) | Flags, Docker, managed updates and data migration |
| [Usage](docs/usage.md) | Monitor configuration, Push heartbeats, public pages, maintenance and security |
| [Subscriptions](docs/subscriptions.md) | Subscription repositories, custom descriptors and sync |
| [AI monitoring](docs/ai-monitoring.md) | Channel protocols, bulk import, model pages and key management |
| [Agent](docs/agents.md) | Agent installation, management, configuration and removal |
| [Notifications](docs/notifications.md) | Channels, routing rules and delivery records |
| [Worker Queue](docs/queue.md) | Batched checks on Workers |
| [Themes](docs/themes.md) | Third-party theme installation, configuration and development |
| [Configuration](docs/configuration.md) | Bindings, environment variables and console settings |
| [API](docs/api.md) | Endpoints and authentication |
| [Operations](docs/operations.md) | Upgrades, backup and restore, retention |
| [Troubleshooting](docs/troubleshooting.md) | Diagnosing failures |

## Friends

[LinuxDo](https://linux.do/)

## License

Released under the [MIT License](LICENSE).
