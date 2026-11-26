# DeepORG — One AI Agent for Your Whole Organization

[![Apache 2.0](https://img.shields.io/github/license/dosco/deeporg.svg?style=for-the-badge)](https://github.com/dosco/deeporg/blob/master/LICENSE)
[![NPM Package](https://img.shields.io/npm/v/deeporg?style=for-the-badge)](https://www.npmjs.com/package/deeporg)
[![Docker Pulls](https://img.shields.io/docker/pulls/dosco/graphjin?style=for-the-badge)](https://hub.docker.com/r/dosco/graphjin/tags)
[![Discord Chat](https://img.shields.io/discord/628796009539043348.svg?style=for-the-badge&logo=discord)](https://discord.gg/6pSWCTZ)
[![GoDoc](https://img.shields.io/badge/godoc-reference-5272B4.svg?style=for-the-badge&logo=go)](https://pkg.go.dev/github.com/dosco/graphjin/core/v3)

> **DeepORG was formerly GraphJin.** The Go module keeps the `graphjin` name for now. The npm package and the Docker images are published as `deeporg`, and under the old name as well.

DeepORG is an AI agent that answers questions and makes changes across the
systems your company already runs: databases, warehouses, APIs, files and
source code. Ask it in plain words; it finds the right tables, has the database
do the work, and answers with the data behind it. It can only see and change
what your access rules allow, and by default a change waits for your approval.

## Why it's different

**No hand-built tools.** Most company agents are wired up one tool at a time:
a "get customer" tool here, a "list invoices" tool there, each written and
maintained by hand. They break when a schema changes, and every new question
or new system means more tools. DeepORG gives the agent a searchable map of
everything you connect, and the agent writes its own queries against it. The
engine checks each query against your access rules and runs it as one efficient
database query. Connecting a new database or API is a few lines of config, not
a new set of tools.

**Proven on a public benchmark.** [DeepORG, the Organizational Agent
Benchmark](https://deeporg.io/benchmarks/deeporg/) scores AI models on real
organizational work against a live system: answers, changes, alerts, follow-ups
and questions that span several sources. The best published run scores 97 of
100 with zero unsafe actions, and every score links to the exact test and build
that produced it.

**Turn your organization into a training environment.** The same machinery
generates checked tasks from your own systems and serves them as graded
episodes, so you can measure an agent, or train one with reinforcement
learning, on your organization instead of a toy.
[Agent environment](https://deeporg.io/environment/)

Underneath is GraphJin, the open-source engine that compiles each query into a
single database query. It is also a GraphQL API server and a Go library in its
own right.

## Install

```bash
curl -fsSL https://deeporg.io/install.sh | bash   # macOS and Linux
npm install -g deeporg                            # any platform
brew install dosco/deeporg/deeporg                # macOS
```

The command is `deeporg`. The old name, `graphjin`, still works as an alias.

If you installed the `graphjin` npm package before, run `npm uninstall -g graphjin`
first: both packages install the same two commands.

Windows: use `npm install -g deeporg`, or download the Windows archive from
the [releases page](https://github.com/dosco/deeporg/releases). Linux packages
are on the same page, and Docker is `docker pull dosco/deeporg`.

## Try it

```bash
deeporg
```

This starts DeepORG and opens a setup page in your browser. You create an admin
account, connect a database or choose the sample data, and pick a model. Then
you ask a question. There is no config file to write: DeepORG keeps its own
files in `~/.deeporg/`.

The setup steps are in the [quick start](https://deeporg.io/start/quick-start/).
For a larger demo company with routines and saved work already in it, run
`deeporg serve --demo`; see [Demos](https://deeporg.io/start/demos/).

## Use it from Claude Code

Open **Connect** in the console and copy the command it shows:

```bash
claude mcp add --transport http --scope user deeporg http://127.0.0.1:8080/api/v1/mcp
```

Then type `/mcp` in Claude Code, choose `deeporg` and Authenticate. Your browser
opens on DeepORG, where you choose Allow. There is no token to copy. Claude Code
asks DeepORG's built-in agent, so choose a model during setup first.

Other clients: [MCP](https://deeporg.io/agentic/mcp/). Servers that sign people
in through an identity provider: [MCP OAuth](https://deeporg.io/agentic/oauth/).

## Learn more

| | |
|---|---|
| Get started | [Quick start](https://deeporg.io/start/quick-start/) · [Your first query](https://deeporg.io/start/first-query/) |
| The agent | [How it works](https://deeporg.io/agentic/server-agent/) · [Conversations](https://deeporg.io/agentic/lead-agent/) · [Watches](https://deeporg.io/agentic/watches/) · [Workflows](https://deeporg.io/agentic/workflows/) |
| Connect your systems | [Databases](https://deeporg.io/reference/database-support/) · [APIs](https://deeporg.io/integrations/openapi/) · [Files](https://deeporg.io/integrations/filesystem-uploads/) · [Source code](https://deeporg.io/integrations/codesql/) |
| Run it in production | [Production](https://deeporg.io/configure/environment-production/) · [Access rules](https://deeporg.io/configure/auth-rbac/) · [Config reference](CONFIG.md) |
| GraphQL and Go | [Query language](https://deeporg.io/core/) · [Go examples](https://pkg.go.dev/github.com/dosco/graphjin/core#pkg-examples) |
| Measure agents | [Benchmark](https://deeporg.io/benchmarks/deeporg/) · [Agent environment](https://deeporg.io/environment/) |

Works with PostgreSQL, MySQL, SQLite, MongoDB, Oracle, SQL Server, Snowflake,
BigQuery, Cassandra, S3, GCS and local files.

## Community

[Discord](https://discord.gg/6pSWCTZ) · [Twitter @dosco](https://twitter.com/dosco)

## License

[Apache 2.0](https://opensource.org/licenses/Apache-2.0)
