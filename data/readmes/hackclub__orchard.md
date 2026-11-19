<img src=".github/assets/banner.png" alt="Hack Club Orchard" width="100%">

# Hack Club Orchard

### A project made by [Leafd](https://github.com/LeafdTK)

[![Kubernetes](https://img.shields.io/badge/Kubernetes-c93a4f?style=for-the-badge&logo=kubernetes&logoColor=white)](https://docs.orchard.hackclub.com/start/what-is-orchard/)
[![Self-hosted](https://img.shields.io/badge/self--hosted-1a0f11?style=for-the-badge)](https://docs.orchard.hackclub.com/start/install/)
[![License](https://img.shields.io/badge/license-AGPL--3.0-c93a4f?style=for-the-badge&labelColor=1a0f11)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-docs.orchard.hackclub.com-1a0f11?style=for-the-badge)](https://docs.orchard.hackclub.com)

Turn a Linux server into a private hosting platform.

Hack Club Orchard is an open-source, self-hosted platform as a service (PaaS). Connect a repository
from GitHub, GitLab, Gitea or another Git host, and Orchard builds it and runs it behind HTTPS, with a
Postgres database that has point-in-time restore from S3-compatible storage, logs, metrics and
rollbacks. Use the dashboard, the CLI, or your AI agent through the MCP server.

Orchard runs on Kubernetes, but you do not have to touch Kubernetes. One command turns a single Linux
server into a k3s cluster with everything Orchard needs, which suits a home lab, a side project, a small
team, or a trial. For production, run the Helm chart on a multi-node cluster such as
[Talos Linux](https://docs.siderolabs.com/talos), with components you operate, such as Harbor for the
registry. Hack Club runs Orchard this way, on six Talos Linux nodes. [Choose how to run Orchard](https://docs.orchard.hackclub.com/start/install/#choose-how-to-run-orchard)
explains the difference.

Orchard is free and licensed under AGPL-3.0 (the graft SDK for extensions is MIT). Hack Club runs its own
apps on it.
[What is Orchard](https://docs.orchard.hackclub.com/start/what-is-orchard/) ·
[Features](https://docs.orchard.hackclub.com/start/features/) ·
[FAQ](https://docs.orchard.hackclub.com/start/faq/) ·
[Compare](https://orchard.hackclub.com/compare)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/screenshots/project-dark.png">
  <img src=".github/assets/screenshots/project-light.png" alt="A Hack Club Orchard project with its apps, databases and recent builds" width="100%">
</picture>

## Installation

**Please follow the [install guide](https://docs.orchard.hackclub.com/start/install/).** It covers every step in
detail.

For the command alone, you need a Linux server with systemd, an IPv4 address and 20 GB of free disk.
Orchard runs on 2 GiB of RAM, and 8 GiB is recommended. On a smaller server, the installer
[trims Orchard](https://docs.orchard.hackclub.com/operate/small-servers/) to leave memory for your apps.

```bash
curl -fsSL https://assets.orchard.my/install.sh -o orchard-install.sh && sudo bash orchard-install.sh
```

![Installing Hack Club Orchard on a Linux server](.github/assets/install.gif)

> [!IMPORTANT]
> Deployments are network isolated from each other and from the platform by default (on the Helm chart,
> your [CNI must enforce NetworkPolicy](https://docs.orchard.hackclub.com/operate/compatibility/#supported-cnis)),
> but they **share the host kernel** unless you install gVisor or Kata and switch them on. Running
> untrusted code is not safe out of the box. Read [Security and isolation](https://docs.orchard.hackclub.com/operate/security/)
> before letting strangers deploy things.

> [!TIP]
> A fresh install is not a production instance. Secrets, signup mode, TLS cookies, control-plane backups
> and isolation all need a decision from you.
> [Going to production](https://docs.orchard.hackclub.com/operate/production/) walks through the list.

### Already running Kubernetes, or going to production?

The installer builds its own single-node k3s cluster, which [cannot take more nodes yet](https://docs.orchard.hackclub.com/operate/nodes/#on-an-installer-host).
For more than one node, or on a cluster you operate, use the Helm chart instead (Kubernetes 1.30 or later):

```bash
helm install orchard oci://ghcr.io/hackclub/orchard/charts/orchard \
  --namespace orchard --create-namespace -f my-values.yaml
```

The [install guide](https://docs.orchard.hackclub.com/start/install/) has a minimal values file, DNS and every
flag.

## How Hack Club Orchard compares

Coolify, Dokploy and CapRover run apps as Docker containers and manage them from a web dashboard. Dokku
gives you git-push deploys on a Docker host, and Kamal deploys containers to servers you manage over SSH.
Orchard runs on Kubernetes instead, with k3s set up for you by the installer. Because of that, apps get
default-deny network isolation from each other on a CNI that enforces NetworkPolicy, managed Postgres
runs on CloudNativePG with point-in-time restore, builds run in rootless BuildKit, and the Helm chart
can run Orchard on a multi-node cluster. The cost is weight: the cluster, the operators and the metrics and logs stack use
memory before your first app runs. The [comparison table](https://orchard.hackclub.com/compare) has the
details, with sources.

## Works with your agent

Connect Claude, Cursor or any MCP client, and it can deploy apps, add databases, read logs and roll back
a bad deploy. [Set up your agent](https://docs.orchard.hackclub.com/agent-setup/).

It can read the docs for you:

```
Read the Orchard docs at https://docs.orchard.hackclub.com/llms.txt and use them to help me. Fetch the pages you need before you answer, and link the pages you used.
```

It can install Orchard for you too:

```
Install Orchard on my server following https://docs.orchard.hackclub.com/start/install.md. Ask me before anything that is not reversible.
```

## Features

- **Deploy from anywhere.** Deploy from GitHub, GitLab, Gitea or another Git host, from a container
  image, or from a folder on your computer (with S3 storage). With auto-deploy on, every push builds and
  deploys your app. On GitHub, auto-deploy needs the GitHub App.
- **HTTPS and domains.** Every web port can get an HTTPS URL (self-signed on a LAN install), and you can add [your own domains](https://docs.orchard.hackclub.com/deploy/domains/) or use a [wildcard certificate](https://docs.orchard.hackclub.com/operate/wildcard-certificates/).
- **Tailscale.** Put an app on your [tailnet](https://docs.orchard.hackclub.com/deploy/tailscale/) instead of the public internet.
- **Managed Postgres.** Add a database with backups to S3-compatible storage and point-in-time restore.
- **Logs and metrics.** Search logs and see requests, errors and resource use for each app. Request data
  needs Traefik or HAProxy as the ingress controller.
- **Rollbacks.** Go back to an earlier version when a deploy goes wrong.
- **Templates.** Deploy any of 90+ [ready-made apps](https://orchard.hackclub.com/templates).
- **Teams.** Organizations, roles, SSO and audit logs.

## Limitations

Postgres is the only managed database, and control-plane backups are off by default. [Known limitations](https://docs.orchard.hackclub.com/start/limitations/)
lists the rest, grouped by area, with a workaround where one exists. Read it before you install.

## Contributing

Issues and pull requests are welcome. [CONTRIBUTING.md](CONTRIBUTING.md) covers running it locally and
how commits drive releases. [DEVELOPERS.md](DEVELOPERS.md) explains how Orchard works for people changing it, and
[Architecture](https://docs.orchard.hackclub.com/operate/architecture/) explains how the pieces fit
together on a cluster. Report security issues privately, as [SECURITY.md](SECURITY.md) describes.

## Help

Browse the [Directory](https://docs.orchard.hackclub.com/directory/), the
[FAQ](https://docs.orchard.hackclub.com/start/faq/) or
[Troubleshooting](https://docs.orchard.hackclub.com/operate/troubleshooting/). For a bug or a question
the docs do not answer, open an [issue](https://github.com/hackclub/orchard/issues).

## License

[AGPL-3.0](LICENSE). The license covers the code, not the Orchard and Hack Club names and logos. For
those, refer to [TRADEMARK.md](TRADEMARK.md).

---

Made by [Leafd](https://github.com/LeafdTK).
