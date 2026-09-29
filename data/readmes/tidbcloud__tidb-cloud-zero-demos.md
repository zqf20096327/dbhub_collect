# TiDB Cloud Zero Demos

This repository collects product demos built around **TiDB Cloud Zero**.

TiDB Cloud Zero is a zero-signup, zero-config, zero-friction way to get instant access to a real **TiDB Cloud** SQL database environment. It is **MySQL-compatible**, **TLS-secured**, and built for rapid prototyping, demos, automation, and AI agent workflows.

## What is TiDB Cloud Zero?

TiDB Cloud Zero is designed for cases where you want a database immediately, without going through a traditional cloud onboarding flow first.

It is especially useful for:

- AI agents that need an on-demand database
- developers validating SQL or building quick prototypes
- demos, tutorials, hackathons, and workshops
- automation and CI-style workflows

Key characteristics:

- **Zero signup**: start without creating an account for the initial session
- **MySQL-compatible**: works with familiar SQL tools and drivers
- **Fast provisioning**: disposable database environments are created quickly
- **Vector search enabled**: supports AI-native application patterns
- **Ephemeral by design**: ideal for experiments, tests, and short-lived workloads

## What's in This Repo

### `tidb-cloud-zero-mcp-main`

An MCP server that lets AI agents access TiDB Cloud Zero as a database tool with almost no setup.

Highlights:

- auto-provisions a TiDB Cloud Zero instance on first use
- exposes SQL operations through Model Context Protocol
- works with agent tools such as Claude Desktop, Claude Code, Cursor, and similar MCP clients

### `tidb-cloud-zero-browser-main`

A browser-based SQL editor and playground for TiDB Cloud Zero.

Highlights:

- provisions a Zero instance from the browser flow
- runs SQL through TiDB's HTTP API
- demonstrates an instant "try SQL now" experience

### `tidb-quest-main`

A browser game that teaches TiDB Cloud concepts through DBA-style challenges.

Highlights:

- uses gameplay to explain concepts like RU, indexing, TiFlash, vector search, and Zero
- stores game state on TiDB Cloud Zero
- shows how Zero can support lightweight interactive apps

### `agent-economy-demo-main`

A demo of AI agents that can pay for data, store memory, and take action.

Highlights:

- uses TiDB Cloud Zero as the agent memory layer
- logs market data, decisions, and payment history
- demonstrates how Zero fits into agentic application architecture

## Why This Collection Exists

These demos show TiDB Cloud Zero from multiple product angles:

- as infrastructure for **AI agents**
- as a backend for **instant browser experiences**
- as a persistence layer for **interactive demos and education**
- as a lightweight database for **experimentation and prototyping**

Together, they help explain the core promise of TiDB Cloud Zero: making a real cloud database available immediately, with minimal friction.

## Getting Started

Each demo lives in its own folder and may have its own setup instructions. Start with the README inside the demo you want to run:

- [`tidb-cloud-zero-mcp-main/README.md`](./tidb-cloud-zero-mcp-main/README.md)
- [`tidb-quest-main/README.md`](./tidb-quest-main/README.md)
- [`agent-economy-demo-main/README.md`](./agent-economy-demo-main/README.md)

The browser SQL editor currently does not include a dedicated README, so the implementation in `tidb-cloud-zero-browser-main/` serves as the reference for that demo.

## Learn More

- [TiDB Cloud Zero](https://zero.tidbcloud.com/)
- [TiDB Cloud](https://www.tidbcloud.com/)
- [PingCAP](https://www.pingcap.com/)
