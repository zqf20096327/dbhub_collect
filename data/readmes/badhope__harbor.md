# Harbor

**English** · [简体中文](README.zh-CN.md)

A self-hosted publishing hub for people who write in more than one place.
Write a piece once, send it to the platforms you already use, and keep every copy in sync.
Accounts, drafts and history stay on your machine.

[![CI](https://github.com/badhope/harbor/actions/workflows/ci.yml/badge.svg)](https://github.com/badhope/harbor/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

![Harbor walkthrough](docs/screenshots/harbor-demo.gif)

*Animated walkthrough. [Open the MP4](docs/screenshots/harbor-demo.mp4) if the GIF does not play.*

## Why Harbor

- **One draft, many places.** Write in Markdown, choose the platforms that fit the piece, and publish from one rail that shows what each platform can actually do.
- **Edit once, update everywhere.** Where the platform supports it, a published copy is updated in place instead of being posted again.
- **Stop when a platform stops you.** CAPTCHA, risk control or an expired session pauses the task, tells you what happened, and resumes where it stopped.
- **Local by default.** Accounts, cookies and drafts live on the machine running Harbor. No hosted account and no telemetry.
- **Yours to adjust.** A content profile holds your voice, posting windows and engagement limits. Every platform has an SOP you can read, edit or reset.
- **Optional AI, not a requirement.** AI drafting, review and MCP access are there when you want them; the publishing flow works without them.

## A closer look

![Content profile](docs/screenshots/09-profile.png)

*A content profile: writing direction, voice, quotas, posting windows, and a personal SOP for each platform.*

![Platform accounts](docs/screenshots/10-platforms.png)

*Platform accounts: browser logins for sites that need them, credential forms for API-based sites.*

## Quick start

Requires Python 3.11+, [uv](https://docs.astral.sh/uv/), Node 20+ and pnpm.

```bash
git clone https://github.com/badhope/harbor.git
cd harbor

# Terminal 1 — backend
cd backed
uv sync
uv run uvicorn app.factory:create_app --factory --host 127.0.0.1 --port 8000 --reload

# Terminal 2 — frontend
cd web
pnpm install
pnpm dev            # http://127.0.0.1:5173
```

Open <http://127.0.0.1:5173>. The dev server proxies `/api` to port 8000.

The first launch opens a three-step setup: create a profile, connect platforms, copy the MCP config. The same profile and SOP files can be created from the CLI:

```bash
uv run --project backed python -m backed.cli init --name demo --platforms juejin,csdn
```

## Platform support

Adapters ship for Zhihu, Juejin, CSDN, Bilibili, Cnblogs, Toutiao, OSChina, SegmentFault, 51CTO, MetaWeblog blogs (WordPress/Typecho), WeChat Official Accounts, GitHub Pages, Dev.to, Telegraph and Xiaohongshu.

Browser-login platforms store their session in a local profile. API platforms take credentials in *Settings → Platform accounts → Configure credentials*; the key is written locally and shown only as a mask. See [PLATFORM_CONNECTION.md](PLATFORM_CONNECTION.md) for the field list and CLI equivalents.

> Login happens on the machine running Harbor, never inside an AI client's browser. An MCP client can read status and publish, but cannot log in for you.

## Documentation

Start at [docs/README.md](docs/README.md). The short list:

- [Login and sessions](docs/guides/login.md)
- [MCP clients](docs/guides/mcp-clients.md)
- [Platform connections](PLATFORM_CONNECTION.md)
- [Architecture](docs/architecture/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Audit reports](docs/audit/AUDIT.md)
- [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)

## Acknowledgements

Harbor stands on open-source work. The MCP servers, libraries and tools it uses are listed in [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md).

## License

MIT — see [LICENSE](LICENSE).
