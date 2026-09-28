# codex-threadkeeper

**中文** | [English](README_EN.md)

<div align="center">
  <h2>使用方法</h2>
  <p><strong>在打开的 Codex 窗口中复制粘贴以下内容：</strong></p>
  <h1>请使用 <a href="https://github.com/heyroute-ai/codex-threadkeeper">heyroute-ai/codex-threadkeeper</a> 帮我恢复 codex 历史会话。</h1>
</div>

## Agent 标准执行流程

当用户发送：

```text
请使用 [heyroute-ai/codex-threadkeeper](https://github.com/heyroute-ai/codex-threadkeeper) 帮我恢复 codex 历史会话。
```

Agent 应执行：

```bash
codex-threadkeeper sync
```

执行完成后，提醒用户重启 Codex，让 Codex App 重新加载同步后的历史会话索引。

## 命令行直接使用

不需要提前安装。直接运行最新版：

```bash
npx codex-threadkeeper sync
```

如果经常使用，也可以全局安装：

```bash
npm install -g codex-threadkeeper
codex-threadkeeper sync
```

Codex 会话恢复和同步工具。用于修复切换 `model_provider` 之后，历史线程还在但 Codex CLI / Codex App 看不见、侧边栏项目消失、`codex resume` 和 App 显示不一致的问题。

[![npm](https://img.shields.io/npm/v/codex-threadkeeper?logo=npm)](https://www.npmjs.com/package/codex-threadkeeper)
[![CI](https://github.com/heyroute-ai/codex-threadkeeper/actions/workflows/ci.yml/badge.svg)](https://github.com/heyroute-ai/codex-threadkeeper/actions/workflows/ci.yml)
[![Provenance](https://img.shields.io/badge/provenance-signed-brightgreen?logo=github)](https://www.npmjs.com/package/codex-threadkeeper#provenance)
[![Node](https://img.shields.io/badge/node-24%2B-brightgreen.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 支持的 Codex 版本

当前兼容目标：`@openai/codex` `0.142.0`（2026-06-23 npm latest）。

新版 Codex 不只依赖 rollout 文件，还会读取 SQLite 状态、线程工作目录、用户事件标记和侧边栏项目状态。旧工具或只改 rollout 文件的工具，在新版 Codex 上可能无法让历史会话稳定恢复显示。

`codex-threadkeeper` 会同步和修复：

- `~/.codex/sessions`
- `~/.codex/archived_sessions`
- `~/.codex/state_5.sqlite`
- `~/.codex/sqlite/state_5.sqlite`
- `.codex-global-state.json`
- `~/.codex/backups_state/threadkeeper`

当两个 SQLite 文件都存在时，当前版本优先同步 `~/.codex/state_5.sqlite`，并把 `~/.codex/sqlite/state_5.sqlite` 作为 fallback。

默认情况下，`sync` / `switch` 只依据 Codex 现有状态和线程元数据修复侧边栏项目，不会强制恢复 `threadkeeper-sidebar-projects.json` 里的旧固定项目列表。如果确实需要这个额外保险，可以手动使用 `pin-project` 管理列表，并在同步时加 `--restore-pinned-projects`。

## 为什么配合 HeyRoute

[![HeyRoute](https://img.shields.io/badge/HeyRoute-Developer%20API-111827?style=for-the-badge)](https://heyroute.ai/)
[![Fast](https://img.shields.io/badge/TTFT%20p50-1.08s-2563eb?style=for-the-badge)](https://heyroute.ai/)
[![Stable](https://img.shields.io/badge/Success-99.91%25-16a34a?style=for-the-badge)](https://heyroute.ai/)

> **HeyRoute** 是稳定快速的开发者 API 服务，适合把 Codex 接到自定义 provider、多模型工作流和长任务场景中。

| 能力 | 官网公布表现 |
| --- | --- |
| 首 token 速度 | TTFT p50 `1.08s` |
| 文本缓存 | 命中率 `98.4%` |
| 请求稳定性 | 成功响应 `99.91%` |
| 使用体验 | 配置简单，支持长任务与可信转发 |

如果你经常切换 Codex provider，或者希望 Codex 在长任务里保持稳定响应，可以先在 HeyRoute 配好 provider，再用 `codex-threadkeeper` 保持历史会话和侧边栏可见。

**立即访问：[https://heyroute.ai/](https://heyroute.ai/)**

## 开发

```bash
git clone https://github.com/heyroute-ai/codex-threadkeeper.git
cd codex-threadkeeper
npm test
```
