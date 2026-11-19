# aoa

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![npm](https://img.shields.io/npm/v/@aoa-dev/sdk?label=%40aoa-dev%2Fsdk)](https://www.npmjs.com/package/@aoa-dev/sdk)
![Bun](https://img.shields.io/badge/Bun-1.3-14151a?logo=bun&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?logo=typescript&logoColor=white)
![Conformance](https://img.shields.io/badge/conformance-C1%E2%80%93C20-3f9a72)

中文 · [English](README.en.md)

在 Bun 上搭 Always-on Agent 的 SDK。agent 按 Inbox + Worker 模式 24x7 运行：事件进 inbox，worker 开 run 交给模型，危险的工具调用停下来等人批准，进程随时被杀也能接着做。

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/sdk-dark.png">
  <img alt="aoa SDK 架构：你的应用用 append、answer 往 Inbox 写事件和审批答复，用 schedule、followUp 设定时器，用 messages、watch 读 Outbox；每个 agent 有 Inbox、Worker、Timers、Memory、Outbox、Permissions 和 Tools，可以有多个 agent，用 send_to 互发；Worker 把 run 交给 runtime，第一档是内置的 pi，第二档是外部 harness，Codex 和 dsh 的适配器在 examples/；runtime 的工具调用回到 Permissions，放行的交给 Tools 执行，要审批的经 Outbox 发出；所有 agent 共用一个 SQLite 文件" src="docs/diagrams/sdk-light.png">
</picture>

想直接用一个写代码的 agent，见建在这个 SDK 上的 [`aoa` 命令](apps/aoa/README.md)。

## 安装

只支持 Bun（≥ 1.3），包里直接是 TypeScript 源码。

```bash
bun add @aoa-dev/sdk
# 用内置的 pi runtime 时再装它的 peer 依赖（用 @aoa-dev/sdk/loop 不需要）
bun add @earendil-works/pi-ai@1.5.2 @earendil-works/pi-coding-agent@1.5.2 typebox@1.3.27
```

## 一个例子

一个会发邮件的 agent。发邮件是高风险工具，内核先停下来要批准，批准后才执行，而且只执行一次。

```ts
import { createHost, sqliteStore, type ToolDef } from "@aoa-dev/sdk";
import { piRuntime } from "@aoa-dev/sdk/pi";

const sendEmail: ToolDef = {
  name: "send_email",
  description: "Send an email.",
  schema: { type: "object", properties: { to: { type: "string" }, body: { type: "string" } }, required: ["to", "body"] },
  risk: "high",
  async execute(args) {
    console.log("sending", args);
    return { sent: true };
  },
};

const host = createHost({ store: sqliteStore("agent.db") });
const agent = host.agent({
  name: "assistant",
  inbox: "assistant",
  runtime: piRuntime({
    provider: "deepseek",
    modelId: "deepseek-v4-pro",
    apiKey: process.env.DEEPSEEK_API_KEY,
    agentDir: ".aoa/pi",
    sessionsDir: ".aoa/sessions",
    cwd: process.cwd(),
    systemPrompt: "You are a helpful assistant. When a task is done, tell the user with notify.",
  }),
  tools: [sendEmail],
});

// agent 的消息都进 outbox；没有 channel 时从 host.messages() 读。
let seen = host.messages().at(-1)?.id;
const answered = new Set<string>();
host.watch(() => {
  for (const m of host.messages(seen ? { since: seen } : {})) console.log(`[${m.kind}] ${m.body}`);
  seen = host.messages().at(-1)?.id ?? seen;
  // 示例里直接批准；真实应用在这里把决定交给人。调用在新 run 接手前一直算待审批，只答一次。
  for (const call of agent.read.pending()) {
    if (answered.has(call.callId)) continue;
    answered.add(call.callId);
    agent.answer(call.callId, { verdict: "approve" });
  }
});

agent.append({
  source: "user_message",
  dedupeKey: crypto.randomUUID(),
  payload: { text: "Email bob@example.com: the build is green." },
  trusted: true,
});
host.start();
```

```bash
DEEPSEEK_API_KEY=... bun main.ts
```

会先看到一条 `[approval_request]`，然后 `sending { ... }`。进程常驻，用 Ctrl-C 退出。默认是后台静默模式，agent 只有调用 `notify` 时才发消息；做对话类助手时传 `reply: "final_text"`，模型的最终文字回复就会自动进 outbox（按钮/卡片审批可再配 `approvals: { by: "answer" }`，并从 `OutMsg.detail` 读结构化审批信息）。

## 原语

都在内核里，状态都在一个 SQLite 文件里。

- **Inbox** 收事件。用 `agent.append` 追加，按 `(source, dedupeKey)` 去重，`thread` 把同一段对话的事件归到一个 session。`trusted` 由追加的一方标明内容是不是用户本人说的，SDK 不判断调用者是谁。
- **Worker** 认领一批事件，开一次 run 交给 runtime，再记下这次 run 的结局。一个 inbox 同时只有一个 run，不同 agent 的 run 可以同时跑。
- **Timers** 到点唤醒：`agent.followUp` 定一次，`agent.schedule({ id })` 定周期，同一个 id 重启时不会多出一条。
- **Memory** 跨 run 保留指令、笔记和进度，传 `memory`（比如 `dirMemory`）才有。
- **Permissions** 决定每次工具调用能不能做，见下一节。
- **Outbox** 发消息并重试送达。传 `channel` 就送到那里（本地文件、GitHub 等）；不传时写入即算送出，从 `host.messages()` 读。

另外：`host.watch` 在库有提交时通知你，其他进程的提交一秒内也能收到；`agent.read` 只读地查 session、事件、待审批、定时器、run 和日志；`agent.activity` 实时给出模型的文字和每次工具调用；`agent.abort` 中断一个 session 正在跑的 run，事件放回去重跑（0.1.1 起）。

## 权限

每次工具调用按顺序裁决：

1. `policy.rules` 里第一条有意见的规则，结果是允许、拦截或延后。
2. 没有规则管，就看风险等级：工具自己的 `risk`，可以用 `policy.risk` 覆盖，都没写就是 `high`。
3. `low` 直接放行，`high` 延后等人，`medium` 交给 `policy.classify` 判断；没有 classifier、出错或拿不准，也延后等人。

```ts
host.agent({
  name: "assistant",
  inbox: "assistant",
  runtime,
  tools: [sendEmail],
  policy: {
    rules: [{ name: "no-prod", match: (call) => (JSON.stringify(call.args).includes("prod") ? "block" : null) }],
    risk: { send_email: "medium" },
    classify: piClassifier({ provider: "deepseek", modelId: "deepseek-flash", apiKey: process.env.DEEPSEEK_API_KEY }),
  },
});
```

`piClassifier` 的提示词是给写代码的 agent 写的；别的场景自己写一个 `classify`，它拿到调用和 session 是否沾过外人内容，返回 `allow`、`block` 或 `unsure`。

延后就是 deferred tool call：内核保存会话、结束这次 run，往 outbox 发一条审批请求，worker 接着处理别的事件。`agent.answer` 的答复作为新事件进 inbox，内核执行这一次调用，再开新 run 接着做。只有 `answer` 或可信的 `user_message` 算数，外人写的内容和其他 agent 的消息都不行。

内核自带的工具（timers、notify、memory、`send_to`）自己标了 `low`。写代码用的 bash、read、edit、write 和配套的规则在可选的 `@aoa-dev/sdk/tools/coding` 里，不默认装上。

## Runtime

- **第一档（内核管每次工具调用）**：`@aoa-dev/sdk/pi` 内置 pi 的多模型接入与会话管理（见 [`examples/tui`](examples/tui)）；不想装 pi 时，`@aoa-dev/sdk/loop` 零第三方依赖，传一个 `complete()` 函数就能接任意模型 SDK 或原生 `fetch`。
- **第二档：外部 harness**（`HarnessRuntime`），用它们自己的工具和沙箱，把需要确认的操作经 `ask` 转成 aoa 的审批请求；SDK 定义接口并在一致性测试里覆盖六条约定，不内置具体 harness 实现。

## 多个 agent

一个 host 持有多个 agent，共用一个库和一个时钟。agent 之间只通过往对方的 inbox 写事件合作，`send_to` 是现成的工具：

```ts
const sendTo = sendToTool(host);
host.agent({ name: "writer", description: "drafts replies", inbox: "writer", runtime, tools: [sendTo] });
host.agent({ name: "checker", description: "checks drafts", inbox: "checker", runtime, tools: [sendTo] });
```

回信会回到发信的 session。一条链上最多 4 条 agent 消息，再多就被拒，两个 agent 不会一直聊下去。

## 崩溃后接着做

- **进程随时能杀。** 一次 run 结束时，结果、会话和「这批事件已处理」在同一个事务里写进去。重启后没处理完的事件还在 inbox 里，会被重新取走再跑。
- **认领有有效期。** worker 取事件时在库里登记一个有效期（5 分钟，跑着会续），过期没完成就算失败。失败的事件 30 秒、2 分钟后重试，三次都失败就成为死信、不再重试；属于某个 session 的死信会往 outbox 发一条通知。
- **重跑不会重复执行工具。** 工具执行前先记一笔；重跑时遇到记过却没有结果的调用，不再执行，而是告诉 agent「结果未知，先查再决定」。标了 `idempotent` 的工具例外。
- **事件和消息不重复。** 事件按来源去重；outbox 送达失败按 1、2、4、8 分钟重试，五次都失败就标为失败。

### 一致性测试

[规范](docs/spec.md) §9 的 C1–C20 每条先写成失败的测试再实现，跑在带故障注入点的假 runtime 和假时钟上。每个提交点都有名字（`after_append`、`after_claim`、`after_tool_exec`、`after_tool_result`、`before_complete`），测试在这些位置杀进程再恢复。

## 示例和应用

| | |
|---|---|
| [`examples/tui`](examples/tui) | 极简终端对话 agent：用 `@aoa-dev/sdk/pi` 流式对话、规则放行只读检查、`/y` 审批写操作、Ctrl-C 中断与重启恢复 |
| [`apps/aoa`](apps/aoa/README.md) | `aoa` 命令：写代码的后台 agent，CLI、MCP、GitHub、观察页 |

0.x 期间接口可能有破坏性改动。设计见 [docs/design/](docs/design/README.md)，SDK 每一步的取舍见 [docs/design/sdk.md](docs/design/sdk.md)，规范见 [docs/spec.md](docs/spec.md)。

## 开发

Bun + TypeScript 的 monorepo。

| 包 | 作用 |
|---|---|
| `packages/sdk` | 唯一对外发布的包 `@aoa-dev/sdk`：五个原语、SQLite 存储（`sqliteStore`）、宿主、`@aoa-dev/sdk/loop`、`@aoa-dev/sdk/pi`、可选的编码工具和规则（`@aoa-dev/sdk/tools/coding`） |
| `packages/channels/`：`local` · `github` | 本地和 GitHub 通道（`apps/aoa` 用） |
| `packages/conformance` | 规范 §9 的 C1–C20 一致性测试 |
| `examples/tui` | 极简终端对话示例 |
| `apps/aoa` | `aoa` 命令 |

```bash
bun test               # 全部测试，不调用真实模型
bun run typecheck
bun scripts/diagrams/build.ts   # 从 docs/diagrams/boards 重新生成 README 里的图（需要 Chrome）
```
