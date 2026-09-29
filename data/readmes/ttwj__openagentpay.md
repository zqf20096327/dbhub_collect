# OpenAgentPay

**An open-source reference implementation demonstrating how emerging agent protocols work together as a coherent system for agentic commerce.**

---

## Why OpenAgentPay Exists

As agent ecosystems mature, the industry is converging on multiple overlapping protocols—**MCP**, **MCP-UI**, and **AP2**—that each address a specific layer of the problem. **A2A** is a promising coordination layer, but in this repo it is currently a **future plan** (see below).

| Protocol | Layer | Purpose |
|----------|-------|---------|
| **MCP** (Model Context Protocol) | Capability Discovery | How agents discover and invoke tools |
| **MCP-UI** | User Mediation | How agents render interactive widgets for human review |
| **AP2** (Agent Payments Protocol) | Value Movement | How agents securely authorize and execute payments |

What is missing today is a **concrete, end-to-end example** that shows how these protocols can work together in practice to power real commerce experiences. OpenAgentPay exists to fill that gap.

---

## What You Can Learn Here

OpenAgentPay is a **reference and learning platform**. Every feature demonstrates a specific protocol interaction:

### Protocol Demonstrations

| Feature | Protocols Used | What It Shows |
|---------|----------------|---------------|
| **Product Search** | MCP + MCP-UI | Tool invocation → Widget rendering |
| **Restaurant Booking (Demo UX)** | MCP + MCP-UI | Tool invocation → Widget rendering |
| **Flight/Hotel Search** | MCP + MCP-UI | Widget-based search and follow-ups |
| **Bill Payment** | MCP + AP2 | Human-present payment authorization (L4) |
| **EV Charging** | MCP + AP2 | Human-not-present mandate (L5/L6) |
| **Bill Split (Future)** | AP2 (today) / A2A (future) | Multi-party negotiation + settlement |
| **Activity & Receipts** | AP2 | Transaction audit trail with VDC proofs |
| **Wallet** | AP2 | Payment mandates and spending limits |
| **Calendar (Future)** | MCP + A2A (future) | Event coordination across agents |

### Key Concepts Demonstrated

