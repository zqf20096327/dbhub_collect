# Sondar

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="Sondar 将 GitHub、AIHOT、HNRSS 与 ZHN 信号经过证据门分流为 STRIKE、WATCH、IGNORE 或 KILL">
</p>

<p align="center">
  <a href="https://go.dev/"><img src="https://img.shields.io/badge/Go-1.26-00ADD8?logo=go&amp;logoColor=white" alt="Go 1.26"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-7D858F" alt="AGPL 3.0 License"></a>
</p>

**把多源 AI 生态噪音，压缩成可执行、可追责、可关闭的商业决策。**

Sondar 是一个面向 AI Builder 的 Go CLI 与 Agent Skill。它持续收集 GitHub、AIHOT、Hacker News 和 ZHN/ishell 等来源的变化，用证据而不是热度决定今天应该行动、观察、忽略还是终止。

每个严肃信号都必须带上证据、负责人、截止时间、指标和关闭路径。

## 先看结果

一次运行会留下三类可审计产物：

```text
.sondar/state.sqlite                       # 跨天状态与 WATCH 生命周期
.sondar/data/signals/YYYY-MM-DD.jsonl     # 完整信号记录
.sondar/reports/YYYY-MM-DD.md             # 供人决策的日报
```

日报只突出当天需要处理的变化；达到 `WATCH` 门槛但超出报告上限，或与上次相比没有实质变化的项目，仍保留在 JSONL 和 SQLite 中继续复核，不会被悄悄丢弃。

| 决策 | 含义 | 必要约束 |
| --- | --- | --- |
| `STRIKE` | 现在行动 | 48 小时内可执行，有 buyer evidence、owner、deadline 和 metric |
| `WATCH` | 等待关键证据 | 有 upgrade trigger、next review 和 expiry，并持续保留生命周期 |
| `IGNORE` | 当前不投入 | 明确记录低价值、无买家、弱证据或不相关 |
| `KILL` | 不再返回 | 只有出现新证据才重新打开 |

## 快速开始

构建并运行完全本地的链路检查：

```bash
make build

./bin/sondar daily \
  --skip-gh \
  --skip-sources \
  --out-dir /tmp/sondar-dry-run \
  --db /tmp/sondar-dry-run/state.sqlite \
  --date 2026-06-24T09:00:00 \
  --json
```

因为显式跳过了全部数据源，预期结果是 `signal_count: 0`。这一步验证 CLI、SQLite、JSONL 和 Markdown 报告链路，不会在仓库内写入运行数据。

接入真实数据源：

```bash
cp config/watchlist.example.yml config/watchlist.yml
gh auth status

./bin/sondar daily \
  --config config/watchlist.yml \
  --db .sondar/state.sqlite \
  --out-dir .sondar \
  --skip-tanso
```

`config/watchlist.yml`、`.sondar/` 与其他本地运行数据已被 Git 忽略。

## 为什么不是热点榜

- **行为证据优先于热度。** Stars、trending、精选列表和发布新闻只能创建候选。
- **行动必须可追责。** `STRIKE` 必须具备 `owner`、`deadline`、`metric` 和 `next_action`。
- **等待必须有出口。** 每个 `WATCH` 都必须升级、过期或被关闭；未变化项目不会每天重复占用报告名额。
- **报告上限不等于数据丢弃。** 超出可读报告容量的合格信号仍保留为后台 `WATCH`。

> **No signal enters unless it can leave.**
>
> 一个不能被执行、升级、忽略或关闭的信号，不应该进入系统。

## 工作方式

```text
采集 → 快照与变化检测 → 相关性过滤 → 证据评分 → 四态决策 → 行动与关闭
```

自动 `STRIKE` 不能只依赖仓库活跃、release、issue 关键词或外部文章；它还需要买家或部署语境、可靠证据和可证伪的 48 小时行动。

| 来源 | 角色 | 边界 |
| --- | --- | --- |
| GitHub | repo、issue、release 与 builder 行为 | 活跃度不能单独触发 `STRIKE` |
| AIHOT | 结构化 AI 动态 | 只为相关 thesis 创建候选 |
| HNRSS | Hacker News JSON Feed | 注意力需要行为或买家证据佐证 |
| ZHN/ishell | 中文精选注意力 | 首次运行建立静默基线；不能独立触发 `STRIKE` |
| `tanso` | 可选的非 GitHub 佐证 | 不能替代 primary behavior evidence |

## 环境与开发

- Go 1.26
- 支持 CGO 的 C 编译器
- `gh` CLI，用于实时 GitHub 获取
- 可选 `tanso`，用于非 GitHub 佐证

提交改动前运行：

```bash
make fmt-check
make test
make vet
```

## 文档

- [使用 SOP](docs/sop.md)
- [评分规则](references/scoring.md)
- [数据源扩展](docs/source-adapters.md)
- [输出示例](references/examples.md)
- [AI Builder watchlist](docs/ai-builder-watchlist.md)

发现问题或漏报，请提交 [GitHub Issue](https://github.com/geekjourneyx/sondar/issues)。

## License

Sondar is licensed under the [GNU Affero General Public License v3.0 only](./LICENSE).
