<p align="center">
  <a href="docs/images/hero.png"><img src="docs/images/hero.png" width="880" alt="The Crucible CE incident command center in a browser, with a page acknowledgment open on a phone"></a>
</p>

# Crucible CE

**A self-hosted out-of-band crisis management platform.**

[![License: PolyForm Internal Use](https://img.shields.io/badge/license-PolyForm%20Internal%20Use-blue.svg)](LICENSE)
[![Self-hosted](https://img.shields.io/badge/deploy-self--hosted-ea580c.svg)](docs/install.md)
[![CI](https://github.com/Crucible-CE/crucible-ce/actions/workflows/ci.yml/badge.svg)](https://github.com/Crucible-CE/crucible-ce/actions/workflows/ci.yml)

When ransomware, an identity compromise or a cloud outage takes down your email, chat and sign-in, your response still has to run somewhere. Crucible CE is that place. It runs on a server you control, outside your corporate network and identity plane, so you can reach your responders, coordinate the response and keep a record while your normal tools are down.

Crucible CE can page people over email, SMS and voice, with a fully customizable escalation matrix. SMS and voice paging need your own Twilio account. It has its own accounts, its own database and its own delivery providers, so nothing it needs depends on the systems that are failing.

On top of that, CE has incident command tools for the response itself: a war room, an action board, a decisions log and a tamper-evident record. It also runs tabletop exercises, so your team can practice the response before you need it.

<p align="center">
  <a href="docs/images/paging-demo.gif"><img src="docs/images/paging-demo.gif" width="880" alt="Paging an outside IR retainer from the incident, watching delivery per channel, and the retainer acknowledging from the emailed link"></a>
</p>
<p align="center"><sub>Paging an outside IR retainer. SMS and voice show "skipped" because this install has no Twilio account.</sub></p>

## Out of band by design

- **Separate from your environment.** CE keeps its own accounts and has no SSO on purpose. It does not depend on your directory, email, chat or network, so a compromise of those does not lock your responders out.
- **Host it apart.** Best practice is to run it outside your corporate network. Use a separate cloud account, its own domain and DNS, and email and SMS providers that don't depend on your systems. Securing access is up to you. See [docs/deployment.md](docs/deployment.md).
- **Secure sign-in.** Two-factor sign-in supports authenticator apps, security keys, passkeys and recovery codes. An administrator can require it for everyone. See [docs/authentication.md](docs/authentication.md).
- **Evidence you can trust.** Actions are written to a hash-chained ledger, and the case file exports as an encrypted package signed with Ed25519, with a verifier script anyone can run offline.

## Out-of-band communication

- **Paging.** Email through SMTP or Resend. SMS and voice require a Twilio account, which you bring and configure with your own keys. Signed webhooks and plugins need no account. CE does not send SMS or voice on its own. Pages retry and are rate limited. See [docs/paging.md](docs/paging.md).
- **Acknowledgment.** Acknowledge by link, SMS reply or voice keypress. Unacknowledged pages escalate up the roster.
- **Escalation matrix.** Internal and external contacts by tier and role. Email and phone are verified separately. SMS and voice go only to a verified phone or one an administrator allowed.
- **Delivery providers.** Use the built-in providers or write your own plugin. See [docs/delivery-providers.md](docs/delivery-providers.md) and [providers/README.md](providers/README.md).
- **Broadcast messaging.** Message members and escalation contacts over the paging channels, with delivery status and acknowledgements.
- **Guest links.** Invite outside counsel, an IR firm or an insurer to one incident by link, with no account. They see its summary, chat and evidence, and nothing else. See [docs/incidents.md](docs/incidents.md).
- **Public status pages.** One page per incident with the updates you post to it. Subscribers confirm by email and get each update.

## Incident command

- **Incidents.** Severity, status, response roles, participants, presence, and a timeline written to the ledger.
- **War room.** Real-time chat and a link to your own call bridge.
- **Action board.** Tasks with owners, due times, acknowledgments, comments and attachments. Corrective actions stay open after the incident closes.
- **Decisions log.** What was decided, by whom, when, and why.
- **Reporting.** Status updates, SITREPs, stakeholder notifications, shift handover and postmortems.
- **Evidence vault.** Uploads encrypted at rest with AES-256-GCM, with an access log.
- **Locked incidents.** Only participants, the incident commander and administrators can see them. Only the incident commander and administrators can edit them. Pages for a locked incident carry no details.
- **Playbooks.** Playbooks from Documents, suggested by rules and run as a checklist on the incident.
- **Also.** Calendar with ICS feeds, MITRE ATT&CK tagging, SLA timers, metrics, an org audit log, and invite-based membership with reader, contributor, exercise director and administrator roles.

## Tabletop exercises

Practice the response before you need it. Run Crisis Sim, Playbook Exercise and Strategic TTX exercises from a template library, or build branching scenarios in Studio. Members join with their account. Guests join with an invite code and no account. See [docs/exercises.md](docs/exercises.md).

After an exercise you get a hotwash, objective ratings, an after-action report written with evidence from the record, an improvement plan, and an evidence bundle anyone can verify offline. A schedule, a program report and a readiness score track your practice over time.

## Getting started

- **Setup wizard.** Creates your organization and first administrator. It needs a one-time code from the server log.
- **Onboarding.** A checklist that checks itself off from real data, with practice steps: a training incident that reaches no one, the solo practice Crisis Sim, your IR playbook and your first scheduled exercise. See [docs/first-run.md](docs/first-run.md#onboarding).

## Screenshots

Click a screenshot to open it full size. The data is a fictional company.

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="docs/images/ce-paging.png"><img src="docs/images/ce-paging.png" alt="Pages and per-channel delivery"></a>
      <p><b>Paging.</b> Delivery status per channel. Push comes from a <a href="providers/README.md">provider plugin</a>.</p>
    </td>
    <td width="50%" valign="top">
      <a href="docs/images/ce-matrix.png"><img src="docs/images/ce-matrix.png" alt="Escalation matrix"></a>
      <p><b>Escalation matrix.</b> Internal and external contacts by tier.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="docs/images/ce-ledger.png"><img src="docs/images/ce-ledger.png" alt="Sealed case file and ledger verification"></a>
      <p><b>Case file.</b> A signed, encrypted export and the ledger check.</p>
    </td>
    <td width="50%" valign="top">
      <a href="docs/images/ce-command.png"><img src="docs/images/ce-command.png" alt="Incident command center"></a>
      <p><b>Command center.</b> Severity, status, the incident log, SLAs and response roles.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="docs/images/ce-warroom.png"><img src="docs/images/ce-warroom.png" alt="War-room chat"></a>
      <p><b>War room.</b> Chat, presence and a bridge link.</p>
    </td>
    <td width="50%" valign="top">
      <a href="docs/images/ce-actions.png"><img src="docs/images/ce-actions.png" alt="Action board and decisions log"></a>
      <p><b>Action board.</b> Tasks and the decisions log.</p>
    </td>
  </tr>
</table>

## Quickstart (Docker)

You need Docker with Compose and `openssl`. Give Docker at least 4 GB of memory. No image is published yet. The first run builds one from source and takes several minutes.

```bash
git clone https://github.com/Crucible-CE/crucible-ce.git
cd crucible-ce
cp .env.docker.example .env
# Set POSTGRES_PASSWORD, NEXTAUTH_SECRET and MASTER_KEK in .env.
# Generate each with: openssl rand -hex 32
docker compose up -d --build
docker compose logs app | grep "setup code"
```

1. If the last command prints nothing, wait a few seconds and run it again.
2. Open `PUBLIC_URL` from your `.env` (default [http://localhost:3000](http://localhost:3000)) and go to `/setup`.
3. Enter the setup code. Create your organization and admin account.
4. Invite everyone else from **Org admin > Members**.

The app does not start with placeholder or short secrets. It runs as one container. See [docs/install.md](docs/install.md) and [docs/first-run.md](docs/first-run.md).

> **Back up `.env`.** `MASTER_KEK` encrypts evidence and sensitive fields. If you lose it, that data can't be recovered. See [docs/backup-restore.md](docs/backup-restore.md).

### Port and address

- **Port in use.** If port 3000 is taken, set `CRUCIBLE_PORT` and `PUBLIC_URL` in `.env` to another port, for example `CRUCIBLE_PORT=3100` and `PUBLIC_URL=http://localhost:3100`. They must match.
- **Other computers.** Set `PUBLIC_URL` to the exact address people open, for example `http://192.168.1.20:3000`. If it doesn't match, sign-in fails.
- **TLS.** Outside a test, put CE behind a reverse proxy with https. Security keys and passkeys need https except on `localhost`. See [docs/reverse-proxy.md](docs/reverse-proxy.md).

After you change `.env`, run `docker compose up -d`.

### Email, SMS and webhooks

These are optional. Without email, copy invite links and send them yourself. To send pages and invites by email, set `SMTP_HOST` or `RESEND_API_KEY`. For SMS and voice, set your Twilio keys. See [docs/paging.md](docs/paging.md).

### Everyday commands

| Task | Command |
|---|---|
| Stop | `docker compose stop` |
| Start | `docker compose up -d` |
| View logs | `docker compose logs -f app` |
| Upgrade | `git pull && docker compose up -d --build` |
| Remove containers, keep data | `docker compose down` |
| Reset a password (locked out) | `docker compose exec app npm run reset-password -- --email you@example.com` |

`docker compose down -v` also deletes the database and uploads. Back up first. See [docs/upgrading.md](docs/upgrading.md).

Release images are published to `ghcr.io/crucible-ce/crucible-ce` (amd64 only). To skip the build, run `docker compose pull && docker compose up -d`. To pin a release, set `CRUCIBLE_VERSION` in `.env`, for example `CRUCIBLE_VERSION=0.2.0`. The default is `latest`.

## Run from source

You need Node 24 and Docker.

```bash
npm ci
cp .env.example .env.local     # replace the placeholder secrets
cp .env.local .env             # the Prisma CLI reads .env
npx prisma generate
npm run db:up                  # Postgres, PgBouncer, Redis, Mailpit
npx prisma migrate deploy
npm run dev:full               # app on :3000, socket and cron sidecar on :3001
```

CI runs `npm test`, `npm run typecheck`, `npm run lint` and `npx next build`. For a production-style run, use `npm run prod`. Don't use `next start`. It has no Socket.io and no paging crons. See [docs/install.md](docs/install.md).

## Documentation

- [Install](docs/install.md) and [first run](docs/first-run.md)
- [Deployment](docs/deployment.md)
- [Sign-in and two-factor](docs/authentication.md)
- [Reverse proxy and TLS](docs/reverse-proxy.md)
- [Configuration](docs/configuration.md)
- [Guests, status pages, messaging, playbooks and training incidents](docs/incidents.md)
- [Paging](docs/paging.md), [delivery providers and webhooks](docs/delivery-providers.md), [provider plugins](providers/README.md)
- [Exercises and improvement](docs/exercises.md)
- [Case-file exports](docs/case-file-exports.md)
- [Backup and restore](docs/backup-restore.md), [upgrading](docs/upgrading.md)

## Telemetry

CE sends no telemetry, including about Cloud notes. It calls out only to the providers you configure. These are email, Twilio, webhooks, plugins and S3 storage. The fonts are bundled and served from your server. Building the image needs internet access for npm packages and OS updates.

## Crucible Cloud

Crucible Cloud is the hosted version. It runs on infrastructure separate from yours. The same hardened sign-in, with hardware security keys and one-time passcodes, is planned.

| | CE | Cloud (Coming Soon) |
|---|---|---|
| Incidents, war room, action board, decisions log and case-file exports | Yes | Yes |
| Paging with escalation over your own email, Twilio, webhooks and plugins | Yes | Yes |
| Guest links and public status pages | Yes | Yes |
| Broadcast messaging | Yes | Yes |
| Incident playbooks from Documents | Yes | Yes |
| Exercises in three modes: Crisis Sim, Playbook Exercise and Strategic TTX | Yes | Yes |
| After-action reports with findings review, and work items | Yes | Yes |
| Exercise schedule, program report, executive dashboard and readiness score | Yes | Yes |
| Hosted out-of-band delivery, with managed SMS and voice paging |  | Yes |
| Mobile app with push paging |  | Yes |
| Exo, the incident assistant that suggests next actions and drafts SITREPs, handovers, postmortems and stakeholder messages |  | Yes |
| Regulatory filing drafts |  | Yes |
| AI posture insights: threat assessment and document gap analysis |  | Yes |
| AI for exercises: Crisis Sim generation, playbook to exercise, grading with quoted evidence and after-action report drafting |  | Yes |
| Transcript reconciliation and AI injects for Strategic TTX |  | Coming soon |

In CE, every AI step has a manual path, and the **Crucible Cloud** page in the side rail describes each Cloud feature. Nothing in CE is locked.

A few manual steps show a one-line Cloud note to contributors, exercise directors and administrators. Each person can dismiss them, and an administrator can turn them off. Set `CLOUD_TRIAL_URL` to show a trial link on the Cloud page. **Export for Cloud** writes a file of your templates and documents for import into Crucible Cloud when it opens. CE never connects to Cloud. See [docs/exercises.md](docs/exercises.md#cloud-notes).

These screenshots are from Crucible Cloud.

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="docs/images/cloud-messaging.png"><img src="docs/images/cloud-messaging.png" alt="Out-of-band messaging in Crucible Cloud"></a>
      <p><b>Messaging.</b> Broadcast over push, SMS, email and voice.</p>
    </td>
    <td width="50%" valign="top">
      <a href="docs/images/cloud-copilot.png"><img src="docs/images/cloud-copilot.png" alt="Active runbook, drafting agents and Exo in Crucible Cloud"></a>
      <p><b>Exo and runbooks.</b> The active playbook step and drafting agents.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="docs/images/cloud-regulatory.png"><img src="docs/images/cloud-regulatory.png" alt="Regulatory filings and obligation clocks in Crucible Cloud"></a>
      <p><b>Regulatory.</b> Obligation clocks and filing drafts.</p>
    </td>
    <td width="50%" valign="top">
      <a href="docs/images/cloud-aar.png"><img src="docs/images/cloud-aar.png" alt="After-action report from an AI-facilitated tabletop in Crucible Cloud"></a>
      <p><b>AI tabletops.</b> An after-action report drafted from the exercise record.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="docs/images/cloud-exec.png"><img src="docs/images/cloud-exec.png" alt="Executive dashboard in Crucible Cloud"></a>
      <p><b>Executive dashboard.</b> Readiness score and document coverage.</p>
    </td>
    <td width="50%" valign="top">
      <a href="docs/images/cloud-mobile.png"><img src="docs/images/cloud-mobile.png" alt="Crucible Cloud mobile companion"></a>
      <p><b>Mobile app.</b> Incidents and emergency alerts.</p>
    </td>
  </tr>
</table>

## Support

- **Bugs and feature requests.** Open a GitHub issue. Support is best effort, with no SLA.
- **Security reports.** See [SECURITY.md](SECURITY.md). Don't open public issues for vulnerabilities.

## License

Copyright REDFOR Security LLC. Crucible CE is source-available under the PolyForm Internal Use License 1.0.0, plus personal and evaluation use. You can run and change it for your organization's internal use. You can't redistribute it or offer it as a service. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

Crucible CE does not accept outside code contributions. Use GitHub issues for bugs and feature requests.