1. **Verifiable Digital Credentials (VDCs)**: Tamper-evident, cryptographically signed authorization objects
2. **Session Capabilities**: Scoped permissions granted per conversation
3. **MCPAppsDelegate**: Controlled data sharing between agents with user consent
4. **Human-Present vs Human-Not-Present**: Different authorization levels based on user availability
5. **Protocol Attribution**: Every widget shows which protocol rendered it

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│  ┌──────────────┐  ┌──────────────────────┐  ┌──────────────────┐  │
│  │   Sidebar    │  │    Main Content      │  │    Copilot       │  │
│  │  (Nav/Agents)│  │  (Chat/Apps/Utils)   │  │  (Protocol View) │  │
│  └──────────────┘  └──────────────────────┘  └──────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│                         PROTOCOL LAYER                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐               │
│  │   MCP   │  │ MCP-UI  │  │   A2A   │  │   AP2   │               │
│  │  Tools  │  │ Widgets │  │ Agents  │  │Payments │               │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘               │
├─────────────────────────────────────────────────────────────────────┤
│                         DATA LAYER                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │   Conversations │  │   Transactions  │  │    Mandates     │    │
│  │   (Threads)     │  │   (AP2 Audit)   │  │    (VDCs)       │    │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Node.js 20+ (matches CI)
- pnpm 10.4.1 (via Corepack recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/openagentpay/openagentpay.git
cd openagentpay

# (Recommended) Ensure pnpm version matches the repo
corepack enable
corepack prepare pnpm@10.4.1 --activate

# Install dependencies
pnpm install

# Set up environment variables
cp .env.example .env

# Push database schema
pnpm db:push

# Start development server
pnpm dev
```

### Dev Loop (OSS-grade, minimal)

```bash
pnpm dev
pnpm check
pnpm test
# optional
pnpm test:e2e
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | MySQL/TiDB connection string |
| `OPENAI_API_KEY` | OpenAI API key for LLM |
| `STRIPE_SECRET_KEY` | Stripe API key for payments |
| `PUBLIC_BASE_URL` | Public origin for generating absolute widget URLs (recommended for MCP‑UI `text/uri-list`) |
| `VITE_APP_TITLE` | Application title (default: "OpenAgentPay") |

---

## Project Structure

```
openagentpay/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   │   ├── widgets/    # MCP-UI widget implementations
│   │   │   └── layout/     # App shell and navigation
│   │   ├── pages/          # Route pages
│   │   └── contexts/       # React contexts
├── server/                 # Express + tRPC backend
│   ├── tools/              # MCP tool implementations
│   ├── services/           # Business logic
│   └── routers/            # tRPC routers
├── drizzle/                # Database schema
├── shared/                 # Shared types and constants
│   ├── credentials/        # VDC type definitions
│   └── app-registry.ts     # Agent/app registry
├── docs/                   # Documentation
│   ├── AP2-*.md            # AP2 protocol specs
│   ├── MCP-*.md            # MCP integration guides
│   └── archive/            # Historical planning docs
└── design/                 # UI/UX design assets
```

---

## Documentation

### Protocol Specifications

- [AP2 Quick Start](docs/AP2-QUICK-START.md) - Get started with Agent Payments Protocol
- [AP2 Glossary](docs/AP2-GLOSSARY.md) - Key terms and definitions
- [AP2 VDC Deep Dive](docs/AP2_VDC_DEEP_DIVE.md) - Verifiable Digital Credentials explained
- [AP2 Payment Intent Spec](docs/AP2-PAYMENT-INTENT-SPEC.md) - Payment authorization levels

### Integration Guides

- [Adding New Widgets](docs/ADDING_NEW_WIDGET.md) - Create MCP-UI widgets
- [Adding Design Systems](docs/ADDING_NEW_DESIGN_SYSTEM.md) - Support new AI platforms
- [Widget Migration Checklist](docs/WIDGET_MIGRATION_CHECKLIST.md) - Canonical MCP‑UI widget patterns
- [API Reference](docs/API_REFERENCE.md) - tRPC endpoint documentation

### Architecture

- [Consent System](docs/CONSENT_SYSTEM.md) - VDC-based authorization framework
- [App Interaction Modes](docs/APP_INTERACTION_MODES.md) - How agents coordinate
- [First Principles Analysis](docs/FIRST_PRINCIPLES_ANALYSIS.md) - Design rationale

---

## Protocol References

OpenAgentPay implements and extends these open protocols:

| Protocol | Source | Status |
|----------|--------|--------|
| **AP2** | [Google Agentic Commerce](https://github.com/google-agentic-commerce/AP2) | Reference implementation |
| **MCP** | [Anthropic MCP](https://modelcontextprotocol.io/) | Tool layer integration |
| **MCP-UI** | [OpenAI MCP-UI](https://platform.openai.com/docs/guides/tools) | Widget rendering |
| **A2A (Future)** | [Google A2A](https://github.com/google/A2A) | Planned coordination layer |

---

## Future Plans: A2A (Agent-to-Agent)

OpenAgentPay does **not** currently implement a real A2A runtime. A2A is planned as a future milestone once:

1. We define agent identities + a capabilities registry
2. We implement delegation and negotiation protocols
3. We add consent + audit trails (especially when AP2 is involved)

Tracking:
- Roadmap tickets: `todo.md` → Sprint 10 (A2A Future Plan)
- Architecture plan: `docs/OpenAgentPay-OSS-Architecture-Plan.md`

---

## Contributing

OpenAgentPay is an open-source project. Contributions are welcome!

See `CONTRIBUTING.md` for the canonical contribution guidelines and PR checklist.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the existing code style (TypeScript, React, Tailwind)
- Add tests for new features
- Update documentation for API changes
- Reference relevant protocol specs in PRs

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [Google Agentic Commerce](https://github.com/google-agentic-commerce) for AP2 and A2A protocols
- [Anthropic](https://anthropic.com) for MCP specification
- [OpenAI](https://openai.com) for MCP-UI patterns
- The open-source community for feedback and contributions

---

**OpenAgentPay** - Demonstrating the future of agentic commerce, one protocol at a time.
