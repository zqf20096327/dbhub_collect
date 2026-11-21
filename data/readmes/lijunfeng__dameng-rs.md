# dameng-rs

达梦数据库（DM8）的 **SQLx 0.9.x** 驱动 workspace。

> **状态：实验性 0.1.x**
> 协议与最小 `Database`/`Executor`/`Transaction` 已落地；真实 DM8 联调、Statement Cache、Describe、TLS 仍在进行中。
> **请勿用于生产。** API 在 0.1 期间可能不兼容变更。

## Crates

| Crate | 说明 |
|-------|------|
| `dameng-types` | DM 类型码、值、编解码辅助 |
| `dameng-protocol` | DM8 二进制协议（Frame / Message） |
| `sqlx-dameng` | `sqlx-core` 驱动（对标 `sqlx-postgres`） |

规划与工程约定：[`docs/dameng.md`](docs/dameng.md) · [`docs/engineering.md`](docs/engineering.md) · 联调查验：[`docs/verification-checklist.md`](docs/verification-checklist.md)

## 要求

- Rust **1.94+**（见 `rust-toolchain.toml` / `rust-version`；对齐 sqlx-core 0.9.1）
- sqlx-core **0.9.x**

## 开发

```bash
just check              # fmt + clippy(-D warnings) + cargo deny
just test               # 单元测试（集成默认 ignore）
export DM_DATABASE_URL='dm://SYSDBA:SYSDBA@127.0.0.1:5236'
just test-integration   # 真实 DM8
just example-crud
```

## 用法（M1 预览）

```rust
use sqlx_core::query::query;
use sqlx_dameng::{Dameng, DmPool};

let pool = DmPool::connect("dm://SYSDBA:SYSDBA@127.0.0.1:5236").await?;

query::<Dameng>("SELECT 1 FROM DUAL")
    .fetch_one(&pool)
    .await?;
```

连接串：

```text
dm://SYSDBA:SYSDBA@127.0.0.1:5236
dameng://user:pass@host:5236/SCHEMA?auto_commit=true&isolation_level=read_committed
```

## 已知限制与处理策略（0.1）

| 点 | 现状 | 处理 |
|----|------|------|
| **Describe** | 用空结果子查询猜列 | 多语法尝试；失败则降级为「仅参数个数」，`prepare` 不整体失败 |
| **Cache** | 只缓存列/参数元数据 | 加速再次 `prepare`；**不**复用服务端 handle（ROLLBACK 会失效） |
| **timezone** | DSN 为小时偏移 | 依次试多种 SQL；全失败只 warn，不阻断建连 |
| TLS | feature `tls`（默认开） | 服务器需支持 SSL |
| offline / migrate / any | 未完成 | 见 `docs/dameng.md` M2/M3 |

联调时按 [`docs/verification-checklist.md`](docs/verification-checklist.md) 打勾并记下胜出 SQL / 日志原文。真实 DM8 联调通过前，请勿用于生产。

## License

MIT — 见 [LICENSE](LICENSE)。
