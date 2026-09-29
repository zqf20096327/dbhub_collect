# KitDev Space

[![CI](https://github.com/hamedniroomand/kitdev-space/actions/workflows/ci.yml/badge.svg)](https://github.com/hamedniroomand/kitdev-space/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Developer tools that run in the browser. Convert, inspect, and clean data without an upload.

**[kitdev.space](https://kitdev.space)**

The hub has JSON, YAML, TOML, and XML converters, a SQLite studio, an EXIF remover, hash and ID
generators, DNS and TLS inspectors, and more. The work runs in the browser. A tool calls the server
only when the browser cannot do the work, such as a DNS lookup. Each page states where its work
runs.

Built with [Nuxt 4](https://nuxt.com), [Nuxt UI](https://ui.nuxt.com), and [Bun](https://bun.sh).
The pages are prerendered, and the server routes run on Vercel.

## Development

Bun 1.4 or later is required.

```bash
bun install
bun run dev
```

`.env` is optional. Copy `.env.example` to enable analytics, error monitoring, or the OG image
secret. Each feature stays off while its value is empty.

```bash
bun run lint
bun run typecheck
bun run test            # Vitest and bun test
bun run test:e2e        # build, then Playwright (run `bunx playwright install chromium` once)
bun run build           # production build; `bun run preview` serves it
```

## Project layout

| Path | Holds |
| --- | --- |
| `app/pages/hub/` | One page per tool, grouped by category |
| `app/components/` | Shared components, such as the tool frame and the editors |
| `shared/utils/` | Logic for the browser and the server, and the tool registry in `tools.ts` |
| `server/api/` | Routes for work that needs the server |
| `docs/` | [Architecture](docs/architecture.md) and [security controls](docs/security-controls.md) |

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). To report a vulnerability, read [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
