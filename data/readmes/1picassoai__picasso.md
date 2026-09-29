# Picasso for Microsoft Agent Framework

**See what your agents are actually emitting — and what compaction quietly threw away.**

A local conversation store and read-only dashboard for [Microsoft Agent Framework](https://github.com/microsoft/agent-framework).
Two small NuGet packages, one line of code each, a SQLite file next to your app. No Docker, no
cloud account, no telemetry. Nothing leaves your machine.

**Use it to** persist MAF agent chat history to a database by conversation id · keep
conversations across application restarts · implement a custom `ChatHistoryProvider` · see
what your agent emitted, with tool calls, arguments and timings · detect context
compaction silently dropping the first user message · inspect agent behaviour locally
without standing up a self-hosted observability stack.

```bash
dotnet add package Picasso.AgentFramework.Persistence
dotnet add package Picasso.AgentFramework.Dashboard
```

---

## Why

Agent Framework's compaction rewrites the working set when the context window fills. It does
this silently, and **the opening user message is often the first casualty** — the agent carries
on with no record of what it was originally asked, and nothing tells you it happened.

Picasso keeps the full conversation regardless, and shows you the moment the context was cut:

```
14:22:19   BillingAgent    A refund of £24.99 has been issued.
14:22:11   ⚠ COMPACTION    12 messages → 3
                           dropped: the first user message
14:22:07   User            why was I charged twice this month
```

![The Picasso dashboard](docs/dashboard.png)

---

## Install

```bash
dotnet add package Picasso.AgentFramework.Persistence
```

Attach it to your agent:

```csharp
var agent = chatClient.AsAIAgent(new ChatClientAgentOptions
{
    Name = "Assistant",
    ChatHistoryProvider = new SqliteChatHistoryProvider("./picasso.db")
});
```

That is the whole integration. Conversations now persist to `picasso.db` beside your app and
survive restarts.

### Add the dashboard

```bash
dotnet add package Picasso.AgentFramework.Dashboard
```

```csharp
app.MapPicasso();   // then open /picasso
```

---

## What you get

| | |
|---|---|
| **Conversations that survive a restart** | Stored by conversation id, in order, roles intact |
| **No duplicated messages** | Appends only what is new; earlier rows are never rewritten |
| **Conversations stay isolated** | One conversation never bleeds into another |
| **A record of every compaction** | Before and after counts, and whether the first user message was lost |
| **A local dashboard** | Live stream of what each agent said, called and dropped |

---

## What it does not do

Stated plainly, because a tool that hides its limits gets found out by a stranger.

- **The dashboard is read-only.** No delete, replay, edit or export. Every route is a `GET`.
- **It does not stop compaction.** It records what compaction removed. Agent Framework still
  decides what the model sees; Picasso makes the loss visible and keeps the full history.
- **Compaction detection is early.** It infers a compaction by comparing what the model was
  sent against what is stored. It never invents one — but if your setup replays history in a
  way it does not recognise, it may miss one silently. **Your conversations are still stored in
  full; only the compaction banner would be absent.** If you hit that, please open an issue —
  a real-world repro is exactly what this needs.
- **SQLite only, for now.** SQL Server and Postgres are next.
- **It is not a production observability platform.** It is a local development tool, in the
  same spirit as the Aspire dashboard.

---

## Add the store to your `.gitignore`

The database sits next to your app so it is easy to find. That also means it is easy to commit
by accident — **and it contains your conversation history.**

```gitignore
picasso.db
picasso.db-shm
picasso.db-wal
```

**If you passed a different filename**, ignore that one instead — the lines above only cover
the default. A safer catch-all if you have no other SQLite files in the project:

```gitignore
*.db
*.db-shm
*.db-wal
```

---

## Privacy

Everything is local. There is no phone-home, no analytics, no account, and no network call of
any kind. The database is a file on your disk; the dashboard is served by your own application.

---

## Samples

- **`samples/Picasso.Chat`** — the smallest thing that works: a console chat agent on OpenAI with
  the store underneath, so every turn lands in `./picasso.db`. Set `OPENAI_API_KEY` and
  `dotnet run --project samples/Picasso.Chat`. Needs the .NET 10 SDK (the samples target
  `net10.0`; the packages themselves target 8, 9 and 10).
- **`samples/Picasso.DemoAgent`** — a web host with the dashboard attached, seeded with demo data.

---

## Requirements

- **.NET 8.0, 9.0 or 10.0** — the packages multi-target all three (the samples need the .NET 10 SDK)
- `Microsoft.Agents.AI` 1.20.0 or later

## Licence

MIT. Fork it, vendor it, support it internally — if this project ever goes quiet, you are not
stuck.

---

Built by [1picassoai](https://github.com/1picassoai). Not affiliated with Microsoft.
