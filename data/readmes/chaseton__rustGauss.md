# rustGauss

[![Rust](https://img.shields.io/badge/rust-1.70%2B-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Phase%201-yellow.svg)]()

> A pure Rust client driver for openGauss database

rustGauss 是一个纯 Rust 实现的 openGauss 数据库客户端驱动项目。

> **注意**: 当前为**第一阶段 (Phase 1)** 原型实现，用于验证核心概念和协议兼容性。后续将进行全面重构，以提供生产级的高性能、内存安全的数据库连接能力。
> 今晚进入第二阶段，重构spark connector。

## 特性

- **纯 Rust 实现** - 无 C 依赖，完全内存安全
- **异步支持** - 基于 tokio 的异步 I/O
- **多种认证** - 支持 MD5、SHA256、SCRAM-SHA-256
- **TLS 加密** - 可选的 SSL/TLS 安全连接
- **连接池** - 可选的高性能连接池
- **完整类型支持** - 支持所有常用 PostgreSQL/openGauss 数据类型

## 快速开始

### 安装

在 `Cargo.toml` 中添加依赖：

```toml
[dependencies]
rustgauss = "0.1"
```

### 基本用法

```rust
use rustgauss::{Client, Config, Result};

fn main() -> Result<()> {
    // 创建配置
    let config = Config::new()
        .host("localhost")
        .port(5432)
        .user("gaussdb")
        .password("password")
        .dbname("postgres");

    // 连接数据库
    let mut client = Client::connect_with_config(config)?;

    // 执行查询
    let rows = client.query("SELECT $1::INT as num", &[&42])?;
    for row in rows.iter() {
        let num: i32 = row.get(0);
        println!("Result: {}", num);
    }

    // 事务操作
    let mut tx = client.begin()?;
    tx.execute("INSERT INTO users (name) VALUES ($1)", &[&"Alice"])?;
    tx.commit()?;

    client.close();
    Ok(())
}
```

## 架构设计

### 项目背景

openGauss 是华为开源的企业级关系型数据库，基于 PostgreSQL 内核开发，具有高性能、高安全、高可用等特性。

| 语言 | 驱动名称 | 状态 |
|------|---------|------|
| C | libpq | 官方支持 |
| Go | openGauss-connector-go-pq | 官方支持 |
| Java | openGauss JDBC Driver | 官方支持 |
| Python | psycopg2 (修改版) | 社区支持 |
| **Rust** | **rustGauss** | **本项目** |

### openGauss 与 PostgreSQL 的主要差异

| 特性 | PostgreSQL | openGauss |
|------|------------|-----------|
| 默认认证 | MD5 | SHA256 |
| 国密算法 | 不支持 | 支持 SM3/SM4 |
| 认证协议 | SCRAM-SHA-256 | RFC 5802 (扩展) |
| 协议版本 | 3.0 | 3.0 (扩展) |

### 通信协议

openGauss 使用基于 TCP/IP 的消息协议，协议分为两个阶段：

```
┌─────────────────────────────────────────────────────────────┐
│                     Protocol Phases                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐     Authentication      ┌─────────┐            │
│  │ Startup │ ──────────────────────► │ Normal  │            │
│  │  Phase  │                         │  Phase  │            │
│  └─────────┘                         └─────────┘            │
│       │                                   │                  │
│       ▼                                   ▼                  │
│  - StartupMessage                   - Simple Query           │
│  - Authentication                   - Extended Query         │
│  - ParameterStatus                  - COPY Protocol          │
│  - BackendKeyData                   - Function Call          │
│  - ReadyForQuery                    - Termination            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 消息格式

所有消息遵循统一格式：

```
┌──────────┬──────────┬─────────────────┐
│ Type (1B)│Length(4B)│   Payload       │
├──────────┼──────────┼─────────────────┤
│  'Q'     │   N+4    │ Query String    │
│  'R'     │   N+4    │ Auth Response   │
│  ...     │   ...    │ ...             │
└──────────┴──────────┴─────────────────┘
```

### 认证流程

openGauss 支持多种认证方式：

| 类型值 | 认证方式 | AuthReq 常量 |
|--------|---------|-------------|
| 0 | MD5 | 5 |
| 1 | SHA256+MD5 | 11 |
| 2 | SHA256 | 10 |
| 3 | SM3 | 13 |

**SHA256 认证流程 (RFC 5802)**:

```
Client                                    Server
  │                                         │
  │──────── StartupMessage ────────────────►│
  │                                         │
  │◄─────── AuthenticationSASL ─────────────│
  │         (mechanism list)                │
  │                                         │
  │──────── SASLInitialResponse ───────────►│
  │         (client-first-message)          │
  │                                         │
  │◄─────── AuthenticationSASLContinue ─────│
  │         (server-first-message)          │
  │                                         │
  │──────── SASLResponse ──────────────────►│
  │         (client-final-message)          │
  │                                         │
  │◄─────── AuthenticationSASLFinal ────────│
  │         (server-final-message)          │
  │                                         │
  │◄─────── AuthenticationOk ───────────────│
  │                                         │
```

### 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Application                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         rustGauss API                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Client     │  │  Connection  │  │     Transaction      │   │
│  │   Builder    │  │    Pool      │  │      Manager         │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Core Driver Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Protocol   │  │    Query     │  │       COPY           │   │
│  │   Handler    │  │   Executor   │  │      Handler         │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │    Type      │  │    Row       │  │     Notification     │   │
│  │   Codec      │  │   Parser     │  │       Handler        │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Authentication Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │    MD5       │  │   SHA256     │  │        SM3           │   │
│  │   Auth       │  │    Auth      │  │       Auth           │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │   SCRAM      │  │   Kerberos   │                             │
│  │   Handler    │  │   (GSSAPI)   │                             │
│  └──────────────┘  └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Transport Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │     TCP      │  │   SSL/TLS    │  │    Unix Socket       │   │
│  │   Socket     │  │   Handler    │  │      Handler         │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 模块划分

```
rustGauss/
├── Cargo.toml
├── src/
│   ├── lib.rs                 # 库入口
│   ├── client/                # 客户端 API
│   ├── connection/            # 连接管理
│   ├── protocol/              # 协议实现
│   │   ├── frontend.rs        # 前端消息
│   │   ├── backend.rs         # 后端消息
│   │   └── codec.rs           # 编解码
│   ├── auth/                  # 认证模块
│   │   ├── md5.rs             # MD5 认证
│   │   ├── sha256.rs          # SHA256 认证
│   │   └── scram.rs           # SCRAM 框架
│   ├── types/                 # 类型系统
│   │   ├── oid.rs             # OID 定义
│   │   ├── to_sql.rs          # Rust → SQL
│   │   └── from_sql.rs        # SQL → Rust
│   ├── config/                # 连接配置
│   ├── row/                   # 行处理
│   └── error/                 # 错误处理
├── examples/                  # 示例程序
├── tests/                     # 测试
├── benches/                   # 性能基准
└── docs/                      # 文档
```

### 类型映射

| PostgreSQL/openGauss 类型 | Rust 类型 | OID |
|---------------------------|-----------|-----|
| BOOLEAN | bool | 16 |
| SMALLINT | i16 | 21 |
| INTEGER | i32 | 23 |
| BIGINT | i64 | 20 |
| REAL | f32 | 700 |
| DOUBLE PRECISION | f64 | 701 |
| NUMERIC | Decimal | 1700 |
| VARCHAR/TEXT | String | 25/1043 |
| BYTEA | Vec<u8> | 17 |
| TIMESTAMP | NaiveDateTime | 1114 |
| TIMESTAMPTZ | DateTime<Utc> | 1184 |
| DATE | NaiveDate | 1082 |
| TIME | NaiveTime | 1083 |
| UUID | Uuid | 2950 |
| JSON/JSONB | serde_json::Value | 114/3802 |
| ARRAY | Vec<T> | * |

## 示例程序

项目包含多个示例程序：

| 示例 | 描述 | 运行命令 |
|------|------|----------|
| simple | 基础功能演示 | `cargo run --example simple` |
| benchmark | 性能测试 | `cargo run --example benchmark --release` |
| cli | 交互式 SQL 客户端 | `cargo run --example cli` |
| sample_db | 电商示例数据库 | `cargo run --example sample_db` |
| query | 命令行 SQL 执行器 | `cargo run --example query -- "SELECT 1"` |

### 运行示例

```bash
# 1. 启动 openGauss Docker
./scripts/docker_opengauss.sh start

# 2. 配置环境变量
source scripts/setup_env.sh

# 3. 运行示例
cargo run --example simple
```

## 测试

```bash
# 运行单元测试
cargo test --lib

# 运行所有测试
cargo test

# 运行性能基准
cargo bench
```

当前测试状态：
- 单元测试: 89 passing
- 集成测试: 8 passing

## Features

| Feature | 描述 | 默认启用 |
|---------|------|----------|
| `tls-rustls` | TLS 支持 (rustls) | ✓ |
| `pool` | 连接池支持 | - |
| `full` | 所有功能 | - |

```toml
# 启用连接池
rustgauss = { version = "0.1", features = ["pool"] }

# 启用所有功能
rustgauss = { version = "0.1", features = ["full"] }

# 禁用 TLS
rustgauss = { version = "0.1", default-features = false }
```

## 性能

在本地 openGauss 测试环境下的基准性能：

| 指标 | 性能 |
|------|------|
| 连接建立 | ~50ms |
| 简单查询 | < 1ms |
| 事务插入 | ~7,000/s |

## 路线图

### Phase 1 - 原型验证 (当前)

- [x] 核心协议实现
- [x] MD5/SHA256 认证
- [x] 基本类型支持
- [x] 事务管理
- [x] TLS 支持
- [x] 连接池

### Phase 2 - openGauss Spark Connector 重构 (进行中)

目标：打造生产级的 openGauss 与 Apache Spark 大数据集成方案

- [ ] 基于 Spark 3.5.x DataSource V2 API
- [ ] 性能优化：列裁剪、谓词下推、分区并行
- [ ] 高速写入：COPY 协议支持
- [ ] Catalog API 支持
- [ ] 完整类型映射

详见：[Phase 2 设计文档](docs/PHASE2_SPARK_CONNECTOR_DESIGN.md)

## 文档

详细文档请参阅 `docs/` 目录：

- [架构设计](docs/ARCHITECTURE_DESIGN.md)
- [需求清单](docs/REQUIREMENTS.md)
- [测试设计](docs/TEST_DESIGN.md)
- [设计汇总](docs/DESIGN_SUMMARY.md)

## 许可证

本项目采用双许可证：

- [MIT License](LICENSE-MIT)
- [Apache License 2.0](LICENSE-APACHE)

## 参考资料

- [openGauss 官方文档](https://docs.opengauss.org/)
- [PostgreSQL 协议规范](https://www.postgresql.org/docs/current/protocol.html)
- [RFC 5802 - SCRAM Authentication](https://tools.ietf.org/html/rfc5802)
